package com.thesis.backend.repository;

import com.thesis.backend.dto.Enrollment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface EnrollmentRepository extends JpaRepository<Enrollment, String> {
    List<Enrollment> findEnrollmentsByUserIdAndSemester(int userId, int semester);

    boolean existsByUserIdAndSubjectIdAndGroupCodeAndSemester(int userId, String subjectId, String groupCode, int semester);
}