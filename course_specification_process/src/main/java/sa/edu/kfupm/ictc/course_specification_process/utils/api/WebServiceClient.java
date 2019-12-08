package sa.edu.kfupm.ictc.course_specification_process.utils.api;

import java.util.HashMap;
import java.util.logging.Logger;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import com.mashape.unirest.request.GetRequest;
import com.mashape.unirest.request.HttpRequestWithBody;
import org.json.JSONObject;

import sa.edu.kfupm.ictc.course_specification_process.utils.DateTimeConverters.Converters;
import sa.edu.kfupm.ictc.course_specification_process.utils.PropertiesHelper;


public class WebServiceClient {
    private final static Logger LOGGER = Logger.getLogger("course specification-Workflow");
    private static Gson gson = Converters.registerDateTime(new GsonBuilder()).create();

    private String baseUrl;
    private String username = null;
    private String password = null;

    public WebServiceClient(String baseUrl, String username, String password) {
        if (PropertiesHelper.isDebug()) {
            LOGGER.info("baseUrl " + baseUrl);
            LOGGER.info("username " + username);
            LOGGER.info("password " + password);
        }

        this.baseUrl = baseUrl;
        this.username = username;
        this.password = password;
    }

    public WebServiceClient(String baseUrl) {
        if (PropertiesHelper.isDebug()) {
            LOGGER.info("baseUrl " + baseUrl);
        }

        this.baseUrl = baseUrl;
    }

    public HttpResponse<JsonNode> get(String endPoint) throws UnirestException {
        if (PropertiesHelper.isDebug())
            LOGGER.info("GET " + baseUrl + "/" + endPoint);

        GetRequest request = Unirest.get(baseUrl + "/" + endPoint);
        if (!username.isEmpty() && !password.isEmpty()) {
            request = request.basicAuth(username, password);
        }

        return request.asJson();
    }

    public HttpResponse<JsonNode> post(String endPoint, HashMap<String, String> content) throws UnirestException {
        return post(endPoint, content, new HashMap<>());
    }

    public HttpResponse<JsonNode> post(String endPoint, HashMap<String, String> content, HashMap<String, String> headers) throws UnirestException {
        if (PropertiesHelper.isDebug()) {
            LOGGER.info("POST " + baseUrl + "/" + endPoint);
            LOGGER.info("BODY " + gson.toJson(content));
        }

        JSONObject body = new JSONObject(content);

        HttpRequestWithBody request = Unirest.post(baseUrl + "/" + endPoint);

        for (String key : headers.keySet()) {
            request.header(key, headers.get(key));
        }

        if (!username.isEmpty() && !password.isEmpty()) {
            request = request.basicAuth(username, password);
        }
        return request.body(body.toString()).asJson();
    }

}
