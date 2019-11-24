import json

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from requests.auth import HTTPBasicAuth


# constants required for figuring out the user type
AAC_HEAD_ADWAR_ROLE_CODE = 'AAC_Head'
DGS_DEPARTMENT_ID = 113
VICE_RECTOR_ACADEMICS_JOB_TITLE_ID = 40983
RECTOR_JOB_TITLE_ID = 41034


class UserType:
    CHAIRMAN = 'CHAIRMAN'
    DEAN = 'DEAN'
    FACULTY = 'FACULTY'
    AAC_HEAD = 'AAC_HEAD'
    DGS_DEAN = 'DGS_DEAN'
    VICE_RECTOR_ACADEMICS = 'VICE_RECTOR_ACADEMICS'
    RECTOR = 'RECTOR'
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

        chairman = get_chairman_details(user)
        if chairman:
            request.session['department_id'] = chairman.get('department_id', 0)
            request.session['type'] = UserType.CHAIRMAN
            return

        dean = get_dean_details(user)
        if dean:
            request.session['type'] = UserType.DEAN
            return

        rector = get_rector_username()
        if user.username == rector:
            request.session['type'] = UserType.RECTOR
            return

        vice_rector_academics = get_vice_rector_academics_username()
        if user.username == vice_rector_academics:
            request.session['type'] = UserType.VICE_RECTOR_ACADEMICS
            return

        dgs_dean = get_dgs_dean_username()
        if user.username == dgs_dean:
            request.session['type'] = UserType.DGS_DEAN
            return

        aac_head = get_aac_head_username()
        if user.username == aac_head:
            request.session['type'] = UserType.AAC_HEAD
            return

        employee_details = get_employee_details(user)
        if employee_details:
            if employee_details.get('type', 0) == 'Faculty':
                """if the faculty is_manager, then his real academic dept is the secondary_department_id"""
                if employee_details.get('is_manager', 0):
                    request.session['department_id'] = employee_details.get('department_id', 0)
                else:
                    request.session['department_id'] = employee_details.get('secondary_department_id', 0)
                request.session['type'] = UserType.FACULTY
            else:
                request.session['type'] = UserType.EMPLOYEE
            return

        if user.is_superuser:
            request.session['type'] = UserType.ADMIN
            return
        else:
            request.session['type'] = UserType.NONE
            return


class APIType:
    BANNER = 'BANNER'
    STAFF = 'STAFF'
    ADWAR = 'ADWAR'


def call_web_service(url, method='get', parameters=None, data=None, basic_auth=True, api=APIType.BANNER,
                     cache_duration=settings.DEFAULT_CACHE_DURATION_WEBSERVICES):
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

    full_url = '{}/{}'.format(base_url, url)

    if cache.get(full_url) and method == 'get':
        return cache.get(full_url)
    else:
        try:
            auth = HTTPBasicAuth(username=user, password=password) if basic_auth else None

            """ calling webservice """
            arguments = {
                'auth': auth,
                'verify': not settings.DEBUG,
                'params': parameters,
                'data': data,
            }
            response = requests.request(method=method, url=full_url, **arguments)
            response_data = response.json().get('data')
        except Exception as e:
            print(e)
            response_data = False

        if response_data and method == 'get':  # Only cache a valid response and only if the request is a GET
            cache.set(full_url, response_data, cache_duration)

        return response_data


def get_chairman_details(chairman):
    return call_web_service(url='chairman/{}'.format(chairman), api=APIType.STAFF)


def get_dean_details(dean):
    return call_web_service(url='dean/{}'.format(dean), api=APIType.STAFF)


def get_aac_head_details():
    return call_web_service('academic-roles?role_code={}'.format(AAC_HEAD_ADWAR_ROLE_CODE), api=APIType.ADWAR)


def get_aac_head_username():
    aac_heads = get_aac_head_details()
    if aac_heads:
        return aac_heads[0].get('assignee')


