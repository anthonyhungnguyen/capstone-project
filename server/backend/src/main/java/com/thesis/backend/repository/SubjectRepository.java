package com.thesis.backend.repository;

import com.thesis.backend.model.Subject;
import com.thesis.backend.model.SubjectId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
@Transactional
public interface SubjectRepository extends JpaRepository<Subject, SubjectId> {
    Subject findBySemesterAndNameAndGroupCode(int semester, String name, String groupCode);

    @Query(value = "SELECT COUNT(*) FROM enrollment WHERE semester=?1 AND group_code=?3 AND subject_id = ?2", nativeQuery = true)
    Integer countStudentsInSubject(int semester, String subjectID, String groupCode);


}
