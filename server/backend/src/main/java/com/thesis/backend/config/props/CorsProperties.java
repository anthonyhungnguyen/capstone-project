package com.thesis.backend.config.props;


import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties("cors")
public class CorsProperties implements ApplicationProperties {
    private String[] allowOrigins;
    private boolean allowCredentials;
}
