package hu.uni.restlab.controller;

import hu.uni.restlab.dto.AuthRequest;
import hu.uni.restlab.dto.AuthResponse;
import hu.uni.restlab.jwt.JwtUtil;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * REST controller for authentication.
 *
 * This controller provides an endpoint for user authentication
 * and JWT token generation.
 */
@RestController
@RequestMapping("/api/v1/auth")
@Tag(name = "Authentication", description = "Endpoints for user authentication and JWT token generation")
public class AuthController {

    private final AuthenticationManager authenticationManager;
    private final JwtUtil jwtUtil;

    /**
     * Constructor for AuthController.
     *
     * @param authenticationManager     The authentication manager provided by Spring Security
     * @param jwtUtil                   The JWT utility class used for token generation and validation
     */
    public AuthController(AuthenticationManager authenticationManager, JwtUtil jwtUtil) {
        this.authenticationManager = authenticationManager;
        this.jwtUtil = jwtUtil;
    }

    /**
     * Authenticate user and generate JWT token.
     *
     * POST /api/v1/auth/login
     *
     * Request body:
     * {
     *   "username": "demo",
     *   "password": "12345"
     * }
     *
     * Response:
     * {
     *   "token": "eyJhbGc...",
     *   "type": "Bearer",
     *   "expiresIn": 86400000
     * }
     */
    @Operation(
            summary = "Login to get JWT token",
            description = "Authenticate with username and password to receive a JWT token. " +
                    "Use credentials: username='demo', password='12345'"
    )
    @ApiResponses(value = {
            @ApiResponse(
                    responseCode = "200",
                    description = "Successfully authenticated - returns JWT token",
                    content = @Content(schema = @Schema(implementation = AuthResponse.class))
            ),
            @ApiResponse(
                    responseCode = "401",
                    description = "Authentication failed - invalid username or password"
            ),
            @ApiResponse(
                    responseCode = "400",
                    description = "Bad request - validation error"
            )
    })
    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody AuthRequest authRequest)
    {
        try {
            // Authenticate the user
            Authentication authentication = authenticationManager.authenticate(
                    new UsernamePasswordAuthenticationToken(
                            authRequest.username(),
                            authRequest.password()
                    )
            );

            // Generate JWT token
            String token = jwtUtil.generateToken(authentication.getName());

            // Return token in response
            AuthResponse response = new AuthResponse(token, jwtUtil.getExpiration());
            return ResponseEntity.ok(response);

        }
        catch (BadCredentialsException e)
        {
            // Return 401 Unauthorized if credentials are invalid
            Map<String, Object> errorResponse = new LinkedHashMap<>();
            errorResponse.put("error", "Authentication failed");
            errorResponse.put("message", "Invalid username or password");

            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body(errorResponse);
        }
    }

}
