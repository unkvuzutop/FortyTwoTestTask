from django import forms
from apps.hello.models import Profile


class ReadOnlyFieldsMixin(object):
    readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        for field in (field for name, field in self.fields.iteritems()
                      if name in self.readonly_fields):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        cleaned_data = super(ReadOnlyFieldsMixin, self).clean()
        for field in self.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)

        return cleaned_data


class UserEditForm(ReadOnlyFieldsMixin, forms.ModelForm):
    photo = forms.ImageField(required=False, widget=forms.FileInput)
    photo_preview = forms.ImageField(required=False)
    readonly_fields = ('email',)

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
                attrs={'class': 'form-control datepicker'})
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'}),
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control'}),
        self.fields['bio'].widget.attrs.update({'class': 'form-control'}),
        self.fields['email'].widget.attrs.update({'class': 'form-control',
                                                  'readonly': 'True'}),
        self.fields['jabber'].widget.attrs.update({'class': 'form-control'}),
        self.fields['skype'].widget.attrs.update({'class': 'form-control'}),
        self.fields['other_contacts'].widget.attrs.\
            update({'class': 'form-control'})
        self.fields['photo'].widget.attrs.update({'display': 'none',
                                                  'title': 'Upload file...'})
