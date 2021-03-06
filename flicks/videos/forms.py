from django import forms
from django.core.exceptions import ValidationError

import waffle
from tower import ugettext_lazy as _lazy

from flicks.base.regions import region_names
from flicks.videos.models import Video
from flicks.videos.search import AUTOCOMPLETE_FIELDS, search_videos


class VideoForm(forms.ModelForm):
    filesize = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Video
        fields = ('title', 'description', 'filename')
        widgets = {
            'title': forms.TextInput(attrs={'required': 'required'}),
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'filename': forms.HiddenInput
        }


class VideoSearchForm(forms.Form):
    """Form for the search feature on the video listing page."""
    FIELD_CHOICES = [(value, '') for value in AUTOCOMPLETE_FIELDS.keys()]
    REGION_CHOICES = [('', _lazy('All regions'))] + region_names.items()
    SORT_CHOICES = [
        # L10n: Label for the order in which to sort a list of videos.
        ('', _lazy('Random')),
        # L10n: Label for the order in which to sort a list of videos.
        ('title', _lazy('by Title')),
    ]

    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'type': 'search',
            'autocomplete': 'off'
        }))
    region = forms.TypedChoiceField(
        required=False,
        choices=REGION_CHOICES,
        coerce=int,
        empty_value='')
    sort = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES)
    field = forms.ChoiceField(
        required=False,
        choices=FIELD_CHOICES,
        widget=forms.HiddenInput)

    region_names = dict(REGION_CHOICES)

    def __init__(self, request, *args, **kwargs):
        super(VideoSearchForm, self).__init__(*args, **kwargs)

        # Only make popular option available if voting hasn't ended.
        if not waffle.flag_is_active(request, 'voting-end'):

            # L10n: Label for the order in which to sort a list of videos.
            self.fields['sort'].choices += [('popular', _lazy('by Popularity'))]

    def clean(self):
        super(VideoSearchForm, self).clean()

        # If the user is performing a search, remove the random sorting option.
        if self.cleaned_data['query']:
            sort = self.fields['sort']
            sort.choices = filter(lambda choice: choice[0] != '', sort.choices)
            self.cleaned_data['sort'] = self.cleaned_data.get('sort') or 'title'

        return self.cleaned_data

    def perform_search(self):
        """
        Perform a search using the parameters bound to this form.

        :throws ValidationError: If the form doesn't pass validation.
        """
        if not self.is_valid():
            raise ValidationError('Form must be valid to perform search.')

        return search_videos(
            query=self.cleaned_data['query'],
            fields=AUTOCOMPLETE_FIELDS.get(self.cleaned_data['field'], None),
            region=self.cleaned_data['region'],
            sort=self.cleaned_data['sort'],
        )
