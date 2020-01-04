from django import forms

from media.models import StatusPost
from account.models import Account


class CreateStatusPostForm(forms.ModelForm):

    class Meta:
        model = StatusPost
        fields = ['text', 'image']


class EditProfileForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = [
            'full_name', 
            'date_of_birth', 
            'profile_picture', 
            'banner_picture', 
            'residency',
            'about'
        ]


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        # Later add password
        fields = ['email', 'username', ]

    def cleanEmail(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError("Email %s is already in use" % email)

    def cleanUsername(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError("Username %s is already in use" % username)