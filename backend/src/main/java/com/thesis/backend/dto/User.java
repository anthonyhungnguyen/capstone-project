package com.thesis.backend.dto;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import lombok.*;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import java.util.List;

@AllArgsConstructor
@RequiredArgsConstructor
@Getter
@Setter
@Builder
@Entity
@Table(name = "user")
public class User {
    @Id
    @NotNull(message = "Student ID cannot be null")
    private int id;
    @NotBlank(message = "User Name is required")
    private String name;

    @NotNull(message = "Gender cannot be null")
    private int gender;

    @Column(name = "major_code")
    private String majorCode;

    // signifies that the annotated field should be represented as BLOB (binary data) in the DataBase.
//    @Lob
//    @Column(name = "image_url")
//    private Blob imageUrl;

    @ManyToMany(fetch = FetchType.LAZY, cascade = CascadeType.PERSIST)
    @JoinTable(name = "enrollment", joinColumns = {
            @JoinColumn(name = "user_id", referencedColumnName = "id",
                    nullable = false, updatable = false)
    }, inverseJoinColumns = {
            @JoinColumn(name = "subject_id", referencedColumnName = "id", nullable = false, updatable = false),
            @JoinColumn(name = "group_code", referencedColumnName = "groupCode", nullable = false, updatable = false),
            @JoinColumn(name = "semester", referencedColumnName = "semester", nullable = false, updatable = false)
    })
    private List<Subject> subjects;

}
