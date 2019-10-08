import json

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
    ADWAR = 'ADWAR'


def call_web_service(url, method='get', parameters=None, data=None, basic_auth=True, api=APIType.BANNER):
    # TODO: use https://aiohttp.readthedocs.io/en/stable/ to make async calls
    try:
        if api == APIType.BANNER:
            base_url = settings.BANNER_WEBSERVICE_BASE_URL
            user = settings.BANNER_WEBSERVICE_USERNAME
            password = settings.BANNER_WEBSERVICE_PASSWORD
        elif api == APIType.STAFF:
            base_url = settings.STAFF_WEBSERVICE_BASE_URL
            user = settings.STAFF_WEBSERVICE_USERNAME
            password = settings.STAFF_WEBSERVICE_PASSWORD
        else:
            base_url = settings.ADWAR_WEBSERVICE_BASE_URL
            user = settings.ADWAR_WEBSERVICE_USERNAME
            password = settings.ADWAR_WEBSERVICE_PASSWORD

        auth = HTTPBasicAuth(username=user, password=password) if basic_auth else None
        full_url = '{}/{}'.format(base_url, url)

        """ calling webservice """
        arguments = {
            'auth': auth,
            'verify': not settings.DEBUG,
            'params': parameters,
            'data': data,
        }
        response = requests.request(method=method, url=full_url, **arguments)
        response_data = response.json().get('data')
        return response_data
    except Exception as e:
        print(e)
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


class CamundaAPI:
    process_definition_key = 'course_spicification_process'

    def __init__(self, process_instance_id):
        self.process_instance_id = process_instance_id

    def get_active_tasks(self):
        parameters = {
            'processInstanceId': self.process_instance_id
        }
        current_tasks = CamundaAPI.call_camunda_api('task', parameters=parameters)
        if current_tasks != 'ERROR':
            if current_tasks and len(current_tasks) != 1:
                raise Exception("Must be one active task in process id: {}, but {} found".format(self.process_instance_id, len(current_tasks or [])))
            return current_tasks

    def get_task_options(self, task=None):
        if not task:
            task = self.get_active_tasks()

        response = CamundaAPI.call_camunda_api('task/{task_id}/localVariables/options'.format(task_id=task['id']))
        if response != 'ERROR':
            return json.loads(response['value'])

    def complete_current_task(self, decision, task=None):
        if not task:
            task = self.get_active_tasks()

        headers = {
            'Content-Type': 'application/json',
        }

        body = {
            "variables":
                {
                    "GatewayDecision": {
                        "value": decision
                    }
                }
        }
        response = CamundaAPI.post_to_web_service('task/{task_id}/complete'.format(task_id=task['id']), json=body, headers=headers)
        return response

    @staticmethod
    def start_process(CourseCode, MaintainerTaskAssignee, ReviewerTaskAssignee, ChairmanTaskAssignee, AACTaskAssignee, isGraguateCourse):
        headers = {
            'Content-Type': 'application/json',
        }

        body = {
            "variables": {
                "CourseCode": {
                    "value": CourseCode,
                    "type": "String"
                },
                "MaintainerTaskAssignee": {
                    "value": MaintainerTaskAssignee,
                    "type": "String"
                },
                "ReviewerTaskAssignee": {
                    "value": ReviewerTaskAssignee,
                    "type": "String"
                },
                "ChairmanTaskAssignee": {
                    "value": ChairmanTaskAssignee,
                    "type": "String"
                },
                "AACTaskAssignee": {
                    "value": AACTaskAssignee,
                    "type": "String"
                },
                "GraduateCourse": {
                    "value": isGraguateCourse,
                    "type": "boolean"
                }
            }
        }

        url = 'process-definition/key/{}/start'.format(CamundaAPI.process_definition_key)
        response = CamundaAPI.post_to_web_service(url, json=body, headers=headers)
        return response.json()

    @staticmethod
    def call_camunda_api(end_point, parameters=None, basic_auth=True):
        base_url = settings.CAMUNDA_BASE_URL
        user = settings.CAMUNDA_USERNAME
        password = settings.CAMUNDA_PASSWORD

        full_url = '{}/{}'.format(base_url, end_point)
        """ calling webservice """

        try:
            auth = HTTPBasicAuth(username=user, password=password) if basic_auth else None
            if settings.DEBUG:
                data = requests.get(full_url, params=parameters, auth=auth, verify=False)
            else:
                data = requests.get(full_url, params=parameters, auth=auth)
            response = data.json()
            return response

        except Exception as err:
            return 'ERROR'

    @staticmethod
    def post_to_web_service(url, data=None, json=None, headers=None, basic_auth=True):
        try:

            base_url = settings.CAMUNDA_BASE_URL
            user = settings.CAMUNDA_USERNAME
            password = settings.CAMUNDA_PASSWORD

            auth = HTTPBasicAuth(username=user, password=password) if basic_auth else None
            full_url = '{}/{}'.format(base_url, url)
            """ calling webservice """
            if settings.DEBUG:
                response = requests.post(full_url, data=data, json=json, headers=headers, auth=auth, verify=False)
            else:
                response = requests.post(full_url, data=data, json=json, headers=headers, auth=auth)
            return response
        except:
            return 'ERROR'
