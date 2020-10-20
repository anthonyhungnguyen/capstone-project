package com.thesis.backend.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import java.time.LocalDateTime;
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
    private LocalDateTime register_at;
    private LocalDateTime update_at;
    private String image_link;

    @OneToMany(targetEntity = UserSubject.class, mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JsonIgnore
    private List<UserSubject> userSubjects;

    @PrePersist
    void onPersist() {
        this.register_at = LocalDateTime.now().plusHours(7);
    }

    @PreUpdate
    void onUpdate() {
        this.update_at = LocalDateTime.now().plusHours(7);
    }
}
