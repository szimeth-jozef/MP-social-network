from django import forms

from media.models import StatusPost


class CreateStatusPostForm(forms.ModelForm):

    class Meta:
        model = StatusPost
        fields = ['text', 'image']