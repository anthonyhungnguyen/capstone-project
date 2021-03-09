package com.thesis.backend.config;

import com.thesis.backend.config.props.OkHttpClientProperties;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.concurrent.TimeUnit;

@Configuration
public class OkHttpClientConfig {

    private final OkHttpClientProperties props;

    @Autowired
    public OkHttpClientConfig(OkHttpClientProperties props) {
        this.props = props;
    }

    @Bean
    public OkHttpClient okHttpClient() {
        return new OkHttpClient.Builder()
                .retryOnConnectionFailure(true)
                .connectTimeout(props.getConnectTimeoutSecond(), TimeUnit.SECONDS)
                .build();
    }
}
