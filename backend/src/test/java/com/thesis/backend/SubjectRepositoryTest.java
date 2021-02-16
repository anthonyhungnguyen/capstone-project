package com.thesis.backend;


import com.thesis.backend.model.Subject;
import com.thesis.backend.model.SubjectId;
import com.thesis.backend.repository.SubjectRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@RunWith(SpringRunner.class)
@DataJpaTest
@AutoConfigureTestDatabase
public class SubjectRepositoryTest {
    @Autowired
    private TestEntityManager testEntityManager;

    @Autowired
    private SubjectRepository subjectRepository;

    @Test
    public void testSaveSubject() {
        testEntityManager.persist(Subject.builder()
                .id("A")
                .groupCode("B")
                .semester(0)
                .build());
        Optional<Subject> subject = subjectRepository.findById(new SubjectId("A", "B", 0));
        assertTrue(subject.isPresent());
        assertEquals(subject.get().getId(), "A");
        assertEquals(subject.get().getGroupCode(), "B");
        assertEquals(subject.get().getSemester(), 0);
    }

    @Test
    public void testGetSubject() {

        testEntityManager.persist(Subject.builder()
                .id("A")
                .groupCode("B")
                .semester(0)
                .build());

        Optional<Subject> subject = subjectRepository.findById(new SubjectId("A", "B", 0));
        assertTrue(subject.isPresent());
        assertEquals(subject.get().getId(), "A");
        assertEquals(subject.get().getGroupCode(), "B");
        assertEquals(subject.get().getSemester(), 0);
    }

    @Test
    public void testDeleteSubject() {
        testEntityManager.persist(Subject.builder()
                .id("A")
                .groupCode("B")
                .semester(0)
                .build());
        SubjectId subjectId = SubjectId.builder().id("A").groupCode("B").semester(0).build();
        Optional<Subject> subject = subjectRepository.findById(subjectId);
        assertTrue(subject.isPresent());
        subjectRepository.deleteById(subjectId);
        Optional<Subject> subjectToCheck = subjectRepository.findById(subjectId);
        assertTrue(subjectToCheck.isEmpty());
    }

    @Test
    public void testUpdateSubject() {
        testEntityManager.persist(Subject.builder()
                .id("A")
                .groupCode("B")
                .semester(0)
                .build());

        SubjectId subjectId = SubjectId.builder().id("A").groupCode("B").semester(0).build();
        Optional<Subject> subject = subjectRepository.findById(subjectId);
        assertTrue(subject.isPresent());

        subject.get().setName("D");
        subjectRepository.save(subject.get());
        Optional<Subject> subjectToCheck = subjectRepository.findById(subjectId);
        assertTrue(subjectToCheck.isPresent());
        assertEquals(subjectToCheck.get().getName(), "D");
    }
}
