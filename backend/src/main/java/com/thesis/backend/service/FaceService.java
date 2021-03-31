package com.thesis.backend.service;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.thesis.backend.model.Face;
import com.thesis.backend.repository.mongodb.FaceRepository;
import com.thesis.backend.util.DateUtil;
import lombok.Data;
import okhttp3.*;
import org.apache.tomcat.util.codec.binary.Base64;
import org.apache.tomcat.util.codec.binary.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@Service
public class FaceService {
    private final String faceAPI = "http://localhost:5000/face/augment";
    private final FaceRepository faceRepository;
    private final String REGISTER_TOPIC = "register";

    @Data
    public class AugmentFaceResponse {
        @JsonProperty("augmentFaceArray")
        private List<String> augmentFaceArray;
    }

    @Autowired
    private KafkaTemplate<String, Object> kafkaTemplate;

    @Autowired
    private OkHttpClient client;

    @Autowired
    private Gson gson;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    public FaceService(FaceRepository faceRepository) {
        this.faceRepository = faceRepository;
    }

    public List<Face> findAllFacesByUserId(Integer username) {
        return faceRepository.findAllByUserId(username);
    }

    public String multipartFileToBase64(byte[] imageByteArray) {
        StringBuilder sb = new StringBuilder();
//        sb.append("data:image/png;base64,");
        sb.append(StringUtils.newStringUtf8(Base64.encodeBase64(imageByteArray, false)));
        return sb.toString();
    }

    public Boolean saveFace(Integer userid, MultipartFile multipartFile) throws IOException {
        Face face = Face.builder()
                .userId(userid)
                .photo(multipartFileToBase64(multipartFile.getBytes()))
                .timestamp(DateUtil.today().toString())
                .status("Not verified")
                .build();
        Face savedFace = faceRepository.save(face);
        kafkaTemplate.send(REGISTER_TOPIC, savedFace);

        List<String> augmentFaceArray = augmentFace(savedFace);
        augmentFaceArray.forEach(l -> {
            Face augmentFace = Face.builder()
                    .userId(face.getUserId())
                    .timestamp(DateUtil.today().toString())
                    .status("Not verified")
                    .isAugmented(true)
                    .photo(l)
                    .source(face.getPhoto())
                    .build();
            Face augmentFaceSaved = faceRepository.save(augmentFace);
            kafkaTemplate.send(REGISTER_TOPIC, augmentFaceSaved);
//            System.out.println("saved");
//            System.out.println(l);
        });
        return true;
    }

    private List<String> augmentFace(Face savedFace) throws IOException {
        String json = String.format("{\"faceImage\":\"%s\"}", savedFace.getPhoto());
        RequestBody body = RequestBody.create(MediaType.parse("application/json"), json);
        Request request = new Request.Builder()
                .url(faceAPI)
                .post(body)
                .build();
        try (Response response = client.newCall(request).execute()) {
            AugmentFaceResponse response1 = gson.fromJson(response.body().string(), AugmentFaceResponse.class);
            return response1.getAugmentFaceArray();
        }
    }
}
