from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView, View

from formtools.wizard.views import SessionWizardView
from simpel_products.models import Product

from simpel_shop.forms import (
    CheckoutWizzardAddressSelectForm, CheckoutWizzardConfirmForm, CheckoutWizzardCustomerSelectForm,
    CheckoutWizzardPaymentSelectForm,
)
from simpel_shop.models import Cart

from .settings import shop_settings


class AddItemView(View):
    def get_success_url(self):
        raise NotImplementedError(
            _("%s must implement get_success_url()") % self.__class__.__name__,
        )

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.shop_adapter = self.get_shop_adapter(request)
        self.shop_adapter.add_item(product)
        messages.success(request, _("%s added to cart."))
        return redirect(self.get_success_url())

    def get_shop_adapter(self, request):
        return self.shop_adapter_class(request)


class AddItemFormView(FormView):
    template_name = "admin/simpel_shop/cart_add_item.html"
    shop_adapter_class = shop_settings.ADAPTER_CLASS
    form_class = shop_settings.SHOP_ADMIN_ADDITEM_FORM

    def get_form_class(self):
        return self.form_class

    def dispatch(self, request, pk, *args, **kwargs):
        self.request = request
        self.product = get_object_or_404(Product, pk=pk)
        self.cart = Cart.get_for_user(request.user)
        self.shop_adapter = self.get_shop_adapter(request)
        return super().dispatch(request, pk, *args, **kwargs)

    def get_success_url(self):
        raise NotImplementedError(
            _("%s must implement get_success_url()") % self.__class__.__name__,
        )

    def get_cancel_url(self):
        raise NotImplementedError(
            _("%s must implement get_cancel_url()") % self.__class__.__name__,
        )

    def get_shop_adapter(self, request):
        return self.shop_adapter_class(request)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["instance"] = self.product
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cancel_url"] = self.get_cancel_url
        context["title"] = _("Add %s") % self.product
        context["product"] = self.product
        context["cart"] = self.cart
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        self.shop_adapter.add_item(self.product, **data)
        return super().form_valid(form)


class SimpleCheckoutView(FormView):
    template_name = "admin/simpel_shop/checkout.html"
    shop_adapter_class = shop_settings.ADAPTER_CLASS

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        if self.has_permissions():
            messages.error(self.request, _("You don't have any permissions!"))
            return redirect(reverse("admin:admin_profile"))
        self.shop_adapter = self.get_shop_adapter(request)
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return self.checkout_template

    def get_shop_adapter(self, request):
        return self.shop_adapter_class(request)


def customer_selection_condition(wizzard):
    user = wizzard.request.user
    return user.is_staff or user.is_superadmin


class CheckoutWizzardView(SessionWizardView):
    condition_dict = {
        "customer_select": customer_selection_condition,
    }
    form_list = [
        ("customer_select", CheckoutWizzardCustomerSelectForm),
        ("address_select", CheckoutWizzardAddressSelectForm),
        ("payment_select", CheckoutWizzardPaymentSelectForm),
        ("confirm", CheckoutWizzardConfirmForm),
    ]
    template_name = "admin/simpel_shop/checkout_wizzard.html"
    template_names = {
        "customer_select": template_name,
        "address_select": template_name,
        "payment_select": template_name,
        "confirm": template_name,
    }
    shop_adapter_class = shop_settings.ADAPTER_CLASS

    def has_permissions(self):
        return True

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        if not self.has_permissions():
            messages.error(self.request, _("You don't have any permissions!"))
            return redirect(self.get_redirect_url())
        self.cart = Cart.get_for_user(request.user)
        if not self.cart.items.count():
            messages.error(request, _("Your cart is empty, please add a product or service!"))
            return redirect(self.get_redirect_url())
        self.shop_adapter = self.get_shop_adapter(request)
        return super().dispatch(request, *args, **kwargs)

    def get_shop_adapter(self, request):
        return self.shop_adapter_class(request)

    def get_template_names(self):
        return self.template_names[self.steps.current]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context.update(
            {
                "title": _("Checkout Step %s ") % self.steps.step1,
                "subtitle": self.steps.current.replace("_", " "),
            }
        )
        if self.steps.current == "customer_select":
            context.update(
                {
                    "subtitle": _("Customer Information"),
                    "description": _("You can select customer or use your own customer account."),
                }
            )
        elif self.steps.current == "address_select":
            context.update({"subtitle": _("Billing and Shipping")})
        elif self.steps.current == "payment_select":
            context.update({"subtitle": _("Payment Method")})
        elif self.steps.current == "confirm":
            context.update({"subtitle": _("Confirm Order")})
        return context

    def get_form_kwargs(self, step=None):
        init_kwargs = dict()
        if step == "customer_select":
            init_kwargs.update(
                {
                    "customer_select": {
                        "request": self.request,
                    }
                }
            )
        if step == "address_select":
            cs_step = "customer_select"
            try:
                form = self.get_form(cs_step, self.storage.get_step_data(cs_step))
                form.is_valid()
                customer = form.cleaned_data.get("customer", None)
            except Exception:
                customer = None
            if customer is None:
                customer = self.request.user.partner
            init_kwargs.update(
                {
                    "address_select": {
                        "customer": customer,
                    }
                }
            )
        return init_kwargs.get(step, dict())

    def get_success_url(self):
        raise NotImplementedError(_("%s must implement get_success_url()") % self.__class__.__name__)

    def get_redirect_url(self):
        raise NotImplementedError(_("%s must implement get_redirect_url()") % self.__class__.__name__)

    def done(self, form_list, form_dict, **kwargs):
        customer_form = form_dict.get("customer_select", None)
        customer = getattr(self.request.user, "partner", self.request.user)
        if customer_form:
            customer_data = customer_form.cleaned_data["customer"]
            if customer_form.cleaned_data["customer"]:
                customer = customer_data
        address = form_dict.get("address_select", None)
        data = {"customer": customer}
        items = self.shop_adapter.get_filtered_items()
        handler = self.shop_adapter.get_checkout_handler("create_salesorder")
        self.instance = handler(
            self.request,
            data=data,
            items=items,
            billing=address.cleaned_data["billing_address"],
            shipping=address.cleaned_data["shipping_address"],
            delete_item=True,
            from_cart=True,
        )
        return redirect(self.get_success_url())

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
