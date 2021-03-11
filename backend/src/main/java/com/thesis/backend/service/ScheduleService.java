package com.thesis.backend.service;

import com.thesis.backend.model.Schedule;
import com.thesis.backend.repository.mysql.ScheduleRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.sql.Timestamp;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@Slf4j
public class ScheduleService {

    private final ScheduleRepository scheduleRepository;

    @Autowired
    public ScheduleService(ScheduleRepository scheduleRepository) {
        this.scheduleRepository = scheduleRepository;
    }

    public Schedule save(Schedule schedule) {
        return scheduleRepository.save(schedule);
    }

    public boolean checkOverlap(Integer deviceID, LocalDateTime startTime, LocalDateTime endTime) {
        Timestamp startTimeTS = Timestamp.valueOf(startTime);
        Timestamp endTimeTS = Timestamp.valueOf(endTime);
        List<Schedule> schedules = scheduleRepository.findByDeviceIDAndEndTimeAfterOrderByEndTime(deviceID, startTimeTS);
        Optional<Schedule> minEndTimeSchedule = schedules.stream().findFirst();
        if (minEndTimeSchedule.isPresent()) {
            if (endTimeTS.getTime() > minEndTimeSchedule.get().getStartTime().getTime()) {
                return true;
            }
        }
        return false;
    }
}
