package com.thesis.backend.util;

import java.nio.charset.StandardCharsets;
import java.util.Base64;

public final class ImageUtil {
    public static byte[] base64ToBytesArray(String base64) {
        try {
            return Base64.getDecoder().decode(base64.getBytes(StandardCharsets.UTF_8));
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
