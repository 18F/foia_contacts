import requests
import json

from django.shortcuts import render
from django.http import HttpResponse

SITE = "https://foia.18f.us/api/{0}/{1}/"


def download_data(request, slug):
    """ Converts POST request into json file ready for download """
    data = dict(request.POST)
    print(data)
    del data['csrfmiddlewaretoken']
    res = HttpResponse(json.dumps(data))
    res['Content-Disposition'] = 'attachment; filename=%s.json' % slug
    return res


def prepopulate_agency(request, slug):
    """
    If GET request Collects agency and office data from foia_hub to
    populate the form. If POST request responds an attachment
    """

    if request.method == 'POST':
        return download_data(request=request, slug=slug)
    r = requests.get(SITE.format('agency', slug))
    agency_data = r.json()
    office_data = []
    if agency_data.get('offices'):
        for office in agency_data['offices']:
            kind = 'office'
            if '--' not in office.get('slug'):
                kind = 'agency'
            r = requests.get(SITE.format(kind, office.get('slug')))
            office_data.append(r.json())
    return render(
        request,
        "agency_form.html",
        {'agency_data': agency_data, 'office_data': office_data})
