package hu.uni.restlab.controller;

import hu.uni.restlab.dto.UserCreateRequest;
import hu.uni.restlab.dto.UserResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.security.SecurityRequirement;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

/**
 * REST controller for managing users.
 *
 * This controller provides CRUD operations for user resources.
 * It uses an in-memory store for demonstration purposes.
 * All endpoints require JWT authentication.
 */
@RestController
@RequestMapping("/api/v1/users")
@Tag(name = "Users", description = "User management endpoints (requires JWT authentication)")
@SecurityRequirement(name = "Bearer Authentication")
public class UserController {

    // For demo purposes the users are stored in-memory store by using HashMap.
    // Note: a real application would persist them in a database.
    private final Map<Long, UserResponse> users = new ConcurrentHashMap<>();

    // AtomicLong provides a simple thread-safe id generator.
    // Note: normally the database would manage identifiers.
    private final AtomicLong idSeq = new AtomicLong(0);

    /**
     * Constructor seeds the in-memory store with a few demo users.
     */
    public UserController()
    {
        // Populate the map with demo data.
        long id1 = idSeq.incrementAndGet();
        users.put(id1, new UserResponse(id1, "Alice", "alice@example.com"));

        long id2 = idSeq.incrementAndGet();
        users.put(id2, new UserResponse(id2, "Bob", "bob@example.com"));
    }

    // GET /api/v1/users
    @Operation(summary = "Get all users", description = "Returns a list of all users (requires JWT token)")
    @GetMapping
    public List<UserResponse> listUsers()
    {
        // Return all users sorted by the id property.
        // Note: in real life this would be done via a database query.
        return users.values().stream()
                .sorted(Comparator.comparingLong(UserResponse::id))
                .toList();
    }

    // GET /api/v1/users/{id}
    @Operation(summary = "Get user by ID", description = "Returns a single user by ID (requires JWT token)")
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable("id") long id)
    {
        // Fetch the user by id from the in-memory map.
        UserResponse user = users.get(id);

        // Return 404 if the user does not exist.
        if (user == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        // Return the user with HTTP 200 OK.
        return ResponseEntity.ok(user);
    }

    // POST /api/v1/users
    @Operation(summary = "Create new user", description = "Creates a new user (requires JWT token)")
    @PostMapping
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody UserCreateRequest req)
    {
        // Generate a new id and construct the user.
        long id = idSeq.incrementAndGet();
        UserResponse created = new UserResponse(id, req.name(), req.email());
        // Store the user in the map.
        users.put(id, created);

        // Respond with 201 Created and a Location header.
        URI location = URI.create("/api/v1/users/" + id);
        return ResponseEntity.created(location).body(created);
    }

    // PUT /api/v1/users/{id}
    @Operation(summary = "Update user", description = "Updates an existing user by ID (requires JWT token)")
    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(@PathVariable("id") long id, @Valid @RequestBody UserCreateRequest req)
    {
        // Load the existing user.
        UserResponse existing = users.get(id);

        // Return 404 if the user does not exist.
        if (existing == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        // Update the user data and replace it in the map.
        UserResponse updated = new UserResponse(id, req.name(), req.email());
        users.put(id, updated);

        return ResponseEntity.ok(updated);
    }

    // DELETE /api/v1/users/{id}
    @Operation(summary = "Delete user", description = "Deletes a user by ID (requires JWT token)")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable("id") long id)
    {
        // Remove the user from the map; remove returns the old value or null if missing.
        UserResponse removed = users.remove(id);

        // Return 404 if the user did not exist.
        if (removed == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        // When deletion succeeds, respond with 204 No Content.
        return ResponseEntity.noContent().build();
    }

}
