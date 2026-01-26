package hu.uni.restlab.dto;

/**
 * Data record representing a user response.
 *
 * This record is used to transfer user data in API responses.
 */
public record UserResponse(
        long id,
        String name,
        String email
) { }
