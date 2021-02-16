package com.thesis.backend.service;

import org.springframework.stereotype.Service;

@Service
public interface BaseService<T, E> {
    T find(E id);

    T create(T o);

    void delete(E o);

    T update(T updateObject);
}
