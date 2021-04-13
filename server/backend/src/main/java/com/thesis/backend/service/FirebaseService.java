package com.thesis.backend.service;

import com.google.auth.oauth2.GoogleCredentials;
import com.google.cloud.storage.*;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class FirebaseService {
    private Storage storage;

    @EventListener
    public void init(ApplicationReadyEvent event) {
        try {
            ClassPathResource serviceAccount = new ClassPathResource("serviceAccount.json");
            storage = StorageOptions.newBuilder().
                    setCredentials(GoogleCredentials.fromStream(serviceAccount.getInputStream())).
                    setProjectId("YOUR_PROJECT_ID").build().getService();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public String downloadMetadata(String classCode) {
        List<String> metadataList = listFiles("subject/" + classCode).stream().filter(l -> l.contains("json")).collect(Collectors.toList());
        String lastMeta = metadataList.get(metadataList.size() - 1);
        Blob blob = storage.get(BlobId.of("capstone-bk.appspot.com", lastMeta));
        blob.downloadTo(Paths.get("/home/phuchung/temp.json"));
        return lastMeta;
    }

    public List<String> listFiles(String prefix) {
        List<String> path = new ArrayList<>();
        Iterable<Blob> blobIterator = storage.list("capstone-bk.appspot.com", Storage.BlobListOption.prefix(prefix)).iterateAll();
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

    public String saveMetadata(MultipartFile file, Map<String, String> map) throws IOException {
        String imageName = generateFileName(file.getOriginalFilename());
        Map<String, String> newMap = new HashMap<>();
        newMap.put("firebaseStorageDownloadTokens", imageName);
        BlobId blobId = BlobId.of("YOUR_BUCKET_NAME", imageName);
        BlobInfo blobInfo = BlobInfo.newBuilder(blobId)
                .setMetadata(newMap)
                .setContentType(file.getContentType())
                .build();
        storage.create(blobInfo, file.getInputStream());
        return imageName;
    }

    private String generateFileName(String originalFileName) {
        return UUID.randomUUID().toString() + "." + getExtension(originalFileName);
    }

    private String getExtension(String originalFileName) {
        return StringUtils.getFilenameExtension(originalFileName);
    }
}
