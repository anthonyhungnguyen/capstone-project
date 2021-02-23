
package com.thesis.backend.repository;

import com.thesis.backend.model.Log;
import com.thesis.backend.repository.mongodb.LogRepository;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.data.mongo.DataMongoTest;
import org.springframework.test.context.junit4.SpringRunner;

import static org.junit.jupiter.api.Assertions.assertTrue;


@RunWith(SpringRunner.class)
@DataMongoTest
public class LogRepositoryTest {

    @Autowired
    private LogRepository logRepository;

    @Before
    public void init() {
        Log log = Log.builder()
                .userId(1752259)
                .subjectID("CO0000")
                .groupCode("CC01")
                .semester(201)
                .build();
        logRepository.save(log);
    }

    @Test
    public void testFindLogBasedOnUserid() {
        assertTrue(logRepository.findLogsByUserId(1752259).size() != 0);
    }

    @Test
    public void testFindLogBasedOnSubjectId() {
        assertTrue(logRepository.findLogsBySubjectIDAndGroupCodeAndSemester("CO0000",
                "CC01", 201).size() != 0);
    }
}
