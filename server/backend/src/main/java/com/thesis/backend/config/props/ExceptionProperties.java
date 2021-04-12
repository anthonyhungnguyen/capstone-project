package com.thesis.backend.config.props;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

@Component
@PropertySource("classpath:custom.properties")
public class ExceptionProperties {
    private final Environment environment;

    @Autowired
    public ExceptionProperties(Environment environment) {
        this.environment = environment;
    }

    public String getConfigValue(String configKey) {
        return environment.getProperty(configKey);
    }
}
