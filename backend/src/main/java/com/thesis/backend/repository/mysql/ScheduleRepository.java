package com.thesis.backend.repository.mysql;

import com.thesis.backend.model.Schedule;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

import java.sql.Timestamp;
import java.util.List;

@Repository
@Transactional
public interface ScheduleRepository extends JpaRepository<Schedule, Integer> {
    List<Schedule> findByDeviceIDAndEndTimeAfterOrderByEndTime(Integer deviceID, Timestamp startTimeInsert);
}
