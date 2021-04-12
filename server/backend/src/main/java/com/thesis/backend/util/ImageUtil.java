package com.thesis.backend.util;

import java.util.Base64;

public final class ImageUtil {
    public static byte[] base64ToBytesArray(String base64) {
        try {
            return Base64.getDecoder().decode(new String(base64).getBytes("UTF-8"));
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
