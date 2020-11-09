package com.thesis.backend.repository;

import com.thesis.backend.dto.Subject;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface SubjectRepository extends JpaRepository<Subject, String> {
    List<Subject> findSubjectsBySemester(int semester);

    List<Subject> findSubjectByIdAndSemester(String id, int semester);

    boolean existsByIdAndGroupCodeAndSemester(String id, String groupCode, int semester);
}
