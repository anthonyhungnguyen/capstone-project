package com.thesis.backend.util;

import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.time.temporal.WeekFields;
import java.util.Date;
import java.util.Locale;

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

    public static String todayStr() {
        return sdf.format(today());
    }

    public static LocalTime localTime() {
        return today().toLocalTime();
    }

    public static LocalDate localDate() {
        return today().toLocalDate();
    }


    public static int dayOfWeek() {
        return localDate().getDayOfWeek().getValue() + 1;
    }

    public static int weekOfYear() {
        return today().toLocalDate().get(WeekFields.of(Locale.ENGLISH).weekOfYear());
    }

    public static String formatDate(Date date) {
        return date == null ? todayStr() : sdf.format(date);
    }

    // Hour needs to be at format: HH:MM, so if we cannot parse hour because of H:MM
    // add 0 at the beginning
    public static LocalTime convertTimeStringToLocalTimeObject(String time) {
        try {
            return LocalTime.parse(time.trim());
        } catch (Exception e) {
            return LocalTime.parse("0" + time.trim());
        }
    }

    public static long timeDifferenceInMinutes(LocalTime a, LocalTime b) {
        return a.until(b, ChronoUnit.MINUTES);
    }
}
