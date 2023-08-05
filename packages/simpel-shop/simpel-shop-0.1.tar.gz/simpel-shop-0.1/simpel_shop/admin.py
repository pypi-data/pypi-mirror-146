from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import path, reverse
from django.utils.translation import gettext as _
from simpel_contacts.admin import DeliverableAddressInline

from simpel_admin.base import ModelAdminMixin
from simpel_products.models import Group

from .models import Cart, CartItem, CartItemBundle
from .settings import shop_settings
from .views import AddItemFormView, CheckoutWizzardView


class AdminAddItemView(AddItemFormView):
    template_name = "admin/simpel_shop/cart_add_item.html"
    model_admin = None
    shop_adapter = None

    def __init__(self, model_admin, **kwargs):
        self.model_admin = model_admin
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(admin.site.each_context(self.request))
        return context

    def get_success_url(self):
        messages.success(self.request, _("Success add product to cart"))
        return self.model_admin.get_changelist_url()

    def get_cancel_url(self):
        return self.model_admin.get_changelist_url()


class AdminCheckoutWizzardView(CheckoutWizzardView):
    model_admin = None

    def dispatch(self, request, *args, **kwargs):
        self.shop_adapter = self.get_shop_adapter(request)
        return super().dispatch(request, *args, **kwargs)

    def __init__(self, model_admin, **kwargs):
        self.model_admin = model_admin
        super().__init__(**kwargs)

    def get_success_url(self):
        messages.success(
            self.request,
            _("Sales Order created, complete payment and send confirmation."),
        )
        return reverse(
            admin_urlname(self.instance._meta, "inspect"),
            args=(self.instance.id,),
        )

    def get_redirect_url(self):
        return self.model_admin.get_changelist_url()

    def get_template_names(self):
        return self.model_admin.checkout_template

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update(
            {
                **admin.site.each_context(self.request),
            }
        )
        return context


class CartItemBundleInline(admin.TabularInline):
    model = CartItemBundle
    extra = 0
    autocomplete_fields = ["product"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(required=False)

    def has_add_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_view_permission(self, request, obj=None):
        return True


class ShopAdmin(ModelAdminMixin):
    readonly_fields = ("cart",)
    inspect_enabled = False
    raw_id_fields = ["cart", "product"]
    search_fields = ("name", "product__name")
    change_list_template = "admin/simpel_shop/cart.html"
    checkout_template = shop_settings.SHOP_ADMIN_CHECKOUT_TEMPLATE
    checkout_view_class = shop_settings.SHOP_ADMIN_CHECKOUT_VIEW
    additem_view_class = shop_settings.SHOP_ADMIN_ADDITEM_VIEW
    adapter_class = shop_settings.ADAPTER_CLASS

    def get_shop_adapter(self, request):
        return self.adapter_class(request)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(cart__user=request.user).select_related("product").prefetch_related("bundles")

    def get_inlines(self, request, obj=None):
        inlines = []
        if obj:
            if obj.product.is_deliverable:
                inlines.append(DeliverableAddressInline)
            if obj.product.is_bundle:
                inlines.append(CartItemBundleInline)
        return inlines

    def has_remove_permission(self, request, obj=None):
        if obj:
            return obj.cart.user == request.user
        return True

    def has_add_permission(self, request, obj=None):
        return request.user.has_perms(
            [
                "simpel_sales.add_salesorder",
                "simpel_sales.add_salesquotation",
            ]
        )

    def has_delete_permission(self, request, obj=None):
        return self.has_add_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        return self.has_add_permission(request, obj)

    def has_view_permission(self, request, obj=None):
        return self.has_add_permission(request, obj)

    def changelist_view(self, request, extra_context=None):

        if not self.has_add_permission(request):
            raise PermissionError(_("You don't have any permission!"))

        self.request = request
        self.cart = Cart.get_for_user(self.request.user)
        resp = super().changelist_view(request, extra_context=extra_context)
        context = resp.context_data
        qs = context["cl"].queryset
        context.update(
            {
                "cart": self.cart,
                # "checkout_form": self.get_checkout_form(),
                "items_total": sum([item.total for item in qs.all()]),
                "items_count": qs.count(),
            }
        )
        return render(request, self.change_list_template, context)

    def get_urls(self):
        super_urls = super().get_urls()
        urls = [
            path(
                "hx-cartitems-table/",
                admin.site.admin_view(self.htmx_cartitems_table),
                name="%s_%s_hx_cartitem_table" % (self.opts.app_label, self.opts.model_name),
            ),
            path(
                "checkout/",
                admin.site.admin_view(self.checkout_view),
                name="%s_%s_checkout" % (self.opts.app_label, self.opts.model_name),
            ),
            path(
                "add-item/<int:object_id>/",
                admin.site.admin_view(self.additem_view),
                name="%s_%s_add_item" % (self.opts.app_label, self.opts.model_name),
            ),
            path(
                "remove-item-bundle/<int:object_id>/",
                admin.site.admin_view(self.remove_item_bundle),
                name="%s_%s_remove_bundle" % (self.opts.app_label, self.opts.model_name),
            ),
        ]
        urls += super_urls
        return urls

    def checkout_view(self, request):
        if not self.has_add_permission(request):
            raise PermissionError(_("You don't have any permission!"))
        self.request = request
        self.shop_adapter = self.get_shop_adapter(request)
        return self.checkout_view_class.as_view(model_admin=self)(request)

    def additem_view(self, request, object_id):
        self.request = request
        self.shop_adapter = self.get_shop_adapter(request)
        return self.additem_view_class.as_view(model_admin=self)(request, pk=object_id)

    def remove_item_bundle(self, request, object_id):
        if not self.has_add_permission(request):
            raise PermissionError(_("You don't have any permission!"))
        bundle_item = get_object_or_404(CartItemBundle, pk=object_id)
        self.delete_view
        redirect_to = reverse("admin:simpel_shop_cartitem_changelist")
        if bundle_item.user != request.user:
            messages.error(request, _("You don't have permission to delete this item!"))
            return redirect(redirect_to)
        if request.method == "POST":
            bundle_item.delete()
            messages.success(request, _("%s removed from %s!") % (bundle_item, bundle_item.cart_item))
            return redirect(redirect_to)
        else:
            context = {
                **self.admin_site.each_context(request),
                "title": _("Remove Bundle Item"),
                "subtitle": None,
                "object_name": bundle_item.product,
                "object": bundle_item,
                "deleted_objects": [],
                "delete_summary": _("This action is not reversible."),
                "opts": CartItem._meta,
                "app_label": "simpel_shop",
                "preserved_filters": self.get_preserved_filters(request),
                "is_popup": False,
            }
            return render(request, "admin/delete_confirmation.html", context=context)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["cart", "product"]
        return super().get_readonly_fields(request, obj)

    def get_bundle_queryset(self, request):
        return CartItemBundle.objects.all()

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        return super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        obj = super().save_form(request, form, change)
        cart = Cart.get_for_user(request.user)
        obj.cart = cart
        return obj

    def htmx_cartitems_table(self, request):
        cart = Cart.get_for_user(request.user)
        group = request.GET.get("group")
        if bool(group):
            group = get_object_or_404(Group, pk=group)
            items = self.shop_adapter.get_filtered_items(group.code)
            setattr(cart, "total_order", sum([item.total for item in items]))
            ctx = {"cart": cart, "items": items}
            return render(request, "admin/simpel_shop/cart_items_table.html", context=ctx)
        else:
            ctx = {"cart": cart, "items": []}
            return render(request, "admin/simpel_shop/cart_items_table.html", context=ctx)
