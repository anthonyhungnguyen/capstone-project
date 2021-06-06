package com.thesis.backend.repository;

import com.thesis.backend.model.CacheAttendance;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;


@Component
public class RedisRepository {
    @Autowired
    private RedisTemplate<String, CacheAttendance> cacheAttendanceTemplate;

    public void save(CacheAttendance cacheAttendance) {
        cacheAttendanceTemplate.opsForValue()
                .set(cacheAttendance.getClassCode(), cacheAttendance);
    }

    public void delete(String id) {
        cacheAttendanceTemplate.delete(id);
    }

    public CacheAttendance findById(String id) {
        return cacheAttendanceTemplate.opsForValue()
                .get(id);
    }
}
