package com.thesis.backend.service;

import com.thesis.backend.BackendApplication;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.mysql.UserRepository;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

import static com.thesis.backend.exception.CustomException.DuplicateEntityException;
import static org.junit.jupiter.api.Assertions.*;

// https://stackoverflow.com/questions/12626502/rollback-transaction-after-test

@RunWith(SpringRunner.class)
@SpringBootTest(classes = BackendApplication.class)
@Transactional
public class UserServiceTest {
    @Autowired
    private ModelMapper modelMapper;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private UserServiceImpl userService;

    @Test
    public void testModelMapperNotNull() {
        assertNotEquals(modelMapper, null);
    }

    @Test
    public void testSaveUserSuccessfully() {
        UserDto userDto = UserDto.builder()
                .id(1752261)
                .name("A")
                .gender(0)
                .majorCode("B")
                .build();
        User testUser = modelMapper.map(userDto, User.class);
        User savedUser = modelMapper.map(userService.create(userDto), User.class);
        assertEquals(testUser, savedUser);
    }

    @Test
    public void testSavedUserFailedShouldThrowDuplicateException() {
        UserDto userDto = UserDto.builder()
                .id(1752259)
                .name("A")
                .gender(0)
                .majorCode("B")
                .build();
        assertThrows(DuplicateEntityException.class, () -> {
            userService.create(userDto);
        });
    }

    @Test
    public void testFindExistingUser() {
        UserDto user = userService.find(1752259);
        assertNotNull(user);
    }

    @Test
    public void testFindNonExistingUserShouldThrowEntityNotFoundException() {
        assertThrows(CustomException.EntityNotFoundException.class, () -> {
            userService.find(-1);
        });
    }

    @Test
    public void testUpdateExistingUser() {
        UserDto userDto = userService.find(9);
        assertNotNull(userDto);
        userDto.setName("test1");
        userService.update(userDto);
        assertEquals(userDto.getName(), userService.find(9).getName());
    }

    @Test
    public void testUpdateNonExistingUserShouldThrowEntityNotFoundException() {
        assertThrows(CustomException.EntityNotFoundException.class, () -> {
            userService.update(new UserDto(-1, "A", 0, "B", "normal"));
        });
    }

    @Test
    public void testDeleteExistingUser() {
        userService.delete(9);
        Optional<User> user = userRepository.findById(9);
        assertTrue(user.isEmpty());
    }

    @Test
    public void testDeleteNonExistingUser() {
        assertThrows(CustomException.EntityNotFoundException.class, () -> {
            userService.delete(-1);
        });
    }
}