def get_dgs_dean_details():
    return call_web_service(url='v2/department/{}'.format(DGS_DEPARTMENT_ID), api=APIType.STAFF)


def get_dgs_dean_username():
    dgs_dean = get_dgs_dean_details()
    if dgs_dean:
        return dgs_dean.get('username')


def get_vice_rector_academics_details():
    return call_web_service(url='employee?job_title_id={}'.format(VICE_RECTOR_ACADEMICS_JOB_TITLE_ID),
                            api=APIType.STAFF)


def get_vice_rector_academics_username():
    vice_rector_academics = get_vice_rector_academics_details()
    if vice_rector_academics:
        return vice_rector_academics[0].get('username')


def get_rector_details():
    return call_web_service(url='employee?job_title_id={}'.format(RECTOR_JOB_TITLE_ID), api=APIType.STAFF)


def get_rector_username():
    rector = get_rector_details()
    if rector:
        return rector[0].get('username')


def get_employee_details(employee):
    return call_web_service(url='employee/{}'.format(employee), api=APIType.STAFF)


def get_full_name(user):
    f_name = 'N/A'

    if get_employee_details(str(user)):
        f_name = get_employee_details(str(user)).get('name_en')

    if f_name != 'N/A':
        return get_first_and_last_name(f_name)
    else:
        return str(user)


def get_department_details(department_id):
    return call_web_service(url='department/{}'.format(department_id), api=APIType.STAFF)


def get_department_name(department_id):
    if get_department_details(department_id):
        return get_department_details(department_id).get('name')


def get_first_and_last_name(full_name):
    try:
        first, *middle, last = full_name.split()
        return '{} {}'.format(first, last)
    except ValueError:
        return full_name


def get_short_full_name(user):
    return get_first_and_last_name(get_full_name(user))


