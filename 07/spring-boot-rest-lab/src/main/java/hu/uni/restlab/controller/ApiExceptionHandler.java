package hu.uni.restlab.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.FieldError;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Global exception handler for REST API.
 *
 * This class handles exceptions thrown by controller methods
 * and translates them into appropriate HTTP responses.
 */
@RestControllerAdvice
public class ApiExceptionHandler {

    // Handle validation errors
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex)
    {
        Map<String, Object> body = new LinkedHashMap<>();

        body.put("error", "Validation failed");

        Map<String, String> fields = new LinkedHashMap<>();
        // We get all field errors and put them into the fields map.
        // These are the fields that failed validation along with their error messages.
        for (FieldError fe : ex.getBindingResult().getFieldErrors()) {
            fields.put(fe.getField(), fe.getDefaultMessage());
        }
        body.put("fields", fields);

        // Add the general exception message
        body.put("message", ex.getMessage());

        return ResponseEntity.status(HttpStatus.BAD_REQUEST).body(body);
    }

    // Handle general Exception
    @ExceptionHandler(Exception.class)
    public ResponseEntity<Map<String, Object>> handleGeneralException(Exception ex)
    {
        Map<String, Object> body = new LinkedHashMap<>();

        body.put("error", "Internal server error");
        body.put("message", ex.getMessage());

        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(body);
    }

}
