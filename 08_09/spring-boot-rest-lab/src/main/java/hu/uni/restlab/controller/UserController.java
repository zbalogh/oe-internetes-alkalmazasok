package hu.uni.restlab.controller;

import hu.uni.restlab.model.User;
import hu.uni.restlab.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

/**
 * REST controller for managing users.
 *
 * This controller provides CRUD operations for user resources.
 * It delegates business logic to the UserService.
 */
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService userService;

    /**
     * Constructor injection of UserService.
     *
     * @param userService the user service handling business logic
     */
    public UserController(UserService userService) {
        this.userService = userService;
    }

    // GET /api/v1/users
    @GetMapping
    public List<UserResponse> listUsers()
    {
        // Delegate to service and convert entities to response DTOs.
        return userService.findAllUsers().stream()
                .map(user -> userService.toResponse(user))
                .toList();
    }

    // GET /api/v1/users/{id}
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUser(@PathVariable("id") long id)
    {
        // Delegate to service to fetch the user by id.
        // If user is found, convert to response DTO and return 200 OK.
        // if the user does not exist, return 404 Not Found.
        return userService.findUserById(id)
                .map(user -> userService.toResponse(user))
                .map(response -> ResponseEntity.ok(response))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND).build());
    }

    // POST /api/v1/users
    @PostMapping
    public ResponseEntity<UserResponse> createUser(@Valid @RequestBody UserCreateRequest req)
    {
        // Delegate to service to create the user.
        User created = userService.createUser(req.name(), req.email());
        UserResponse response = userService.toResponse(created);

        // Respond with 201 Created and a Location header.
        URI location = URI.create("/api/v1/users/" + created.getId());
        return ResponseEntity.created(location).body(response);
    }

    // PUT /api/v1/users/{id}
    @PutMapping("/{id}")
    public ResponseEntity<UserResponse> updateUser(@PathVariable("id") long id, @Valid @RequestBody UserCreateRequest req)
    {
        // Delegate to service to update the user.
        // If user is found and updated, convert to response DTO and return 200 OK.
        // If the user does not exist, return 404 Not Found.
        return userService.updateUser(id, req.name(), req.email())
                .map(user -> userService.toResponse(user))
                .map(response -> ResponseEntity.ok(response))
                .orElse(ResponseEntity.status(HttpStatus.NOT_FOUND).build());
    }

    // DELETE /api/v1/users/{id}
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable("id") long id)
    {
        // Delegate to service to delete the user.
        boolean deleted = userService.deleteUser(id);

        // Return 404 if the user did not exist, otherwise 204 No Content.
        if (!deleted) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        // When deletion succeeds, respond with 204 No Content.
        return ResponseEntity.noContent().build();
    }

}
