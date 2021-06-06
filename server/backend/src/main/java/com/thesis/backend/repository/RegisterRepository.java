package com.thesis.backend.repository;

import com.thesis.backend.model.Register;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.transaction.annotation.Transactional;

public interface RegisterRepository extends JpaRepository<Register, String> {
    @Modifying
    @Query(value = "INSERT INTO register(user_id, image_link) VALUES(?1, ?2)", nativeQuery = true)
    @Transactional
    void insertRegisterByUserId(Integer userid, String imageLink);

    @Modifying
    @Query(value = "DELETE FROM register WHERE user_id = ?1", nativeQuery = true)
    @Transactional
    void deleteRegisterByUserId(Integer userid);
}
