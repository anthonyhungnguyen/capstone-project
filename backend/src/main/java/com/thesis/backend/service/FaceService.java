package com.thesis.backend.service;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.thesis.backend.model.Face;
import com.thesis.backend.repository.mongodb.FaceRepository;
import com.thesis.backend.util.DateUtil;
import lombok.Data;
import okhttp3.*;
import org.bson.BsonBinarySubType;
import org.bson.types.Binary;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@Service
public class FaceService {
    private final String faceAPI = "http://localhost:5000";
    private final FaceRepository faceRepository;

    @Data
    public class AugmentFaceResponse {
        @JsonProperty("augmentFaceArray")
        private List<String> augmentFaceArray;
    }

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

    public Boolean saveFace(Integer userid, MultipartFile multipartFile) throws IOException {
        Face face = Face.builder()
                .userId(userid)
                .photo(new Binary(BsonBinarySubType.BINARY, multipartFile.getBytes()))
                .timestamp(DateUtil.today().toString())
                .status("Not verified")
                .build();
        Face savedFace = faceRepository.save(face);

        List<String> augmentFaceArray = augmentFace(savedFace);
        augmentFaceArray.forEach(l -> {
            System.out.println(l);
        });
        return true;
    }

    private List<String> augmentFace(Face savedFace) throws IOException {
        RequestBody requestBody = new FormBody.Builder()
                .add("faceImage", savedFace.getPhoto().toString())
                .build();
        Request request = new Request.Builder()
                .url(faceAPI)
                .post(requestBody)
                .build();

        Response response = client.newCall(request).execute();

        AugmentFaceResponse response1 = gson.fromJson(response.body().toString(), AugmentFaceResponse.class);

        return response1.getAugmentFaceArray();
    }
}
