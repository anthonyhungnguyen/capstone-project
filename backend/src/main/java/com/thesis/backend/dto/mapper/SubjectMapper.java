package com.thesis.backend.dto.mapper;

import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.model.Subject;
import com.thesis.backend.model.SubjectId;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.stream.Collectors;

@Component
public class SubjectMapper {
    private static ModelMapper modelMapper;

    @Autowired
    public SubjectMapper(ModelMapper modelMapper) {
        SubjectMapper.modelMapper = modelMapper;
    }

    public static SubjectDto toSubjectDto(Subject subject) {
        return SubjectDto.builder()
                .subjectIDDto(modelMapper.map(new SubjectId(subject.getId(), subject.getGroupCode(), subject.getSemester()), SubjectIDDto.class))
                .weekDay(subject.getWeekDay())
                .weekLearn(subject.getWeekLearn())
                .name(subject.getName())
                .room(subject.getRoom())
                .timeRange(subject.getTimeRange())
                .userDtos(subject.getUsers()
                        .stream()
                        .map(user -> modelMapper.
                                map(user, UserDto.class))
                        .collect(Collectors.toList()))
                .build();
    }
}
