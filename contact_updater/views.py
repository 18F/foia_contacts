import requests

from django.shortcuts import render

SITE = "https://foia.18f.us/api/{0}/{1}/"

def prepopulate_agency(request, slug):
    r = requests.get(SITE.format('agency', slug))
    agency_data = r.json()
    office_data = []
    if agency_data.get('offices'):
        for office in agency_data['offices']:
            kind = 'office'
            if '--' not in office.get('slug'):
                kind = 'agency'
            print(SITE.format(kind, office.get('slug')))
            r = requests.get(SITE.format(kind, office.get('slug')))
            office_data.append(r.json())
    return render(
        request,
        "agency_form.html",
        {'agency_data': agency_data, 'office_data': office_data})
