from django import forms
from apps.hello.models import Profile


class UserEditForm(forms.ModelForm):
    photo = forms.ImageField(required=False, widget=forms.FileInput)
    photo_preview = forms.ImageField(required=False)

    class Meta(object):
        model = Profile
        fields = ('name',
                  'last_name',
                  'date_of_birth',
                  'bio',
                  'email',
                  'jabber',
                  'skype',
                  'other_contacts',
                  'photo',
                  'photo_preview')
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'class': 'form-control datepicker',
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
                                                  'disabled': 'disabled',
                                                  'readonly': 'True'}),
        self.fields['jabber'].widget.attrs.update({'class': 'form-control',
                                                   'disabled': 'disabled'}),
        self.fields['skype'].widget.attrs.update({'class': 'form-control',
                                                  'disabled': 'disabled'}),
        self.fields['other_contacts'].widget.attrs.\
            update({'class': 'form-control',
                    'disabled': 'disabled'})
        self.fields['photo'].widget.attrs.update({'disabled': 'disabled',
                                                  'display': 'none',
                                                  'title': 'Upload file...'})
