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

def get_first_array(array):
    """ Given a list returns first element """

    if array:
        return array[0]

def unpack_libraries(libraries):
    """ Given a list of libraries returns url """

    if libraries:
        return libraries[0].get('url')

def join_array(array):
    """ Joins array feilds using `\n` """
    if array:
        return "\n".join(array)

def transform_data(data):
    """ Returns only first email """

    data['emails'] = get_first_array(data.get('emails'))
    data['foia_libraries'] = unpack_libraries(data.get('foia_libraries'))
    data['common_requests'] = join_array(data.get('common_requests'))
    data['no_records_about'] = join_array(data.get('no_records_about'))
    data['address_lines'] = join_array(data.get('address_lines'))
    # data['person_name'] = data.get('person_name', '').replace('Phone: ', '')

    return data

def get_agency_data(slug):
    """
    Given an agency slug parse through the agency API and collect agency
    info to populate agency form
    """

    r = requests.get(SITE + 'agency/%s/' % slug)
    if r.status_code == 200:
        agency_data = [transform_data(r.json())]
        if agency_data[0].get('offices'):
            for office in agency_data[0]['offices']:
                kind = 'office/'
                if '--' not in office.get('slug'):
                    kind = 'agency/'
                r = requests.get(SITE + kind + office.get('slug') )
                agency_data.append(transform_data(r.json()))
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


