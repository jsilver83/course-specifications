from course_specifications.utils import call_web_service, APIType


class CourseRoles:
    MAINTAINER = 'course_specifications_maintainer'
    REVIEWER = 'course_specifications_reviewer'


def assign_new_role(course, role, assigner, assignee, department):
    data = {
        'course_code': course,
        'role_code': role,
        'assigner': assigner,
        'assignee': assignee,
        'department': department,
    }
    return call_web_service(
        'v2/academic-roles/course/role/add',
        method='post',
        data=data,
        api=APIType.ADWAR,
    )


def assign_new_maintainer(course, assigner, assignee, department):
    return assign_new_role(course, CourseRoles.MAINTAINER, assigner, assignee, department)


def assign_new_reviewer(course, assigner, assignee, department):
    return assign_new_role(course, CourseRoles.REVIEWER, assigner, assignee, department)

