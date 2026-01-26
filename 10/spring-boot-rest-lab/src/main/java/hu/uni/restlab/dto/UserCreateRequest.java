package hu.uni.restlab.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;

/**
 * Data record representing a user creation request.
 *
 * This record is used to transfer user data in API requests when creating a new user.
 */
public record UserCreateRequest(
        @NotBlank(message = "Name is required")
        String name,

        @Email(message = "Invalid email format")
        String email
) { }
