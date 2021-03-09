package com.thesis.backend.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.thesis.backend.constant.ERole;
import lombok.Data;
import lombok.ToString;
import lombok.experimental.Accessors;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Data
@Accessors(chain = true)
@Entity
@Table(name = "role")
public class Role {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Enumerated(EnumType.STRING)
    @Column(length = 20)
    private ERole name;

    @ManyToMany(targetEntity = User.class,
            mappedBy = "roles", fetch = FetchType.LAZY)
    @ToString.Exclude
    @JsonIgnore
    private List<User> users = new ArrayList<>();
}
