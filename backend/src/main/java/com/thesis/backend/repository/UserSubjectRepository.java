package com.thesis.backend.repository;

import com.thesis.backend.dto.UserSubject;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface UserSubjectRepository extends JpaRepository<UserSubject, String> {
    @Query("SELECT us.subject.id FROM UserSubject us WHERE us.user.id = ?1")
    List<String> getSubjectsFromUserId(String id);
}