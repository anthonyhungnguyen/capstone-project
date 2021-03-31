package com.thesis.backend.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.*;
import lombok.experimental.Accessors;

import javax.persistence.*;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

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

    private String password;

    @ManyToMany(targetEntity = Subject.class,
            cascade = CascadeType.ALL, fetch = FetchType.EAGER)
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
    private List<Subject> subjects = new ArrayList<>();

    @ManyToMany(targetEntity = Role.class, fetch = FetchType.EAGER)
    @JoinTable(name = "user_role",
            joinColumns = @JoinColumn(name = "user_id", referencedColumnName = "id"),
            inverseJoinColumns = @JoinColumn(name = "role_id", referencedColumnName = "id"))
    private Set<Role> roles = new HashSet<>();


}