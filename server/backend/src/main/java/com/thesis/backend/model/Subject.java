package com.thesis.backend.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.*;
import lombok.experimental.Accessors;

import javax.persistence.*;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

@Data
@Accessors(chain = true)
@Builder
@Entity
@AllArgsConstructor
@NoArgsConstructor
@Table(name = "subject")
@IdClass(SubjectId.class)
public class Subject implements Serializable {
    @Id
    private String id;

    @Id
    @Column(name = "group_code")
    private String groupCode;

    @Id
    private int semester;

    private String name;

    @ManyToMany(targetEntity = User.class,
            mappedBy = "subjects", fetch = FetchType.EAGER)
    @ToString.Exclude
    @JsonIgnore
    private List<User> users = new ArrayList<>();
}
