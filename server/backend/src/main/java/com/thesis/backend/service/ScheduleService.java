package com.thesis.backend.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.thesis.backend.constant.EntityType;
import com.thesis.backend.constant.ExceptionType;
import com.thesis.backend.dto.mapper.ScheduleMapper;
import com.thesis.backend.dto.model.SubjectDto;
import com.thesis.backend.dto.model.SubjectIDDto;
import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.dto.request.ScheduleRequest;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.CacheAttendance;
import com.thesis.backend.model.Schedule;
import com.thesis.backend.repository.RedisRepository;
import com.thesis.backend.repository.ScheduleRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.io.File;
import java.io.IOException;
import java.time.Instant;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.stream.Collectors;

@Service
@Slf4j
public class ScheduleService {
    private final static String SCHEDULE_TOPIC = "schedule";
    private final static String MODIFY_TOPIC = "update";
    private final static String DELETE_TOPIC = "delete";
    private final SubjectService subjectService;
    private final UserService userService;
    private final ScheduleRepository scheduleRepository;
    private final KafkaTemplate<String, Object> kafkaTemplate;
    private final FirebaseService firebaseService;
    private final RedisRepository redisRepository;

    @Autowired
    public ScheduleService(SubjectService subjectService, UserService userService, ScheduleRepository scheduleRepository, KafkaTemplate<String, Object> kafkaTemplate, FirebaseService firebaseService, RedisRepository redisRepository) {
        this.subjectService = subjectService;
        this.userService = userService;
        this.scheduleRepository = scheduleRepository;
        this.kafkaTemplate = kafkaTemplate;
        this.firebaseService = firebaseService;
        this.redisRepository = redisRepository;
    }

    public String registerSchedule(ScheduleRequest scheduleRequest) throws IOException {
        int semester = scheduleRequest.getSemester();
        String subjectID = scheduleRequest.getSubjectID();
        String groupCode = scheduleRequest.getGroupCode();
        if (!checkOverlap(scheduleRequest.getDeviceID(), scheduleRequest.getStartTime(), scheduleRequest.getEndTime())) {
            Schedule schedule = ScheduleMapper.toModel(scheduleRequest);
            String classCode = String.format("%d_%s_%s", semester, subjectID, groupCode);
            cacheNewSchedule(scheduleRequest, classCode);
            String lastMetaData = firebaseService.downloadMetadata(classCode);
            Map<String, Object> studentPath = getStudentDifferences(semester, subjectID, groupCode);
            Map<String, Object> message = new HashMap<>();
            message.put("request", scheduleRequest);
            message.put("student", studentPath.get("differences"));
            message.put("haveAttendance", studentPath.get("haveAttendance"));
            message.put("lastMetaDataPath", lastMetaData);
            scheduleRepository.save(schedule);
            scheduleRequest.setId(schedule.getId());
            kafkaTemplate.send(SCHEDULE_TOPIC, message);
            return "Successfully";
        }
        return "Overlaps";
    }

    public void cacheNewSchedule(ScheduleRequest scheduleRequest, String classCode) {
        redisRepository.delete(classCode);
        SubjectIDDto subjectID = new SubjectIDDto(scheduleRequest.getSubjectID(), scheduleRequest.getGroupCode(), scheduleRequest.getSemester());
        SubjectDto subjectToRegister = subjectService.find(subjectID);
        List<Integer> studentList = subjectToRegister.getUserDtos().stream().map(UserDto::getId).collect(Collectors.toList());
        List<Integer> studentHaveCheckedAttendance = new ArrayList<>();
        CacheAttendance cacheAttendance = CacheAttendance.builder()
                .classCode(classCode)
                .studentList(studentList)
                .studentHaveAttendances(studentHaveCheckedAttendance)
                .startTime(scheduleRequest.getStartTime())
                .endTime(scheduleRequest.getEndTime())
                .build();
        redisRepository.save(cacheAttendance);
    }

