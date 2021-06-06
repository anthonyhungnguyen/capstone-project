package com.thesis.backend.service;

import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.UserDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class TeacherService {
    private final UserService userService;
    private final SubjectService subjectService;
    private final ScheduleService scheduleService;
    private final LogService logService;

    @Autowired
    public TeacherService(UserService userService, SubjectService subjectService, ScheduleService scheduleService, LogService logService) {
        this.userService = userService;
        this.subjectService = subjectService;
        this.scheduleService = scheduleService;
        this.logService = logService;
    }

    public Map<String, Float> calculateAttendanceRate(Integer teacherId) {
        UserDto userDto = userService.find(teacherId);
        Map<String, Float> result = new HashMap<>();
        List<SubjectDto> subjectDtoList = userDto.getTeachSubjects();
        subjectDtoList.stream().map(SubjectDto::getSubjectIDDto).forEach(id -> {
            int expectTotalTimes =
                    subjectService.countStudentsInSubject(id.getSemester(), id.getId(), id.getGroupCode()) *
                            scheduleService.countSchedulesWithID(id.getSemester(), id.getId(), id.getGroupCode());
            Integer realTotalTimes = logService.countAttendanceLogsBySubject(id.getSemester(), id.getId(), id.getGroupCode());
            result.put(String.format("%s_%s_%s", id.getSemester(), id.getId(), id.getGroupCode()), (float) realTotalTimes / expectTotalTimes);
        });
        return result;
    }
}
