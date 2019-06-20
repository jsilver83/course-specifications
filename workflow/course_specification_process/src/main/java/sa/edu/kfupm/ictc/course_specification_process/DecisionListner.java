package sa.edu.kfupm.ictc.course_specification_process;

import org.camunda.bpm.engine.delegate.DelegateTask;
import org.camunda.bpm.engine.delegate.TaskListener;

import java.util.logging.Logger;

public class DecisionListner implements TaskListener {

    public void notify(DelegateTask delegateTask) {
        delegateTask.setVariable("GatewayDecision", delegateTask.getVariable("FormDecision"));
        delegateTask.setVariable("FormDecision", null);
    }
}
