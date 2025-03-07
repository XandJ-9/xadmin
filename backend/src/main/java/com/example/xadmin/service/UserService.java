package com.example.xadmin.service;

import com.example.xadmin.entity.User;
import java.util.List;

public interface UserService {
    User createUser(User user);
    User updateUser(Long id, User user);
    void deleteUser(Long id);
    User getUserById(Long id);
    List<User> getAllUsers();
    User findByUsername(String username);
    boolean existsByUsername(String username);
}