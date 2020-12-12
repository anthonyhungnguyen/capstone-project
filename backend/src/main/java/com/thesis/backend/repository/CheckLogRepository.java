package com.thesis.backend.repository;

import com.thesis.backend.dto.CheckLog;
import org.springframework.data.mongodb.repository.MongoRepository;
import java.util.List;

public interface CheckLogRepository extends MongoRepository<CheckLog, String> {
    List<CheckLog> findAllByStudentID(int id);
}
