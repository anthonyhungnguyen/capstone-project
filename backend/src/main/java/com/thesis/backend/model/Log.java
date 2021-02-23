package com.thesis.backend.model;

import com.thesis.backend.util.DateUtil;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import javax.persistence.PrePersist;
import java.time.ZonedDateTime;

@Document(collection = "attendance_log")
@Data
@Builder
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
public class Log {
    @Field(value = "userId")
    private Integer userId;

    @Field(value = "semester")
    private int semester;

    @Field(value = "groupCode")
    private String groupCode;

    @Field(value = "subjectID")
    private String subjectID;

    @Field(value = "type")
    private String type;

    @Field(value = "timestamp")
    private String timestamp;

}