def get_subordinates(supervisor):
    response = call_web_service(url='employee/{}/employee'.format(supervisor), api=APIType.STAFF)

    if response:
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
    class TaskTypes:
        MAINTAINER = 'Maintainer_Task'
        REVIEWER = 'Reviewer_Task'
        CHAIRMAN = 'Chairman_Task'
        ACC_HEAD = 'ACC_Task'
        COLLAGE_DEAN = 'Collage_Dean_Task'
        DGS_DEAN = 'DGS_Dean_Task'
        VICE_RECTOR_ACADEMICS = 'Vice_Rector_Task'
        RECTOR = 'Rector_Task'

        @classmethod
        def all(cls):
            return [
                cls.MAINTAINER,
                cls.REVIEWER,
                cls.CHAIRMAN,
                cls.ACC_HEAD,
                cls.COLLAGE_DEAN,
                cls.DGS_DEAN,
                cls.VICE_RECTOR_ACADEMICS,
                cls.RECTOR,
            ]

        @classmethod
        def user_task_types_map(cls):
            return (
                (UserType.CHAIRMAN, cls.CHAIRMAN),
                (UserType.AAC_HEAD, cls.ACC_HEAD),
                (UserType.DEAN, cls.COLLAGE_DEAN),
                (UserType.DGS_DEAN, cls.DGS_DEAN),
                (UserType.VICE_RECTOR_ACADEMICS, cls.VICE_RECTOR_ACADEMICS),
                (UserType.RECTOR, cls.RECTOR),
            )

        @classmethod
        def choices(cls):
            return (
                (cls.MAINTAINER, _('Maintainer Task')),
                (cls.REVIEWER, _('Reviewer Task')),
                (cls.CHAIRMAN, _('Chairman Task')),
                (cls.ACC_HEAD, _('ACC Task')),
                (cls.COLLAGE_DEAN, _('Collage Dean Task')),
                (cls.DGS_DEAN, _('DGS Dean Task')),
                (cls.VICE_RECTOR_ACADEMICS, _('Vice Rector For Academic Affairs Task')),
                (cls.RECTOR, _('Rector Task')),
            )

    PROCESS_DEFINITION_KEY = 'course_spicification_process'

    def __init__(self, process_instance_id):
        self.process_instance_id = process_instance_id

    def get_active_task(self):
        parameters = {
            'processInstanceId': self.process_instance_id
        }
        current_tasks = CamundaAPI.call_camunda_api('task?processInstanceId={}'.format(self.process_instance_id))
        if current_tasks != 'ERROR':
            if current_tasks and len(current_tasks) != 1:
                raise Exception("Must be one active task in process id: {}, but {} found".format(self.process_instance_id, len(current_tasks or [])))
            return current_tasks[0]

    def get_task_options(self, task=None):
        if not task:
            task = self.get_active_task()

        response = CamundaAPI.call_camunda_api('task/{task_id}/localVariables/options'.format(task_id=task['id']))
        if response != 'ERROR':
            return json.loads(response['value'])

    def complete_current_task(self, decision=None, task=None):
        if not task:
            task = self.get_active_task()

        headers = {
            'Content-Type': 'application/json',
        }

        if decision:
            body = {
                "variables":
                    {
                        "GatewayDecision": {
                            "value": decision
                        }
                    }
            }
        else:
            body=None

        response = CamundaAPI.post_to_web_service('task/{task_id}/complete'.format(task_id=task['id']), json=body, headers=headers)
        return response

    def is_process_completed(self):
        response = CamundaAPI.call_camunda_api('history/process-instance/{}'.format(self.process_instance_id))
        if response != 'ERROR':
            return response['state']=='COMPLETED'

    @staticmethod
    def start_process(course_code, course_history_id, AAC_task_assignee, is_graduate_course, department_id, college_id):
        headers = {
            'Content-Type': 'application/json',
        }

        body = {
            "variables": {
                "CourseCode": {
                    "value": course_code,
                    "type": "String"
                },
                "CourseHistoryId": {
                    "value": course_history_id,
                    "type": "Integer"
                },
                "AACTaskAssignee": {
                    "value": AAC_task_assignee,
                    "type": "String"
                },
                "GraduateCourse": {
                    "value": is_graduate_course,
                    "type": "boolean"
                },
                "DepartmentId": {
                    "value": department_id,
                    "type": "String"
                },
                "CollegeId": {
                    "value": college_id,
                    "type": "String"
                },
            }
        }

        url = 'process-definition/key/{}/start'.format(CamundaAPI.PROCESS_DEFINITION_KEY)
        response = CamundaAPI.post_to_web_service(url, json=body, headers=headers)
        return response.json()

    @staticmethod
    def get_role_tasks(task_name, college_id=None, department_id=None, course_code=None):
        if task_name not in CamundaAPI.TaskTypes.all():
            raise ValueError('task name passed \'{}\' is not valid'.format(task_name))

        headers = {
            'Content-Type': 'application/json',
        }

        body = {
            "processDefinitionKey": CamundaAPI.PROCESS_DEFINITION_KEY,
            "taskDefinitionKey": task_name,
            "processVariables": []
        }
        if college_id:
            body['processVariables'].append({
                "name": "CollegeId",
                "value": college_id,
                "operator": "eq"
            })

        if department_id:
            body['processVariables'].append({
                "name": "DepartmentId",
                "value": department_id,
                "operator": "eq"
            })

        if course_code:
            body['processVariables'].append({
                "name": "CourseCode",
                "value": course_code,
                "operator": "eq"
            })

        url = 'task'
        response = CamundaAPI.post_to_web_service(url, json=body, headers=headers)
        return response.json()

    @staticmethod
    def call_camunda_api(end_point, parameters=None, basic_auth=True):
        base_url = settings.CAMUNDA_BASE_URL
        user = settings.CAMUNDA_USERNAME
        password = settings.CAMUNDA_PASSWORD

        full_url = '{}/{}'.format(base_url, end_point)
        print(full_url)
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


def list_to_comma_separated_values(my_list):
    return ','.join(map(str, my_list))
