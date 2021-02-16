package com.thesis.backend.dto.mapper;

import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.model.User;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

import java.util.HashSet;
import java.util.stream.Collectors;

@Component
public class UserMapper {
    public static UserDto toUserDto(User user) {
        return UserDto.builder()
                .id(user.getId())
                .gender(user.getGender())
                .name(user.getName())
                .majorCode(user.getMajorCode())
                .subjectDtos(new HashSet<SubjectDto>(user
                        .getSubjects()
                        .stream()
                        .map(subject -> new ModelMapper().map(subject, SubjectDto.class))
                        .collect(Collectors.toSet())))
                .build();
    }
}
