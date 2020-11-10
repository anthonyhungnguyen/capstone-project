package com.thesis.backend.repository;

import com.thesis.backend.dto.Subject;
import com.thesis.backend.dto.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface UserRepository extends JpaRepository<User, Integer> {
}
