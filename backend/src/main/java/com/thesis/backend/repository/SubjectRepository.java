package com.thesis.backend.repository;

import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.model.Subject;
import com.thesis.backend.model.SubjectId;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import javax.transaction.Transactional;
import java.util.List;

@Repository
@Transactional
public interface SubjectRepository extends JpaRepository<Subject, SubjectId> {
    List<UserDto> findSubjectsBySemester(int semester);
}
