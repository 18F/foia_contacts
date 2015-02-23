from django import forms


class AgencyData(forms.Form):
    description = forms.CharField(required=False, widget=forms.Textarea)
    public_liaison_email = forms.EmailField(required=False)
    emails = forms.CharField(required=False)
    phone = forms.RegexField(
        required=False,
        regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
        error_message=("Must contain a valid phone number"))
    toll_free_phone = forms.RegexField(
        required=False,
        regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
        error_message=("Must contain a valid phone number"))
    public_liaison_phone = forms.RegexField(
        required=False,
        regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
        error_message=("Must contain a valid phone number"))
    request_form_url = forms.URLField(required=False)
    # Will need to reformat the value
    foia_libraries = forms.CharField(required=False)
    address_lines = forms.CharField(required=False, widget=forms.Textarea)
    street = forms.CharField(required=False)
    state = forms.CharField(required=False)
    city = forms.CharField(required=False)
    zip_code = forms.CharField(required=False)
    office_url = forms.URLField(required=False)
    common_requests = forms.CharField(required=False, widget=forms.Textarea)
    no_records_about = forms.CharField(required=False, widget=forms.Textarea)
    # person_name = forms.CharField(required=False)
    public_liaison_name = forms.CharField(required=False)
    fax = forms.RegexField(
        required=False,
        regex=r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$',
        error_message=("Must contain a valid phone number"))
