package com.thesis.backend.repository;

import com.thesis.backend.dto.Enrollment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserSubjectRepository extends JpaRepository<Enrollment, String> {
    List<Enrollment> findUserSubjectsByUser_Id(String id);
}