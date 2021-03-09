package com.thesis.backend.dto.mapper;

import com.thesis.backend.dto.model.RoleDto;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.dto.request.SignUpRequest;
import com.thesis.backend.model.User;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

import java.util.stream.Collectors;

@Component
public class UserMapper {


    private static ModelMapper modelMapper;
    private static PasswordEncoder passwordEncoder;

    @Autowired
    public UserMapper(ModelMapper modelMapper, PasswordEncoder passwordEncoder) {
        UserMapper.modelMapper = modelMapper;
        UserMapper.passwordEncoder = passwordEncoder;

    }

    public static UserDto toUserDto(User user) {
        return UserDto.builder()
                .id(user.getId())
                .subjectDtos(user
                        .getSubjects()
                        .stream()
                        .map(subject -> modelMapper.map(subject, SubjectDto.class))
                        .collect(Collectors.toList()))
                .roleDtos(user
                        .getRoles()
                        .stream()
                        .map(role -> modelMapper.map(role, RoleDto.class))
                        .collect(Collectors.toList()))
                .build();
    }

    public static User signUpRequestToUser(SignUpRequest signUpRequest) {
        return User.builder()
                .id(signUpRequest.getId())
                .password(passwordEncoder.encode(signUpRequest.getPassword()))
                .build();
    }
}
