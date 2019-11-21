package sa.edu.kfupm.ictc.course_specification_process.utils;


import org.camunda.bpm.engine.RepositoryService;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.DelegateTask;
import org.camunda.bpm.engine.impl.javax.el.ExpressionFactory;
import org.camunda.bpm.engine.impl.javax.el.ValueExpression;
import org.camunda.bpm.engine.impl.juel.ExpressionFactoryImpl;
import org.camunda.bpm.engine.impl.juel.SimpleContext;
import org.camunda.bpm.engine.impl.juel.SimpleResolver;
import org.camunda.bpm.model.bpmn.instance.FlowNode;
import org.camunda.bpm.model.bpmn.instance.Gateway;
import org.camunda.bpm.model.bpmn.instance.SequenceFlow;
import org.camunda.bpm.model.xml.instance.ModelElementInstance;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class BpmnUtils {

    private final static Logger LOGGER = Logger.getLogger("DGS-Workflow");

    public static String GetProcessName(DelegateTask delegateTask){
        return GetProcessName(delegateTask.getExecution());
    }

    public static String GetProcessName(DelegateExecution execution){
        RepositoryService repositoryService = execution.getProcessEngineServices().getRepositoryService();
        String processName = repositoryService.createProcessDefinitionQuery()
                .processDefinitionId(execution.getProcessDefinitionId())
                .singleResult()
                .getName();
        return processName;
    }

    public static ArrayList<SequenceFlow> getGateWayOptions(ModelElementInstance instance) {
        ArrayList<SequenceFlow> sequenceFlows = new ArrayList<SequenceFlow>();

        FlowNode node = (FlowNode)instance;


        for(SequenceFlow sf: node.getOutgoing()) {
            if (sf.getTarget() != null && sf.getTarget() instanceof Gateway) {

                //sequenceFlows.addAll(sf.getTarget().getOutgoing());
                for(SequenceFlow eps : sf.getTarget().getOutgoing()){
                    sequenceFlows.add(eps);
                }
            }
        }
        return sequenceFlows;
    }

    public static String getDecisionValue(ModelElementInstance instance, String expresionKey, String expresionValue) {

        try {
            ArrayList<SequenceFlow> sequenceFlows = new ArrayList<SequenceFlow>();

            FlowNode node = (FlowNode)instance;


            for(SequenceFlow sf: node.getOutgoing()) {
//                if (sf.getName() != null) {
//                    LOGGER.info("Entering flow node " + sf.getName());
//                }

                if (sf.getTarget() != null && sf.getTarget() instanceof Gateway) {
                    //LOGGER.info(sf.getTarget().getName()+" Is Gateway Node");

//                    sequenceFlows.addAll(sf.getTarget().getOutgoing());
                    for(SequenceFlow eps : sf.getTarget().getOutgoing()){
//                        sequenceFlows.add(eps);
                        if (eps.getConditionExpression() != null) {
                            ExpressionFactory factory = new ExpressionFactoryImpl();
                            SimpleContext context = new SimpleContext(new SimpleResolver());

                            factory.createValueExpression(context, "${"+ expresionKey +"}", String.class).setValue(context, expresionValue);

                            ValueExpression expr1 = factory.createValueExpression(context, eps.getConditionExpression().getTextContent(), boolean.class);

                            boolean expresionResult = (Boolean)expr1.getValue(context);
                            //LOGGER.info("Evaluating expression "+ eps.getConditionExpression().getTextContent() +" to result " + expr1.getValue(context));
                            if(expresionResult){
                                //LOGGER.info("this is the one value we wan' it " + eps.getName());
                                return eps.getName();
                            }
                        }
                    }
                }
            }
        }
        catch (Exception e){
            LOGGER.info("an error was thrown in getDecisionValue with exception message: " + e.getMessage());
        }
        return expresionValue;
    }

    public static HashMap<String, String> getGateWayOptionsAsStringMap(ModelElementInstance instance) {
        HashMap<String, String> AvailableDecisions = new HashMap<>();

        try {
            FlowNode node = (FlowNode) instance;

            for (SequenceFlow sf : node.getOutgoing()) {
                if (sf.getTarget() != null && sf.getTarget() instanceof Gateway) {

                    for (SequenceFlow eps : sf.getTarget().getOutgoing()) {
                        if (eps.getConditionExpression() != null) {
                            String conditionExpression = eps.getConditionExpression().getTextContent();

                            Pattern pattern = Pattern.compile("=='(.*?)'");
                            Matcher matcher = pattern.matcher(conditionExpression);
                            String decisionsValue = "";
                            if (matcher.find()) {
                                decisionsValue = matcher.group(1);
                            }
                            AvailableDecisions.put(decisionsValue, eps.getName());

                        }
                    }
                }
            }
        } catch (Exception e) {
            LOGGER.info("an error was thrown in getDecisionValue with exception message: " + e.getMessage());
        }
        return AvailableDecisions;
    }

//    public static String getDecisionValue1(ModelElementInstance instance, String expresionKey, String expresionValue) {
//
//        try {
//            ArrayList<SequenceFlow> gateWaySequenceFlows = getGateWayOptions(instance);
//
//            //LOGGER.info("gateWaySequenceFlows is " + gson.toJson(gateWaySequenceFlows));
//
//            for(SequenceFlow expresionSequenceFlow : gateWaySequenceFlows){
//                if (expresionSequenceFlow.getConditionExpression() != null) {
//                    ExpressionFactory factory = new ExpressionFactoryImpl();
//                    SimpleContext context = new SimpleContext(new SimpleResolver());
//
//                    factory.createValueExpression(context, "${"+ expresionKey +"}", String.class).setValue(context, expresionValue);
//
//                    ValueExpression expr1 = factory.createValueExpression(context, expresionSequenceFlow.getConditionExpression().getTextContent(), boolean.class);
//
//                    boolean expresionResult = (Boolean)expr1.getValue(context);
//                    //LOGGER.info("Evaluating expression "+ expresionSequenceFlow.getConditionExpression().getTextContent() +" to result " + expr1.getValue(context));
//                    if(expresionResult){
//                        //LOGGER.info("this is the one value we wan' it " + expresionSequenceFlow.getName());
//                        return expresionSequenceFlow.getName();
//                    }
//                }
//            }
//        }
//        catch (Exception e){
//            LOGGER.info("an error was thrown in getDecisionValue with exception message: " + e.getMessage());
//        }
//        return expresionValue;
//    }
}
