package com.thesis.backend.dto.mapper;

import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.model.Subject;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Component;

import java.util.HashSet;
import java.util.stream.Collectors;

@Component
public class SubjectMapper {
    public static SubjectDto toUserDto(Subject subject) {
        return SubjectDto.builder()
                .subjectIDDto(new SubjectIDDto(subject.getId(), subject.getGroupCode(), subject.getSemester()))
                .name(subject.getName())
                .weekDay(subject.getWeekDay())
                .timeRange(subject.getTimeRange())
                .room(subject.getRoom())
                .base(subject.getBase())
                .weekLearn(subject.getWeekLearn())
                .userDtos(new HashSet<UserDto>(subject
                        .getUsers()
                        .stream()
                        .map(user -> new ModelMapper().map(user, UserDto.class))
                        .collect(Collectors.toSet())))
                .build();
    }
}
