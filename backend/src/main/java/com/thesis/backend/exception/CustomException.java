package com.thesis.backend.exception;

import com.thesis.backend.config.PropertiesConfig;
import com.thesis.backend.constant.EntityType;
import com.thesis.backend.constant.ExceptionType;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.text.MessageFormat;
import java.util.Optional;

@Component
public class CustomException {
    private static PropertiesConfig propertiesConfig;

    @Autowired
    public CustomException(PropertiesConfig propertiesConfig) {
        CustomException.propertiesConfig = propertiesConfig;
    }

    public static class EntityNotFoundException extends RuntimeException {
        public EntityNotFoundException(String message) {
            super(message);
        }
    }

    public static class DuplicateEntityException extends RuntimeException {
        public DuplicateEntityException(String message) {
            super(message);
        }
    }

    private static String format(String template, String... args) {
        // https://stackoverflow.com/questions/2809633/what-is-the-difference-between-messageformat-format-and-string-format-in-jdk-1-5
        Optional<String> templateContent = Optional.ofNullable(propertiesConfig.getConfigValue(template));
        return templateContent.map(s -> MessageFormat.format(s, (Object[]) args)).orElseGet(() -> String.format(template, (Object) args));
    }

    private static String getMessageTemplate(EntityType entityType, ExceptionType exceptionType) {
        return entityType.name().concat(".").concat(exceptionType.getValue()).toLowerCase();
    }

    private static RuntimeException throwException(ExceptionType exceptionType, String messageTemplate, String... args) {
        if (ExceptionType.ENTITY_NOT_FOUND.equals(exceptionType)) {
            return new EntityNotFoundException(format(messageTemplate, args));
        } else if (ExceptionType.DUPLICATE_ENTITY.equals(exceptionType)) {
            return new DuplicateEntityException(format(messageTemplate, args));
        }
        return new RuntimeException(format(messageTemplate, args));
    }

    public static RuntimeException throwException(String messageTemplate, String... args) {
        return new RuntimeException(format(messageTemplate, args));
    }

    public static RuntimeException throwException(EntityType entityType,
                                                  ExceptionType exceptionType,
                                                  String... args) {
        String messageTemplate = getMessageTemplate(entityType, exceptionType);
        return throwException(exceptionType, messageTemplate, args);
    }

    public static RuntimeException throwExceptionWithId(EntityType entityType,
                                                        ExceptionType exceptionType,
                                                        Integer id,
                                                        String... args) {
        String messageTemplate = getMessageTemplate(entityType, exceptionType).concat(".").concat(id.toString());
        return throwException(exceptionType, messageTemplate, args);
    }

    public static RuntimeException throwExceptionWithTemplate(ExceptionType exceptionType,
                                                              String messageTemplate,
                                                              String... args) {
        return throwException(exceptionType, messageTemplate, args);
    }

}
