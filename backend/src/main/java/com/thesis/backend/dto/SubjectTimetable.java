package com.thesis.backend.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.apache.tomcat.jni.Local;

import javax.persistence.*;
import java.time.LocalTime;
import java.time.OffsetTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;

@Entity
@Table(name = "subject_timetable")
@Data
@AllArgsConstructor
@RequiredArgsConstructor
public class SubjectTimetable {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private int id;

    @ManyToOne
    @JoinColumn(name = "subject_id")
    private Subject subject;

    @Column(name = "start_time")
    private String start_time;

    @Column(name = "end_time")
    private String end_time;

    @Column(name = "day_in_week")
    private int day_in_week;
}
