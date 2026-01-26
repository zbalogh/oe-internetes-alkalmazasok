package hu.uni.restlab.dto;

/**
 * Data record representing an authentication response.
 *
 * This record is used to transfer JWT token in authentication responses.
 */
public record AuthResponse(
        String token,
        String type,
        long expiresIn
) {
    /**
     * Constructor with default token type "Bearer".
     */
    public AuthResponse(String token, long expiresIn) {
        this(token, "Bearer", expiresIn);
    }

}
