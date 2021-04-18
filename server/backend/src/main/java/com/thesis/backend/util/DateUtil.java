package com.thesis.backend.util;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

public final class DateUtil {
    public static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
    public static final String zoneId = "Asia/Ho_Chi_Minh";

    public static LocalDateTime convertStringToLocalDateTime(String ldt) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        return LocalDateTime.parse(ldt, formatter);

    }

    public static Timestamp convertStringToTimestamp(String time) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        LocalDateTime dateTime = LocalDateTime.parse(time, formatter);
        return Timestamp.valueOf(dateTime);
    }

    public static ZonedDateTime today() {
        return ZonedDateTime.now(ZoneId.of(zoneId));
    }

}
