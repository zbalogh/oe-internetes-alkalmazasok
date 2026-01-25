package hu.uni.mvclab.service;

import hu.uni.mvclab.dto.User;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Service layer for User management
 * Uses ConcurrentHashMap for thread-safe in-memory storage
 * Uses AtomicLong for thread-safe ID generation
 */
@Service
public class UserService {

    // In-memory data store
    private final ConcurrentHashMap<Long, User> userStore = new ConcurrentHashMap<>();

    // AtomicLong for generating unique user IDs
    private final AtomicLong idGenerator = new AtomicLong(1);

    public UserService()
    {
        // Initialize with some sample data for demonstration
        createUser(new User(null, "John", "Doe", "john.doe@example.com"));
        createUser(new User(null, "Jane", "Smith", "jane.smith@example.com"));
        createUser(new User(null, "Bob", "Johnson", "bob.johnson@example.com"));
    }

    /**
     * Get all users
     * @return List of all users
     */
    public List<User> getAllUsers()
    {
        return new ArrayList<>(userStore.values());
    }

    /**
     * Get user by ID
     * @param id User ID
     * @return User object or null if not found
     */
    public User getUserById(Long id)
    {
        return userStore.get(id);
    }

    /**
     * Create a new user
     * @param user User object (ID will be auto-generated)
     * @return Created user with assigned ID
     */
    public User createUser(User user)
    {
        Long id = idGenerator.getAndIncrement();
        user.setId(id);
        userStore.put(id, user);
        return user;
    }

    /**
     * Update an existing user
     * @param id User ID
     * @param updatedUser Updated user data
     * @return Updated user or null if user not found
     */
    public User updateUser(Long id, User updatedUser)
    {
        if (userStore.containsKey(id)) {
            updatedUser.setId(id);
            userStore.put(id, updatedUser);
            return updatedUser;
        }
        return null;
    }

    /**
     * Delete a user
     * @param id User ID
     * @return true if deleted, false if user not found
     */
    public boolean deleteUser(Long id)
    {
        return userStore.remove(id) != null;
    }

    /**
     * Check if user exists
     * @param id User ID
     * @return true if exists, false otherwise
     */
    public boolean userExists(Long id)
    {
        return userStore.containsKey(id);
    }

}
