package com.thesis.backend.repository;

import com.thesis.backend.model.Subject;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;

public interface EnrollmentRepository extends JpaRepository<Subject, String> {
    @Modifying
    @Query(value = "INSERT INTO enrollment VALUES(?1, ?2, ?3, ?4)", nativeQuery = true)
    @Transactional
    void insertEnrollment(Integer userid, String subjectID, String groupCode, Integer semester);
}
