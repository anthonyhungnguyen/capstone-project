package com.thesis.backend.repository.mongodb;

import com.thesis.backend.model.Log;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface LogRepository extends MongoRepository<Log, Integer> {
    List<Log> findLogsByUserIDAndSubjectIDAndGroupCodeAndSemester(Integer userid,
                                                                  String subjectId,
                                                                  String groupCode,
                                                                  int semester);

    List<Log> findLogsByUserID(Integer userid);

    List<Log> findLogsBySubjectIDAndGroupCodeAndSemester(String subjectId,
                                                         String groupCode,
                                                         int semester);
}