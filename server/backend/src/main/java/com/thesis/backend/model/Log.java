package com.thesis.backend.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

import javax.persistence.*;

@Data
@Builder
@Entity
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "attendance_log")
public class Log {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(name = "user_id")
    private Integer userID;

    @Column(name = "semester")
    private Integer semester;

    @Column(name = "group_code")
    private String groupCode;

    @Column(name = "subject_id")
    private String subjectID;

    @Column(name = "teacher_id")
    private Integer teacherID;

    @Column(name = "attendance_time")
    private String attendanceTime;

    @Column(name = "device_id")
    private Integer deviceID;

    @Column(name = "image_link")
    private String imageLink;
}
