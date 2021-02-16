package com.thesis.backend.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.*;
import lombok.experimental.Accessors;

import javax.persistence.*;
import javax.validation.constraints.NotBlank;
import java.io.Serializable;
import java.util.List;

@Data
@Accessors(chain = true)
@Builder
@Entity
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "user")
public class User implements Serializable {
    @Id
    private int id;

    @NotBlank
    private String name;

    @NotBlank
    private int gender;

    @Column(name = "major_code")
    @NotBlank
    private String majorCode;

    @ManyToMany(targetEntity = Subject.class,
            cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinTable(name = "enrollment",
            joinColumns = {
                    @JoinColumn(name = "user_id", referencedColumnName = "id")
            },
            inverseJoinColumns = {
                    @JoinColumn(name = "subject_id", referencedColumnName = "id"),
                    @JoinColumn(name = "group_code", referencedColumnName = "group_code"),
                    @JoinColumn(name = "semester", referencedColumnName = "semester")
            })
    @ToString.Exclude
    @JsonIgnore
    private List<Subject> subjects;
}