    public Map<String, Object> getStudentDifferences(int semester, String subjectID, String groupCode) throws IOException {
        List<String> users = subjectService.findAllUsersTakeSubject(semester, subjectID, groupCode)
                .stream()
                .map(user -> String.valueOf(user.getId()))
                .collect(Collectors.toList());
        List<String> allPath = firebaseService.listFiles("student");
        List<String> pathList = firebaseService.filterPathWithStudentList(allPath, users);

        Set<String> studentHaveAttendances = findStudentHaveCheckedAttendance(pathList);

        List<String> studentInMetaData = loadMetadata();
        pathList.removeAll(studentInMetaData);

        Map<String, Object> studentPath = new HashMap<>();
        studentPath.put("differences", pathList);
        studentPath.put("haveAttendance", studentHaveAttendances);
        return studentPath;
    }

    public Set<String> findStudentHaveCheckedAttendance(List<String> pathList) {
        return pathList.stream().filter(p -> p.contains("attendance")).map(p -> {
            String[] pathElements = p.split("/", -1);
            return pathElements[1];
        }).collect(Collectors.toSet());
    }

    private List<String> loadMetadata() throws IOException {
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> temp = mapper.readValue(new File("/tmp/schedule.json"), Map.class);
        return (List<String>) temp.get("student_path_list");
    }

    public ScheduleRequest updateSchedule(ScheduleRequest request) {
        Optional<Schedule> schedule = scheduleRepository.findById(request.getId());
        if (schedule.isPresent()) {
            schedule.get().setStartTime(request.getStartTime());
            schedule.get().setEndTime(request.getEndTime());
            Schedule scheduleUpdated = scheduleRepository.save(schedule.get());
            kafkaTemplate.send(MODIFY_TOPIC, scheduleUpdated);
            return ScheduleMapper.toDto(scheduleUpdated);
        }
        throw CustomException.throwException(EntityType.SCHEDULE, ExceptionType.ENTITY_EXCEPTION, String.valueOf(request.getId()));
    }


    public void deleteSchedule(ScheduleRequest request) {
        Optional<Schedule> schedule = scheduleRepository.findById((request.getId()));
        if (schedule.isPresent()) {
            scheduleRepository.delete(schedule.get());
            kafkaTemplate.send(DELETE_TOPIC, schedule.get());
        }
        throw CustomException.throwException(EntityType.SCHEDULE, ExceptionType.ENTITY_EXCEPTION, String.valueOf(request.getId()));
    }

    public List<ScheduleRequest> fetch(int userid) {
        userService.find(userid);
        return scheduleRepository.findByTeacherID(userid)
                .stream().map(ScheduleMapper::toDto)
                .collect(Collectors.toList());
    }

    public Optional<Schedule> existScheduleRightNow(Integer deviceID) {
        String now = ZonedDateTime.ofInstant(Instant.now(), ZoneId.of("Asia/Ho_Chi_Minh")).format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
        return Optional.ofNullable(scheduleRepository.findByDeviceIDAndStartTimeBeforeAndEndTimeAfter(deviceID, now, now));
    }

    public Optional<Schedule> fetchOne(Integer deviceID, String timestamp) {
        return Optional.ofNullable(scheduleRepository.findByDeviceIDAndStartTimeBeforeAndEndTimeAfter(deviceID, timestamp, timestamp));
    }


    public boolean checkOverlap(Integer deviceID, String startTime, String endTime) {
        List<Schedule> schedules = scheduleRepository.findByDeviceIDAndEndTimeAfterOrderByEndTime(deviceID, startTime);
        Optional<Schedule> minEndTimeSchedule = schedules.stream().findFirst();
        return minEndTimeSchedule.filter(schedule -> endTime.compareTo(schedule.getStartTime()) > 0).isPresent();
    }

    public Integer countSchedulesWithID(int semester, String subjectID, String groupCode) {
        return scheduleRepository.countScheduleBySemesterAndSubjectIDAndGroupCode(semester, subjectID, groupCode);
    }
}
