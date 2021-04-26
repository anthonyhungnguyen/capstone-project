package com.thesis.backend.repository;

import com.thesis.backend.model.Log;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface LogRepository extends JpaRepository<Log, Integer> {
    List<Log> findByUserID(Integer userid);

    List<Log> findByTeacherID(Integer teacherid);

    Integer countBySemesterAndSubjectIDAndGroupCode(int semester, String subjectID, String groupCode);
}
