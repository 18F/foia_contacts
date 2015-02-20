import requests
import json
import time

from contact_updater.forms import AgencyData

from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound


SITE = "https://foia.18f.us/api/"


def index(request):
    r = requests.get(SITE + 'agency/')
    return render(request, "index.html", {'agencies': r.json()['objects']})


def download_data(request, slug):
    """ Converts POST request into json file ready for download """

    data = dict(request.POST)
    data['timestamp'] = int(time.time())
    del data['csrfmiddlewaretoken']
    res = HttpResponse(json.dumps(data))
    res['Content-Disposition'] = 'attachment; filename=%s.json' % slug
    return res

def get_agency_data(slug):
    """
    Given an agency slug parse through the agency API and collect agency
    info to populate agency form
    """

    r = requests.get(SITE + 'agency/%s/' % slug)
    if r.status_code == 200:
        agency_data = [r.json()]
        print(agency_data[0].keys())
        if agency_data[0].get('offices'):
            for office in agency_data[0]['offices']:
                kind = 'office/'
                if '--' not in office.get('slug'):
                    kind = 'agency/'
                r = requests.get(SITE + kind + office.get('slug') )
                agency_data.append(r.json())
        return agency_data

def prepopulate_agency(request, slug):
    """
    If GET request Collects agency and office data from foia_hub to
    populate the form. If POST request responds an attachment
    """

    AgencyFormSet = formset_factory(AgencyData)

    # I think we'll need a special endpoint for this
    # looping though multiple pages is taking too long
    agency_data = get_agency_data(slug=slug)

    if request.method == "GET":
        formset = AgencyFormSet(initial=agency_data)

    elif request.method == 'POST':
        formset = AgencyFormSet(request.POST)
        if formset.is_valid():
            return download_data(request=request, slug=slug)

    management_form = formset.management_form

    return render(
        request,
        "agency_form.html",
        {
            'data': zip(agency_data, formset),
            'management_form': management_form,
        })


