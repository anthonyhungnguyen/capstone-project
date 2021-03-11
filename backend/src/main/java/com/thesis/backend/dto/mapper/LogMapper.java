package com.thesis.backend.dto.mapper;

import com.thesis.backend.dto.model.EnrollmentDto;
import com.thesis.backend.dto.model.LogDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.model.Log;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class LogMapper {
    private static ModelMapper modelMapper;

    @Autowired
    public LogMapper(ModelMapper modelMapper) {
        LogMapper.modelMapper = modelMapper;
    }

    public static LogDto toLogDto(Log log) {
        return LogDto.builder()
                .enrollmentDto(
                        EnrollmentDto.builder()
                                .userId(log.getUserID())
                                .subjectIDDto(
                                        new SubjectIDDto(log.getSubjectID(),
                                                log.getGroupCode(), log.getSemester()))
                                .build())
                .timestamp(log.getTimestamp())
                .build();
    }
}
