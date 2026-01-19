package hu.uni.restlab.model;

/**
 * Entity class representing a User in the domain model.
 *
 * This class represents the core user entity in the application.
 * For this demo, it's stored in-memory, but it's designed to be
 * easily adaptable to a database using JPA/Hibernate in the future.
 */
public class User {

    private Long id;
    private String name;
    private String email;

    /**
     * Default constructor for frameworks.
     */
    public User() {
    }

    /**
     * Constructor for creating a user with name and email.
     *
     * @param name the user's name
     * @param email the user's email address
     */
    public User(String name, String email)
    {
        this.name = name;
        this.email = email;
    }

    /**
     * Full constructor including id.
     *
     * @param id the user's unique identifier
     * @param name the user's name
     * @param email the user's email address
     */
    public User(Long id, String name, String email)
    {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // Getters and setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

}
