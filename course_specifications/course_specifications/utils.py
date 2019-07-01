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
    def get_department_id(cls, request):
        return request.session.get('department_id', 0)

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
            elif request.user.is_superuser:
                request.session['type'] = UserType.ADMIN
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
            base_url = settings.BANNER_WEBSERVICE_BASE_URL
            user = settings.BANNER_WEBSERVICE_USERNAME
            password = settings.BANNER_WEBSERVICE_PASSWORD
        else:  # api == APIType.STAFF':
            base_url = settings.STAFF_WEBSERVICE_BASE_URL
            user = settings.STAFF_WEBSERVICE_USERNAME
            password = settings.STAFF_WEBSERVICE_PASSWORD

        auth = HTTPBasicAuth(username=user, password=password) if basic_auth else None
        full_url = '{}/{}'.format(base_url, url)
        """ calling webservice """
        if settings.DEBUG:
            data = requests.get(full_url, params=parameters, auth=auth, verify=False)
        else:
            data = requests.get(full_url, params=parameters, auth=auth)
        response = data.json()['data']
        return response
    except:
        return 'ERROR'


def get_chairman_details(chairman):
    return call_web_service(url='chairman/{}'.format(chairman), api=APIType.STAFF)


def get_employee_details(employee):
    return call_web_service(url='employee/{}'.format(employee), api=APIType.STAFF)


def get_api_cached_value(cache_suffix, param, api_attribute, url, api_type):
    cache_key = param + cache_suffix
    if cache.get(cache_key) is None:
        response = call_web_service(url=url, api=api_type)

        if response and response != 'ERROR':
            cache.set(cache_key, response.get(api_attribute, 'N/A'), 24 * 60 * 60)
        else:
            cache.set(cache_key, 'N/A', 24 * 60 * 60)
    else:
        return cache.get(cache_key)


def get_full_name(user):
    return get_api_cached_value('_name', str(user), 'name_en', 'employee/{}'.format(user), APIType.STAFF)


def get_department_name(department_id):
    return get_api_cached_value('_dept', department_id, 'name', 'department/{}'.format(department_id), APIType.STAFF)
