package com.thesis.backend.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;

@AllArgsConstructor
@RequiredArgsConstructor
@Data
@Builder
@Entity
@Table(name = "user")
public class User {
    @Id
    @NotBlank(message = "Student ID is Mandatory")
    private String id;
    @NotBlank(message = "User Name is Mandatory")
    private String name;
    private Timestamp register_at;
    private String image_link;

    @OneToMany(targetEntity = UserSubject.class, mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JsonIgnore
    private List<UserSubject> userSubjects;

    @PrePersist
    void registerAtOnCreation() {
        this.register_at = new Timestamp(System.currentTimeMillis());
    }

    @PreUpdate
    void registerAtOnUpdate() {
        this.register_at = new Timestamp(System.currentTimeMillis());
    }
}
