package com.thesis.backend.service;

import com.thesis.backend.model.Face;
import com.thesis.backend.repository.mongodb.FaceRepository;
import com.thesis.backend.util.DateUtil;
import org.bson.BsonBinarySubType;
import org.bson.types.Binary;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.List;

@Service
public class FaceService {

    private final FaceRepository faceRepository;

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
        faceRepository.save(face);
        return true;
    }
}
