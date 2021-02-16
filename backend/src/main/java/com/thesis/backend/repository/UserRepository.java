package com.thesis.backend.repository;

import com.thesis.backend.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import javax.transaction.Transactional;
import javax.validation.constraints.NotNull;


@Repository
@Transactional
public interface UserRepository extends JpaRepository<User, Integer> {
    void deleteById(@NotNull(message = "Student ID cannot be null") int id);

}
