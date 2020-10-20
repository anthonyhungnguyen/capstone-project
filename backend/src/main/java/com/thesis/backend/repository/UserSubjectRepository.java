package com.thesis.backend.repository;

import com.thesis.backend.dto.UserSubject;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.Collection;
import java.util.List;
import java.util.Map;

@Repository
public interface UserSubjectRepository extends JpaRepository<UserSubject, String> {
    List<UserSubject> findUserSubjectsByUser_Id(String id);
}