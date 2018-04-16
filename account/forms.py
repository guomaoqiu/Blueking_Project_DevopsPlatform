# -*- coding: utf-8 -*-
"""BK user form."""
from django import forms

from account.models import BkUser


class BkUserCreationForm(forms.ModelForm):
    """A form that creates a user, with no privileges"""
    class Meta:
        model = BkUser
        fields = ("username",)

    def save(self, commit=True):
        user = super(BkUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class BkUserChangeForm(forms.ModelForm):
    """A form for updating users.

    Includes all the fields onthe user,
    """
    class Meta:
        model = BkUser
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super(BkUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
