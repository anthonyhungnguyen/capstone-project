package com.thesis.backend.service;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.storage.*;
import com.google.firebase.FirebaseApp;
import com.google.firebase.FirebaseOptions;
import com.google.firebase.cloud.StorageClient;
import com.thesis.backend.config.props.FirebaseProperties;
import com.thesis.backend.util.ImageUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;

@Service
@Slf4j
public class FirebaseService {
    private Storage storage;
    private final FirebaseProperties firebaseProperties;

    @Autowired
    public FirebaseService(FirebaseProperties firebaseProperties) {
        this.firebaseProperties = firebaseProperties;
    }

    @EventListener
    public void init(ApplicationReadyEvent event) {
        try {
            ClassPathResource serviceAccount = new ClassPathResource(firebaseProperties.getServiceAccountPath());
            storage = StorageOptions.newBuilder()
                    .setCredentials(GoogleCredentials.fromStream(serviceAccount.getInputStream()))
                    .build().getService();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public String downloadMetadata(String classCode) {
        List<String> metadataList = listFiles("subject/" + classCode).stream().filter(l -> l.contains("json")).collect(Collectors.toList());
        String lastMeta = metadataList.get(metadataList.size() - 1);
        Blob blob = storage.get(BlobId.of(firebaseProperties.getBucketName(), lastMeta));
        blob.downloadTo(Paths.get("/home/phuchung/temp.json"));
        return lastMeta;
    }

    public List<String> listFiles(String prefix) {
        List<String> path = new ArrayList<>();
        Iterable<Blob> blobIterator = storage.list(firebaseProperties.getBucketName(), Storage.BlobListOption.prefix(prefix)).iterateAll();
        blobIterator.forEach(blob -> {
            path.add(blob.getName());
        });
        return path;
    }

    public List<String> filterPathWithStudentList(List<String> path, List<String> studentList) {
        return path.stream().filter(p -> {
            try {
                String[] pathElements = p.split("/", -1);
                String rootFolder = pathElements[0];
                String studentID = pathElements[1];
                String fileName = pathElements[pathElements.length - 1];
                String[] fileNameAndExtension = fileName.split("\\.", -1);
                String fileExtension = fileNameAndExtension[1];
                return rootFolder.equals("student") && studentList.contains(studentID) && fileExtension.equals("npy");
            } catch (Exception e) {
                System.out.println(p);
                return true;
            }
        }).collect(Collectors.toList());
    }

    public String saveImg(String base64, String studentID, String timestamp) throws IOException {
        Map<String, String> newMap = new HashMap<>();
        String token = UUID.randomUUID().toString();
        newMap.put("firebaseStorageDownloadTokens", token);
        String path = String.format("student/%s/attendance/photos/%s.jpg", studentID, timestamp);
        BlobId blobId = BlobId.of(firebaseProperties.getBucketName(), path);
        BlobInfo blobInfo = BlobInfo.newBuilder(blobId)
                .setMetadata(newMap)
                .setContentType("image/jpeg")
                .build();
        Blob blob = storage.create(blobInfo, ImageUtil.base64ToBytesArray(base64));
        String mediaLink = "https://firebasestorage.googleapis.com/v0/" + blob.getMediaLink().split("/", 7)[6] + "&token=" + token;
        log.info("Blob ID {}", mediaLink);

        return mediaLink;
    }
}
