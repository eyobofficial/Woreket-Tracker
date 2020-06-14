from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from shared.constants import ROLE_ADMIN, ROLE_MANAGEMENT, ROLE_STAFF, \
    ROLE_SUPPLIER, ROLE_GUEST
from purchases.models import Supplier


User = get_user_model()


class UserForm(forms.ModelForm):
    role = forms.ModelChoiceField(
        queryset=Group.objects.filter(
            name__in=[
                ROLE_ADMIN, ROLE_MANAGEMENT,
                ROLE_STAFF, ROLE_SUPPLIER, ROLE_GUEST
            ]
        ),
        required=True, empty_label=None
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        required=False, empty_label=None
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'role', 'supplier')

    def save(self, commit=True):
        role = self.cleaned_data['role']

        user = super().save(commit)
        user.groups.clear()
        user.groups.add(role)

        if user.role.name != ROLE_SUPPLIER:
            user.supplier = None
            user.save()

        return user
