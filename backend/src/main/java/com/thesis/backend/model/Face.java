package com.thesis.backend.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;
import org.bson.types.Binary;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "faces")
@Data
@Builder
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
public class Face {
    @Field(value = "_id")
    private String id;

    @Field(value = "userId")
    private Integer userId;

    @Field(value = "photo")
    private String photo;

    @Field(value = "status")
    private String status;

    @Field(value = "timestamp")
    private String timestamp;

    @Field(value = "isAugmented")
    private Boolean isAugmented;

    @Field(value = "augmentSource")
    private String source;
}
