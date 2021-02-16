package com.thesis.backend.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Component;

@Component
@PropertySource("classpath:custom.properties")
public class PropertiesConfig {
    private final Environment environment;

    @Autowired
    public PropertiesConfig(Environment environment) {
        this.environment = environment;
    }

    public String getConfigValue(String configKey) {
        return environment.getProperty(configKey);
    }
}
