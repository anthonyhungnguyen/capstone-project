package com.thesis.backend.util;

import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.temporal.ChronoUnit;
import java.time.temporal.WeekFields;
import java.util.Date;
import java.util.Locale;

public class DateUtil {
    public static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
    public static final String zoneId = "Asia/Ho_Chi_Minh";

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
