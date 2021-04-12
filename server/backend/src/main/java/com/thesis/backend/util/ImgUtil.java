package com.thesis.backend.util;


import org.apache.tomcat.util.codec.binary.Base64;
import org.apache.tomcat.util.codec.binary.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

public final class ImgUtil {
    public static String convertImgToBase64(MultipartFile img) throws IOException {
        return "data:image/png;base64," +
                StringUtils.newStringUtf8(Base64.encodeBase64(img.getBytes(), false));
    }
}
