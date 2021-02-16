package com.thesis.backend;

import com.thesis.backend.model.User;
import com.thesis.backend.repository.UserRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jdbc.AutoConfigureTestDatabase;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.test.context.junit4.SpringRunner;

import java.util.Optional;

import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@RunWith(SpringRunner.class)
@DataJpaTest
@AutoConfigureTestDatabase
public class UserRepositoryTest {
    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;


    @Test
    public void testSaveNewUser() {
        entityManager.persist(User.builder().id(0)
                .gender(0)
                .name("A")
                .majorCode("B")
                .build());
        Optional<User> user = userRepository.findById(0);
        assertTrue(user.isPresent());
        assertNotNull(user.get());
        assertEquals(user.get().getName(), "A");
    }

    @Test
    public void testGetUser() {
        entityManager.persist(User.builder().id(0)
                .gender(0)
                .name("A")
                .majorCode("B")
                .build());
        Optional<User> user = userRepository.findById(0);
        assertTrue(user.isPresent());
        assertNotNull(user.get());
        assertEquals(user.get().getName(), "A");
    }

    @Test
    public void testDeleteUser() {
        entityManager.persist(User.builder().id(1752259)
                .gender(0)
                .name("A")
                .majorCode("B")
                .build());
        Optional<User> user = userRepository.findById(1752259);
        assertTrue(user.isPresent());
        userRepository.deleteById(1752259);
        Optional<User> userToCheck = userRepository.findById(1752259);
        assertTrue(userToCheck.isEmpty());
    }

    @Test
    public void testUpdateUser() {
        entityManager.persist(User.builder().id(0)
                .gender(0)
                .name("A")
                .majorCode("B")
                .build());
        Optional<User> user = userRepository.findById(0);
        assertTrue(user.isPresent());
        user.get().setName("C");
        userRepository.save(user.get());
        Optional<User> userToCheck = userRepository.findById(0);
        userToCheck.ifPresent(value -> assertEquals(value.getName(), "C"));
    }
}
