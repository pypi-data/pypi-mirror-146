from django import forms

# from simpel_payments.models import PaymentGateway
from django.contrib import admin
from django.contrib.admin.widgets import AutocompleteSelect
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django_select2.forms import Select2Widget

from simpel_products.models import Group, Product
from simpel_sales.settings import sales_settings

from .models import Cart, CartItem, CartItemBundle

CustomerModel = sales_settings.CUSTOMER_MODEL


# class CustomerSelectWidget(Select2Widget):
#     template_name = "admin/simpel_shop/customer_select.html"

# autocomplete = Select2Widget(
#         attrs={"class": "admin-autocomplete w-100", "data-theme": "bootstrap-5"},
#     )


class AdminCustomerSelect(AutocompleteSelect):
    pass


class CheckoutForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields["group"] = forms.ModelChoiceField(
            required=False,
            widget=forms.Select(),
            queryset=Group.objects.all(),
        )
        if self.request.user.is_staff or self.request.user.is_superuser:
            self.fields["customer"] = forms.ModelChoiceField(
                required=True,
                queryset=CustomerModel.objects.filter(is_active=True),
                widget=Select2Widget(attrs={"class": "admin-autocomplete"}),
            )
        self.fields["reference"] = forms.CharField(required=False)

        self.fields["note"] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={"rows": 4}),
        )

    def clean_group(self):
        data = self.cleaned_data["group"]
        cart = Cart.get_for_user(self.request.user)
        if not cart.items.filter(product__group=data).exists():
            raise forms.ValidationError(_("Please add at least one product in your cart"))
        return data

    def clean_customer(self):
        data = self.cleaned_data["customer"]
        return data


class CheckoutWizzardCustomerSelectForm(forms.Form):
    use_mine = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    customer = forms.ModelChoiceField(
        queryset=CustomerModel.objects.filter(is_active=True),
        required=False,
    )

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_partner = getattr(request.user, "partner", None)

    def clean_customer(self):
        data = self.cleaned_data["customer"]
        mine = self.cleaned_data["use_mine"]
        if mine and self.user_partner is not None:
            data = self.user_partner
        elif data is None:
            raise ValidationError(_("Please select a customer!"))
        return data


class CheckoutWizzardAddressSelectForm(forms.Form):
    def __init__(self, customer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["billing_address"] = forms.ModelChoiceField(
            queryset=customer.addresses.all(),
            help_text=_("My available address."),
            required=True,
        )
        self.fields["shipping_address"] = forms.ModelChoiceField(
            queryset=customer.addresses.all(),
            help_text=_("My available address."),
            required=True,
        )
        self.fields["note"] = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={"rows": 3}),
            help_text=_("Tell us anything we should know when delivering your order."),
        )


class CheckoutWizzardPaymentSelectForm(forms.Form):
    # TODO Attach Payment Backend
    # payment = forms.ModelChoiceField(
    #     queryset=PaymentGateway.objects.all(),
    #     required=True,
    #     widget=forms.RadioSelect(),
    # )
    # def __init__(self, *args, **kwargs):
    #     return
    pass


class CheckoutWizzardConfirmForm(forms.Form):
    confirm = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=True,
    )


class AddItemForm(forms.Form):
    name = forms.CharField(
        required=False,
        help_text=_("Give your cart item name."),
    )
    note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 4}),
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        super().__init__(*args, **kwargs)
        self.fields["quantity"] = forms.IntegerField(
            min_value=self.instance.min_order,
            max_value=self.instance.max_order,
            help_text=_("Quantity limit %s - %s") % (self.instance.min_order, self.instance.max_order),
        )
        self.fields["bundles"] = forms.ModelMultipleChoiceField(
            queryset=self.instance.recommended_items.all(),
            required=False,
        )


class CartItemModelForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = (
            "name",
            "quantity",
            "note",
        )


class CartItemRecommendedBundleForm(forms.ModelForm):
    class Meta:
        model = CartItemBundle
        fields = ("cart_item", "product")
        widgets = {"cart_item": forms.HiddenInput()}

    def __ini__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"] = forms.ModelMultipleChoiceField(
            queryset=self.instance.recommended_items.all(),
            required=False,
        )


class CartItemBundleForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(bundle=True),
        label=_("Bundle/Parameter"),
        widget=AutocompleteSelect(admin_site=admin.site, field=CartItemBundle._meta.get_field("product")),
    )

    class Meta:
        model = CartItemBundle
        fields = ("cart_item", "product")
        widgets = {"cart_item": forms.HiddenInput()}

    def __ini__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["product"] = forms.ModelMultipleChoiceField(
            queryset=self.instance.recomended_bundles.all(),
            required=False,
        )
