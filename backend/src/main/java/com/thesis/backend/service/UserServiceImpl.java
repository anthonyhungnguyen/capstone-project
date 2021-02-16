package com.thesis.backend.service;

import com.thesis.backend.dto.model.UserDto;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.UserRepository;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

import static com.thesis.backend.constant.EntityType.USER;
import static com.thesis.backend.constant.ExceptionType.DUPLICATE_ENTITY;
import static com.thesis.backend.constant.ExceptionType.ENTITY_NOT_FOUND;

@Service
public class UserServiceImpl implements BaseService<UserDto, Integer>, UserService {
    private final UserRepository userRepository;
    private final ModelMapper modelMapper;

    @Autowired
    public UserServiceImpl(UserRepository userRepository, ModelMapper modelMapper) {
        this.userRepository = userRepository;
        this.modelMapper = modelMapper;
    }


    @Override
    public UserDto find(Integer id) {
        Optional<User> user = userRepository.findById(id);
        if (user.isPresent()) {
            return modelMapper.map(user.get(), UserDto.class);
        }
        throw CustomException.throwException(USER, ENTITY_NOT_FOUND, id.toString());
    }

    @Override
    public UserDto create(UserDto userDto) {
        Optional<User> user = userRepository.findById(userDto.getId());
        if (user.isEmpty()) {
            User mapToUser = modelMapper.map(userDto, User.class);
            return modelMapper.map(userRepository.save(mapToUser), UserDto.class);
        }
        throw CustomException.throwException(USER, DUPLICATE_ENTITY, String.valueOf(userDto.getId()));
    }

    @Override
    public void delete(Integer id) {
        Optional<User> user = userRepository.findById(id);
        if (user.isPresent()) {
            userRepository.delete(modelMapper.map(user.get(), User.class));
            return;
        }
        throw CustomException.throwException(USER, ENTITY_NOT_FOUND, id.toString());
    }

    @Override
    public UserDto update(UserDto o) {
        Optional<User> user = userRepository.findById(o.getId());
        if (user.isPresent()) {
            User userToSave = modelMapper.map(o, User.class);
            return modelMapper.map(userRepository.save(userToSave), UserDto.class);
        }
        throw CustomException.throwException(USER, ENTITY_NOT_FOUND, String.valueOf(o.getId()));
    }

}
