package com.thesis.backend.config;

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Contact;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.servers.Server;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.Arrays;

@Configuration
public class OpenApiConfig {
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
                .servers(Arrays.asList(new Server().url("http://localhost:8080")))
                .info(new Info()
                        .title("Facial-recognition attendance system")
                        .description("Api documentation for system")
                        .contact(new Contact().email("hung.nguyenkevin99@hcmut.edu.vn")
                                .name("Anthony Hung Nguyen")
                                .url("facebook.com/phuchung276")));
    }
}
