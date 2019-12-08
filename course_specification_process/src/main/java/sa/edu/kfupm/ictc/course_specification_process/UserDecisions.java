package sa.edu.kfupm.ictc.course_specification_process;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.camunda.bpm.engine.delegate.DelegateTask;
import org.camunda.bpm.engine.delegate.TaskListener;
import sa.edu.kfupm.ictc.course_specification_process.utils.BpmnUtils;
import sa.edu.kfupm.ictc.course_specification_process.utils.DateTimeConverters.Converters;
import sa.edu.kfupm.ictc.course_specification_process.utils.PropertiesHelper;

import java.util.HashMap;
import java.util.logging.Logger;

public class UserDecisions implements TaskListener {
    private final static Logger LOGGER = Logger.getLogger("Course Specification-Workflow");

    public void notify(DelegateTask delegateTask) {
        try {
            Gson gson = Converters.registerDateTime(new GsonBuilder()).create();

            HashMap<String, String> options = BpmnUtils.getGateWayOptionsAsStringMap(delegateTask.getBpmnModelElementInstance());

            String optionsJson = gson.toJson(options);

            delegateTask.setVariableLocal("options", optionsJson);

        } catch (Exception e) {
            if(PropertiesHelper.isDebug())
                LOGGER.warning("an exception has been thrown in UserDecisions" +
                        " Process id: " + delegateTask.getProcessInstanceId() +
                        " and task id:" + delegateTask.getId() +
                        " ,with message: " + e.getMessage());
            throw e;
        }
    }
}
