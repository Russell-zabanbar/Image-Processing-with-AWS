from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class CardSelectionForm(forms.Form):
    card_number = forms.ChoiceField(choices=[(1, 'کارت 1'), (2, 'کارت 2'), (3, 'کارت 3')], widget=forms.RadioSelect())
