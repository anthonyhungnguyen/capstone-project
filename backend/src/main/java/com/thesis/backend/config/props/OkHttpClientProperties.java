package com.thesis.backend.config.props;

import lombok.Data;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties("okhttp")
public class OkHttpClientProperties {
    public int connectTimeoutSecond;
}
