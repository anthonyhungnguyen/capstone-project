package com.thesis.backend;

import okhttp3.Call;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringRunner;

import java.io.IOException;

import static org.junit.jupiter.api.Assertions.assertEquals;

@RunWith(SpringRunner.class)
@SpringBootTest
public class OkHttpTest {

    @Autowired
    private OkHttpClient client;

    @Test
    public void testGetGoogle() throws IOException {
        Request request = new Request.Builder()
                .url("https://google.com.vn")
                .build();
        Call call = client.newCall(request);
        Response response = call.execute();
        assertEquals(response.code(), 200);
    }
}
