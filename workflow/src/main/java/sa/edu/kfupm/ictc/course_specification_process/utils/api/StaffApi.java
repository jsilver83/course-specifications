package sa.edu.kfupm.ictc.course_specification_process.utils.api;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.JSONArray;
import org.json.JSONObject;
import sa.edu.kfupm.ictc.course_specification_process.utils.PropertiesHelper;

import java.util.Properties;
import java.util.logging.Logger;

public class StaffApi {

    private final static Logger LOGGER = Logger.getLogger("course_specification_process");

    private static StaffApi instance = null;

    private WebServiceClient webClient = null;

    private StaffApi() {
        PropertiesHelper propertiesInstance = PropertiesHelper.getInstance();
        Properties properties = propertiesInstance.getProperties();

        this.webClient = new WebServiceClient(
                properties.getProperty("STAFF_URL"),
                properties.getProperty("STAFF_USERNAME"),
                properties.getProperty("STAFF_PASSWORD")
        );
    }

    public static StaffApi getInstance() {
        if (instance == null) {
            synchronized (StaffApi.class) {
                if (instance == null) {
                    instance = new StaffApi();
                }
            }
        }
        return instance;
    }


    public JSONArray getEmployeesByJobTitle(String job_title_id) throws UnirestException {
        HttpResponse<JsonNode> jsonResponse = webClient.get("employee?job_title_id=" + job_title_id);
        if (jsonResponse.getStatus() <= 399) {
            JsonNode body = jsonResponse.getBody();

            return (JSONArray) body.getObject().get("data");
        }
        return null;
    }

    public JSONObject getDepartment(String department_id) throws UnirestException {
        HttpResponse<JsonNode> jsonResponse = webClient.get("v2/department/" + department_id);
        if (PropertiesHelper.isDebug()){
            LOGGER.info("Status: "+jsonResponse.getStatus());
            LOGGER.info("body: "+jsonResponse.getBody().toString());

        }

        if (jsonResponse.getStatus() <= 399) {
            JsonNode body = jsonResponse.getBody();

            return (JSONObject) body.getObject().get("data");
        }
        return null;
    }
}
