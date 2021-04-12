package com.thesis.backend.security.services;

import com.thesis.backend.constant.EntityType;
import com.thesis.backend.constant.ExceptionType;
import com.thesis.backend.exception.CustomException;
import com.thesis.backend.model.User;
import com.thesis.backend.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    private final UserRepository userRepository;

    @Autowired
    public UserDetailsServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String id) throws UsernameNotFoundException {
        User user = userRepository.findById(Integer.valueOf(id)).orElseThrow(
                () -> CustomException.throwException(EntityType.USER,
                        ExceptionType.ENTITY_NOT_FOUND,
                        id)
        );
        return new UserDetailsImpl(user);
    }
}
