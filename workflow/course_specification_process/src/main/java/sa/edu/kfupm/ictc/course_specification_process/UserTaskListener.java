package sa.edu.kfupm.ictc.course_specification_process;

import com.mashape.unirest.http.exceptions.UnirestException;
import org.camunda.bpm.engine.delegate.DelegateTask;
import org.camunda.bpm.engine.delegate.TaskListener;
import org.json.JSONArray;
import org.json.JSONObject;
import sa.edu.kfupm.ictc.course_specification_process.utils.PropertiesHelper;
import sa.edu.kfupm.ictc.course_specification_process.utils.api.AdwarApi;
import sa.edu.kfupm.ictc.course_specification_process.utils.api.StaffApi;

import java.util.Properties;
import java.util.logging.Logger;

public class UserTaskListener implements TaskListener {

    private final static Logger LOGGER = Logger.getLogger("course_specification_process");

    public void notify(DelegateTask delegateTask) {
        assignUser(delegateTask);
    }

    private void assignUser(DelegateTask delegateTask) {
        AdwarApi adwarApi = AdwarApi.getInstance();
        StaffApi staffApi = StaffApi.getInstance();

        String courseCode = delegateTask.getVariable("CourseCode") + "";
        String departmentId = delegateTask.getVariable("DepartmentId") + "";
        String collegeId = delegateTask.getVariable("CollegeId") + "";

        PropertiesHelper propertiesInstance = PropertiesHelper.getInstance();
        Properties properties = propertiesInstance.getProperties();

        String dgs_department_id = properties.getProperty("DGS_DEPARTMENT_ID");

        String vice_rector_job_title_id = properties.getProperty("VICE_RECTOR_JOB_TITLE_ID");
        String rector_job_title_id = properties.getProperty("RECTOR_JOB_TITLE_ID");

        if (PropertiesHelper.isDebug()) {
            LOGGER.info("TaskDefinitionKey ===============================");
            LOGGER.info(delegateTask.getTaskDefinitionKey());
        }

        try {
            switch (delegateTask.getTaskDefinitionKey()) {
                case "Maintainer_Task":
                    JSONObject maintainer = adwarApi.getCourseMaintainerRole(courseCode);
                    if (maintainer != null) {
                        delegateTask.setAssignee(maintainer.getString("assignee"));
                    }
                    break;
                case "Reviewer_Task":
                    JSONObject reviewer = adwarApi.getCourseReviewerRole(courseCode);
                    if (reviewer != null) {
                        delegateTask.setAssignee(reviewer.getString("assignee"));
                    }
                    break;
                case "Chairman_Task":
                    JSONObject departments = staffApi.getDepartment(departmentId);

                    if (departments != null) {
                        String chainrman_username = departments.getJSONObject("manager").getString("username");

                        delegateTask.setAssignee(chainrman_username);
                    }
                    break;
                case "ACC_Task":
                    String aac_assignee = delegateTask.getVariable("AACTaskAssignee") + "";
                    delegateTask.setAssignee(aac_assignee);

                    break;
                case "Collage_Dean_Task":
                    JSONObject college = staffApi.getDepartment(collegeId);

                    if (college != null) {
                        String dean_username = college.getJSONObject("manager").getString("username");

                        delegateTask.setAssignee(dean_username);
                    }
                    break;
                case "DGS_Dean_Task":
                    JSONObject dgs_department = staffApi.getDepartment(dgs_department_id);
                    if (dgs_department != null) {
                        delegateTask.setAssignee(dgs_department.getJSONObject("manager").getString("username"));
                    }
                    break;
                case "Vice_Rector_Task":
                    JSONArray vice_rector_users = staffApi.getEmployeesByJobTitle(vice_rector_job_title_id);
                    if (vice_rector_users != null && vice_rector_users.length() > 0) {
                        if (vice_rector_users.length() == 1) {
                            delegateTask.setAssignee(((JSONObject) vice_rector_users.get(0)).getString("username"));
                        } else {
                            throw new IllegalStateException("got multiple Vice Rector Users");
                        }
                    }
                    break;
                case "Rector_Task":
                    JSONArray rector_users = staffApi.getEmployeesByJobTitle(rector_job_title_id);
                    if (rector_users != null && rector_users.length() > 0) {
                        if (rector_users.length() == 1) {
                            delegateTask.setAssignee(((JSONObject) rector_users.get(0)).getString("username"));
                        } else {
                            throw new IllegalStateException("got multiple Rector Users");
                        }
                    }
                    break;
            }
        } catch (UnirestException e) {
            LOGGER.warning(e.getStackTrace().toString());
            throw new IllegalStateException(e.getStackTrace().toString());
        }

        if (PropertiesHelper.isDebug()) {
            LOGGER.info("Task Assigned to  ===============================");
            LOGGER.info(delegateTask.getAssignee());
        }

        if (delegateTask.getAssignee() == null || delegateTask.getAssignee().equals("")) {
            throw new IllegalStateException("This Task was not assigned to any user");
        }
    }
}
