package com.thesis.backend.service;

import com.thesis.backend.dto.request.SubjectRegister;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.util.FileCopyUtils;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

@Service
@Slf4j
public class TeacherService {

    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final String BASE_URL = "http://localhost:3000/";

    @Autowired
    public TeacherService(KafkaTemplate<String, Object> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    public Boolean registerIOTDevice(SubjectRegister subjectRegister) throws IOException {
        String PRODUCER_TOPIC = "schedule";
        kafkaTemplate.send(PRODUCER_TOPIC, subjectRegister);
        sendPickle();
        return true;
    }

    private void sendPickle() throws IOException {
        Resource resource = new ClassPathResource("/static/emb.pickle");
        InputStream inputStream = resource.getInputStream();
        try {
            byte[] bData = FileCopyUtils.copyToByteArray(inputStream);
            String data = new String(bData, StandardCharsets.UTF_8);
            kafkaTemplate.send("data", data);
        } catch (IOException ioException) {
            log.error("IO Exception", ioException);
        }
    }

    @KafkaListener(topics = "attendance", groupId = "group-id")
    public void listen(String message) {
        System.out.println(message);
    }
}
