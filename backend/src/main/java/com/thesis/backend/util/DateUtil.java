package com.thesis.backend.util;

import java.text.SimpleDateFormat;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Date;

public class DateUtil {
    public static final SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");

    public static ZonedDateTime today() {
        return ZonedDateTime.now(ZoneId.of("Asia/Ho_Chi_Minh"));
    }

    public static String todayStr() {
        return sdf.format(today());
    }

    public static String formatDate(Date date) {
        return date == null ? todayStr() : sdf.format(date);
    }

}
