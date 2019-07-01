import requests
from django.conf import settings
from django.core.cache import cache
from requests.auth import HTTPBasicAuth


class UserType:
    CHAIRMAN = 'CHAIRMAN'
    FACULTY = 'FACULTY'
    EMPLOYEE = 'EMPLOYEE'
    ADMIN = 'ADMIN'
    NONE = 'NONE'

    @classmethod
    def get_user_type(cls, request):
        return request.session.get('type', cls.NONE)

    @classmethod
    def set_user_type(cls, request):
        response = get_chairman_details(request.user)

        if response and response != 'ERROR':
            request.session['department_id'] = response.get('department_id', 0)
            request.session['type'] = UserType.CHAIRMAN
            return
        else:
            response = get_employee_details(request.user)
            if response and response != 'ERROR':
                request.session['department_id'] = response.get('department_id', 0)
                if response.get('type', 0) == 'Faculty':
                    request.session['type'] = UserType.FACULTY
                else:
                    request.session['type'] = UserType.EMPLOYEE
                return
            else:
                request.session['type'] = UserType.NONE
                return


class APIType:
    BANNER = 'BANNER'
    STAFF = 'STAFF'


def call_web_service(url, parameters=None, basic_auth=True, api=APIType.BANNER):
    try:
        if api == APIType.BANNER:
            user = settings.BANNER_WEBSERVICE_USERNAME
            password = settings.BANNER_WEBSERVICE_PASSWORD
        else:  # api == APIType.STAFF':
            user = settings.STAFF_WEBSERVICE_USERNAME
            password = settings.STAFF_WEBSERVICE_PASSWORD

        auth = HTTPBasicAuth(username=user, password=password) if basic_auth else None
        """ calling webservice """
        if settings.DEBUG:
            data = requests.get(url, params=parameters, auth=auth, verify=False)
        else:
            data = requests.get(url, params=parameters, auth=auth)
        response = data.json()['data']
        return response
    except:
        return 'ERROR'


def get_chairman_details(chairman):
    return call_web_service(url='%s/chairman/%s' % (settings.STAFF_WEBSERVICE_BASE_URL, chairman),
                            api=APIType.STAFF)


def get_employee_details(employee):
    return call_web_service(url='%s/employee/%s' % (settings.STAFF_WEBSERVICE_BASE_URL, employee),
                            api=APIType.STAFF)


def get_full_name(user):
    user = str(user)
    if cache.get(user + '_name') is None:
        response = call_web_service(url='%s/employee/%s' % (settings.STAFF_WEBSERVICE_BASE_URL, user),
                                    api=APIType.STAFF)

        if response and response != 'ERROR':
            cache.set(user + '_name', response.get('name_en', user), 24 * 60 * 60)
        else:
            cache.set(user + '_name', user, 24 * 60 * 60)
    else:
        return cache.get(user + '_name')
