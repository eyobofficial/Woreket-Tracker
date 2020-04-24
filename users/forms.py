from django import forms
from django.contrib.auth import get_user_model

from shared.constants import ROLE_SUPPLIER


User = get_user_model()


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'role', 'supplier')

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.role.name != ROLE_SUPPLIER:
            user.supplier = None

        return super().save(commit)
