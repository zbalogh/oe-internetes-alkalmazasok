package hu.uni.restlab.service;

import hu.uni.restlab.controller.UserResponse;
import hu.uni.restlab.model.User;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * Service class for managing user business logic.
 *
 * This service handles all business operations related to users,
 * including CRUD operations and data validation.
 * For demo purposes, users are stored in an in-memory store.
 */
@Service
public class UserService {

    // For demo purposes the users are stored in-memory store by using HashMap.
    // Note: a real application would persist them in a database.
    private final Map<Long, User> users = new ConcurrentHashMap<>();

    // AtomicLong provides a simple thread-safe id generator.
    // Note: normally the database would manage identifiers.
    private final AtomicLong idSeq = new AtomicLong(0);

    /**
     * Constructor seeds the in-memory store with a few demo users.
     */
    public UserService()
    {
        // Populate the map with demo data.
        long id1 = idSeq.incrementAndGet();
        users.put(id1, new User(id1, "Alice", "alice@example.com"));

        long id2 = idSeq.incrementAndGet();
        users.put(id2, new User(id2, "Bob", "bob@example.com"));
    }

    /**
     * Retrieves all users from the store.
     *
     * @return list of all users sorted by id
     */
    public List<User> findAllUsers()
    {
        // Return all users sorted by the id property.
        // Note: in real life this would be done via a database query.
        return users.values().stream()
                .sorted(Comparator.comparingLong(User::getId))
                .toList();
    }

    /**
     * Finds a user by their unique identifier.
     *
     * @param id the user's id
     * @return Optional containing the user if found, empty otherwise
     */
    public Optional<User> findUserById(long id)
    {
        return Optional.ofNullable(users.get(id));
    }

    /**
     * Creates a new user with the provided data.
     *
     * @param name the user's name
     * @param email the user's email address
     * @return the created user with assigned id
     */
    public User createUser(String name, String email)
    {
        // Generate a new id and construct the user.
        long id = idSeq.incrementAndGet();
        User user = new User(id, name, email);

        // Store the user in the map.
        users.put(id, user);

        return user;
    }

    /**
     * Updates an existing user with new data.
     *
     * @param id the user's id
     * @param name the new name
     * @param email the new email address
     * @return Optional containing the updated user if found, empty otherwise
     */
    public Optional<User> updateUser(long id, String name, String email)
    {
        // Check if the user exists.
        if (!users.containsKey(id)) {
            return Optional.empty();
        }

        // Update the user data and replace it in the map.
        User updated = new User(id, name, email);
        users.put(id, updated);

        return Optional.of(updated);
    }

    /**
     * Deletes a user by their unique identifier.
     *
     * @param id the user's id
     * @return true if the user was deleted, false if not found
     */
    public boolean deleteUser(long id)
    {
        // Remove the user from the map; remove returns the old value or null if missing.
        User removed = users.remove(id);

        // Return true if a user was actually removed.
        return removed != null;
    }

    /**
     * Converts a User entity to a UserResponse DTO.
     *
     * @param user the user entity
     * @return the user response DTO
     */
    public UserResponse toResponse(User user)
    {
        return new UserResponse(user.getId(), user.getName(), user.getEmail());
    }

}
