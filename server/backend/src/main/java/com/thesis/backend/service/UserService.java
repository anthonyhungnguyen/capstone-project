package com.thesis.backend.service;

import com.thesis.backend.constant.ERole;
import com.thesis.backend.dto.mapper.UserMapper;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.dto.request.SignUpRequest;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.Register;
import com.thesis.backend.model.Role;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.RoleRepository;
import com.thesis.backend.repository.UserRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

import static com.thesis.backend.constant.EntityType.USER;
import static com.thesis.backend.constant.ExceptionType.DUPLICATE_ENTITY;
import static com.thesis.backend.constant.ExceptionType.ENTITY_NOT_FOUND;

@Service
public class UserService {
    private final UserRepository userRepository;
    private final RoleRepository roleRepository;

    @Autowired
    public UserService(UserRepository userRepository, ModelMapper modelMapper, RoleRepository roleRepository) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
    }

    public List<UserDto> findAll() {
        return userRepository.findAll().stream().map(UserMapper::toUserDto).collect(Collectors.toList());
    }

    public boolean updateRegisterImageLink(Integer userid, String imageLink) {
        Optional<User> userOptional = userRepository.findById(userid);
        if (userOptional.isPresent()) {
            List<Register> registers = userOptional.get().getRegisters();
            registers.add(Register.builder().user(User.builder().id(userid).build()).imageLink(imageLink).build());
            userOptional.get().setRegisters(registers);
            userRepository.save(userOptional.get());
        }
        return true;
    }

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
}
