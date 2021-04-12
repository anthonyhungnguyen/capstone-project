package com.thesis.backend.util;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public final class StringUtil {
    public static List<Integer> convertRawWeekScheduleToList(String weekString) {
        return Arrays.stream(weekString
                .split("\\|", 0))
                .filter(x -> !x.equals("--"))
                .map(Integer::parseInt)
                .collect(Collectors.toList());
    }

    public static List<String> convertRawTimeRangeToList(String raw) {
        return Arrays.asList(raw.split("-", 0).clone());
    }
}
