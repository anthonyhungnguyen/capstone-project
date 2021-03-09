package com.thesis.backend.service;

import com.thesis.backend.constant.ERole;
import com.thesis.backend.dto.mapper.UserMapper;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.dto.request.SignUpRequest;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.Role;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.mysql.RoleRepository;
import com.thesis.backend.repository.mysql.UserRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

import static com.thesis.backend.constant.EntityType.USER;
import static com.thesis.backend.constant.ExceptionType.DUPLICATE_ENTITY;
import static com.thesis.backend.constant.ExceptionType.ENTITY_NOT_FOUND;

@Service
public class UserServiceImpl implements BaseService<UserDto, Integer> {
    private final UserRepository userRepository;
    private final ModelMapper modelMapper;
    private final RoleRepository roleRepository;

    @Autowired
    public UserServiceImpl(UserRepository userRepository, ModelMapper modelMapper, UserMapper userMapper, RoleRepository roleRepository) {
        this.userRepository = userRepository;
        this.modelMapper = modelMapper;
        this.roleRepository = roleRepository;
    }


    @Override
    public UserDto find(Integer id) {
        Optional<User> user = userRepository.findById(id);
        if (user.isPresent()) {
            return UserMapper.toUserDto(user.get());
        }
        throw CustomException.throwException(USER, ENTITY_NOT_FOUND, id.toString());
    }

    public boolean register(SignUpRequest signUpRequest) {
        Optional<User> user = userRepository.findById(signUpRequest.getId());
        if (user.isEmpty()) {
            User mapToUser = UserMapper.signUpRequestToUser(signUpRequest);

            Set<Role> roles = new HashSet<>();
            Role studentRole = roleRepository.findByName(ERole.STUDENT)
                    .orElseThrow(() -> new RuntimeException("Error: Role is not found."));
            roles.add(studentRole);

            mapToUser.setRoles(roles);
            userRepository.save(mapToUser);
            return true;
        }
        throw CustomException.throwException(USER, DUPLICATE_ENTITY, String.valueOf(signUpRequest.getId()));
    }

    @Override
    public UserDto create(UserDto userDto) {
        Optional<User> user = userRepository.findById(userDto.getId());
        if (user.isEmpty()) {
            User mapToUser = modelMapper.map(userDto, User.class);
            return modelMapper.map(userRepository.save(mapToUser), UserDto.class);
        }
        throw CustomException.throwException(USER, DUPLICATE_ENTITY, String.valueOf(userDto.getId()));
    }

    @Override
    public void delete(Integer id) {
        Optional<User> user = userRepository.findById(id);
        if (user.isPresent()) {
            userRepository.delete(modelMapper.map(user.get(), User.class));
            return;
        }
        throw CustomException.throwException(USER, ENTITY_NOT_FOUND, id.toString());
    }

    @Override
    public UserDto update(UserDto o) {
        Optional<User> user = userRepository.findById(o.getId());
        if (user.isPresent()) {
            User userToSave = modelMapper.map(o, User.class);
            return modelMapper.map(userRepository.save(userToSave), UserDto.class);
        }
        throw CustomException.throwException(USER, ENTITY_NOT_FOUND, String.valueOf(o.getId()));
    }

}
