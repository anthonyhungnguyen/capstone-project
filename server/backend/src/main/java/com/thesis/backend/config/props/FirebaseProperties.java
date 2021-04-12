package com.thesis.backend.config.props;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Data
@ConfigurationProperties(prefix = "firebase")
@Configuration
public class FirebaseProperties {
    private String bucketName;
    private String imageUrl;
}
