package com.thesis.backend.config.props;

import lombok.Data;
import lombok.experimental.Accessors;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@Accessors(chain = true)
@ConfigurationProperties("jwt")
public class JwtProperties implements ApplicationProperties {
    String jwtSecret;
    long jwtExpirationMs;
}
