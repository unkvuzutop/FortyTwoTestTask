from django import forms
from apps.hello.models import User


class UserEditForm(forms.ModelForm):
    photo = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta(object):
        model = User
        fields = ('name',
                  'last_name',
                  'date_of_birth',
                  'bio',
                  'email',
                  'jabber',
                  'skype',
                  'other_contacts',
                  'photo')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date',
                                                    'class': 'form-control',
                                                    'disabled': 'disabled'})
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control',
                                                 'disabled': 'disabled'}),
        self.fields['last_name'].widget.attrs.update({'class': 'form-control',
                                                      'disabled': 'disabled'}),
        self.fields['bio'].widget.attrs.update({'class': 'form-control',
                                                'disabled': 'disabled'}),
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'disabled': 'disabled'}),
        self.fields['jabber'].widget.attrs.update({'class': 'form-control',
                                                   'disabled': 'disabled'}),
        self.fields['skype'].widget.attrs.update({'class': 'form-control',
                                                  'disabled': 'disabled'}),
        self.fields['other_contacts'].widget.attrs.\
            update({'class': 'form-control',
                    'disabled': 'disabled'})
        self.fields['photo'].widget.attrs.update({'disabled': 'disabled',
                                                  'display': 'none'})

