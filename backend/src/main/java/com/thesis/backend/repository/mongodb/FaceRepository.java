package com.thesis.backend.repository.mongodb;

import com.thesis.backend.model.Face;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface FaceRepository extends MongoRepository<Face, Integer> {
    List<Face> findAllByUserId(Integer userid);
}
