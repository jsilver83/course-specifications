package sa.edu.kfupm.ictc.course_specification_process.utils.api;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.json.JSONArray;
import org.json.JSONObject;
import sa.edu.kfupm.ictc.course_specification_process.utils.PropertiesHelper;

import java.util.Properties;

public class BannerApi {
    private static BannerApi instance = null;

    private WebServiceClient webClient = null;

    private BannerApi() {
        PropertiesHelper propertiesInstance = PropertiesHelper.getInstance();
        Properties properties = propertiesInstance.getProperties();

        this.webClient = new WebServiceClient(
                properties.getProperty("BANNER_URL"),
                properties.getProperty("BANNER_USERNAME"),
                properties.getProperty("BANNER_PASSWORD")
        );
    }

    public static BannerApi getInstance() {
        if (instance == null) {
            synchronized (BannerApi.class) {
                if (instance == null) {
                    instance = new BannerApi();
                }
            }
        }
        return instance;
    }

    public JSONObject getDepartment(String department_id) throws UnirestException {
        HttpResponse<JsonNode> jsonResponse = webClient.get("department/" + department_id);
        if (jsonResponse.getStatus() <= 399) {
            JsonNode body = jsonResponse.getBody();

            return (JSONObject) body.getObject().get("data");
        }
        return null;
    }

    public JSONObject getCollage(String collage_id) throws UnirestException {
        HttpResponse<JsonNode> jsonResponse = webClient.get("collage/" + collage_id);
        if (jsonResponse.getStatus() <= 399) {
            JsonNode body = jsonResponse.getBody();

            return (JSONObject) body.getObject().get("data");
        }
        return null;
    }

}
