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
    def set_user_type(cls, request, user=None):
        """the user param will have a value if it is an impersonation, otherwise it will be None"""
        if user is None:
            if getattr(request.user, 'is_impersonate', False):
                user = request.impersonator
            else:
                user = request.user

        response = get_chairman_details(user)

        if response and response != 'ERROR':
            request.session['department_id'] = response.get('department_id', 0)
            request.session['type'] = UserType.CHAIRMAN
            return
        else:
            response = get_employee_details(user)
            if response and response != 'ERROR':
                if response.get('type', 0) == 'Faculty':
                    """if the faculty is_manager, then his real academic dept is the secondary_department_id"""
                    if response.get('is_manager', 0):
                        request.session['department_id'] = response.get('department_id', 0)
                    else:
                        request.session['department_id'] = response.get('secondary_department_id', 0)
                    request.session['type'] = UserType.FACULTY
                else:
                    request.session['type'] = UserType.EMPLOYEE
                return
            elif user.is_superuser:
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
    if param:
        cache_key = param + cache_suffix
        if cache.get(cache_key) is None:
            response = call_web_service(url=url, api=api_type)

            if response and response != 'ERROR':
                cache.set(cache_key, response.get(api_attribute, 'N/A'), 24 * 60 * 60)
            else:
                cache.set(cache_key, 'N/A', 24 * 60 * 60)

        return cache.get(cache_key)


def get_full_name(user):
    f_name = get_api_cached_value('_name', str(user), 'name_en', 'employee/{}'.format(user), APIType.STAFF)

    if f_name and f_name != 'N/A':
        return return_first_and_last_name(f_name)
    else:
        return str(user)


def get_department_name(department_id):
    return get_api_cached_value('_dept', department_id, 'name', 'department/{}'.format(department_id), APIType.STAFF)


def return_first_and_last_name(full_name):
    try:
        first, *middle, last = full_name.split()
        return '{} {}'.format(first, last)
    except ValueError:
        return full_name


def get_subordinates(supervisor):
    response = call_web_service(url='employee/{}/employee'.format(supervisor), api=APIType.STAFF)

    if response != 'ERROR':
        return sorted(response, key=lambda x: x['name_en'])


def get_subordinates_choices(supervisor):
    subordinates = get_subordinates(supervisor)

    if subordinates:
        return (
            (
                employee.get('username'),
                employee.get('name_en')
            ) for employee in subordinates)
    else:
        return [{'username': 'N/A', 'name_en': '', }, ]

