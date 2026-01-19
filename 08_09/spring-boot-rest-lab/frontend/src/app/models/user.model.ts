/**
 * User model interface.
 * 
 * This interface matches the UserResponse from the backend REST API.
 * It represents the structure of user data received from the server.
 */
export interface User {
  /**
   * Unique identifier for the user
   */
  id: number;

  /**
   * User's full name
   */
  name: string;

  /**
   * User's email address
   */
  email: string;
}

/**
 * User creation/update request interface.
 * 
 * This interface is used when creating or updating a user.
 * It contains only the fields that can be modified by the user.
 */
export interface UserRequest {
  /**
   * User's full name
   */
  name: string;

  /**
   * User's email address
   */
  email: string;
}
