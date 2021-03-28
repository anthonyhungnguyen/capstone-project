package com.thesis.backend.config.props;

import lombok.Data;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Data
@Component
@ConfigurationProperties(prefix = "spring.kafka")
public class KafkaProperties {

    @Data
    @Component
    @ConfigurationProperties(prefix = "spring.kafka.consumer")
    public static class KafkaConsumerProperties {
        private String groupId;
        private Boolean enableAutoCommit;
        private Integer autoCommitInterval;
        private String autoOffsetReset;
    }


    private String bootstrapServers;

    @Autowired
    private KafkaConsumerProperties kafkaConsumerProperties;
}

