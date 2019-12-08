package sa.edu.kfupm.ictc.course_specification_process.utils.api;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.JSONArray;
import org.json.JSONObject;
import sa.edu.kfupm.ictc.course_specification_process.utils.DateTimeConverters.Converters;
import sa.edu.kfupm.ictc.course_specification_process.utils.PropertiesHelper;

import java.util.Properties;
import java.util.logging.Logger;

public class AdwarApi {
    private final static Logger LOGGER = Logger.getLogger("course specification-Workflow");
    private static Gson gson = Converters.registerDateTime(new GsonBuilder()).create();

    private static AdwarApi instance = null;

    private WebServiceClient webClient = null;
    private String COURSE_REVIEWER = null;
    private String COURSE_MAINTAINTER = null;

    private AdwarApi() {
        PropertiesHelper propertiesInstance = PropertiesHelper.getInstance();
        Properties properties = propertiesInstance.getProperties();

        this.webClient = new WebServiceClient(
                properties.getProperty("ADWAR_URL"),
                properties.getProperty("ADWAR_USERNAME"),
                properties.getProperty("ADWAR_PASSWORD")
        );
        COURSE_REVIEWER = properties.getProperty("ADWAR_COURSE_REVIEWER");
        COURSE_MAINTAINTER = properties.getProperty("ADWAR_COURSE_MAINTAINER");
    }

    public static AdwarApi getInstance() {
        if (instance == null) {
            synchronized (AdwarApi.class) {
                if (instance == null) {
                    instance = new AdwarApi();
                }
            }
        }
        return instance;
    }

    public JSONObject getCourseReviewerRole(String course_code) throws UnirestException {
        return getRoleObject(course_code, COURSE_REVIEWER);
    }

    public JSONObject getCourseMaintainerRole(String course_code) throws UnirestException {
        return getRoleObject(course_code, COURSE_MAINTAINTER);
    }

    private JSONObject getRoleObject(String course_code, String role_code) throws UnirestException {
        HttpResponse<JsonNode> jsonResponse = webClient.get("api/academic-roles/course/roles?role_code=" + role_code + "&course=" + course_code);
        if (PropertiesHelper.isDebug())
            LOGGER.info("responce status is " + jsonResponse.getStatus());
        if (jsonResponse.getStatus() <= 399) {
            JsonNode body = jsonResponse.getBody();

            JSONArray data = (JSONArray) body.getObject().get("data");
            if (PropertiesHelper.isDebug())
                LOGGER.info(((JSONObject) data.get(0)).getString("assignee"));
            return (JSONObject) data.get(0);
        }
        return null;
    }
}
