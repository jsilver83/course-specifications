package sa.edu.kfupm.ictc.course_specification_process.utils;

import java.io.InputStream;
import java.util.Properties;

public class PropertiesHelper {

    private static PropertiesHelper propertiesHelper = null;
    private Properties properties = null;

    private PropertiesHelper() {
        this.properties = new Properties();
        try {
            InputStream propertiesStream = getClass().getClassLoader().getResourceAsStream("config.properties");
            this.properties.load(propertiesStream);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static PropertiesHelper getInstance() {
        if (propertiesHelper == null) {
            synchronized (PropertiesHelper.class) {
                if (propertiesHelper == null) {
                    propertiesHelper = new PropertiesHelper();
                }
            }
        }
        return propertiesHelper;
    }

    public Properties getProperties() {
        return this.properties;
    }

    public static boolean isDebug() {
        try {
            String debug = getInstance().getProperties().getProperty("DEBUG");
            return debug.equals("True");
        }
        catch (Exception e){
            return false;
        }
    }
}