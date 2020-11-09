package com.thesis.backend.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import java.sql.Blob;
import java.util.List;

@AllArgsConstructor
@RequiredArgsConstructor
@Data
@Builder
@Entity
@Table(name = "user")
public class User {
    @Id
    @NotBlank(message = "Student ID is required")
    private int id;
    @NotBlank(message = "User Name is required")
    private String name;

    @NotBlank(message = "Gender is required")
    private int gender;

    @Column(name = "major_code")
    private String majorCode;

    // signifies that the annotated field should be represented as BLOB (binary data) in the DataBase.
    @Lob
    @Column(name = "image_url")
    private Blob imageUrl;

    @OneToMany(targetEntity = Enrollment.class, mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Enrollment> enrollments;
}
