package hu.uni.restlab.dto;

import jakarta.validation.constraints.NotBlank;

/**
 * Data record representing an authentication request.
 *
 * This record is used to transfer login credentials in authentication requests.
 */
public record AuthRequest(
        @NotBlank(message = "Username is required")
        String username,

        @NotBlank(message = "Password is required")
        String password
) { }
