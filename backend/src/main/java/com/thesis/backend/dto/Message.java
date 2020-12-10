package com.thesis.backend.dto;

import lombok.*;

import javax.persistence.Entity;
import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@RequiredArgsConstructor
@Builder
@Getter
@Setter
public class Message {
    private boolean status;
    private String message;
}
