import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { User, UserRequest } from '../models/user.model';

/**
 * Service for managing user data via REST API.
 * 
 * This service provides methods for CRUD operations on users.
 * It uses HttpClient to communicate with the backend REST API.
 * All HTTP errors are handled and converted to user-friendly messages.
 */
@Injectable({
  providedIn: 'root'
})
export class UserService {

  /**
   * Base URL for the user API endpoints.
   * In development mode, this will be proxied to the backend server.
   */
  private readonly apiUrl = '/api/v1/users';

  /**
   * Constructor with dependency injection of HttpClient.
   * 
   * @param http - Angular's HttpClient for making HTTP requests
   */
  constructor(private http: HttpClient) { }

  /**
   * Fetches all users from the backend.
   * 
   * @returns Observable of an array of User objects
   */
  getAllUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.apiUrl)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Fetches a single user by ID.
   * 
   * @param id - The unique identifier of the user
   * @returns Observable of a User object
   */
  getUserById(id: number): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/${id}`)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Creates a new user.
   * 
   * @param user - The user data to create (name and email)
   * @returns Observable of the created User object with assigned ID
   */
  createUser(user: UserRequest): Observable<User> {
    return this.http.post<User>(this.apiUrl, user)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Updates an existing user.
   * 
   * @param id - The unique identifier of the user to update
   * @param user - The updated user data (name and email)
   * @returns Observable of the updated User object
   */
  updateUser(id: number, user: UserRequest): Observable<User> {
    return this.http.put<User>(`${this.apiUrl}/${id}`, user)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Deletes a user by ID.
   * 
   * @param id - The unique identifier of the user to delete
   * @returns Observable of void (no content)
   */
  deleteUser(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Handles HTTP errors and converts them to user-friendly messages.
   * 
   * This method is called when any HTTP request fails.
   * It logs the error to the console and returns an Observable error
   * with a meaningful message for the user.
   * 
   * @param error - The HTTP error response
   * @returns Observable that throws an error with a user-friendly message
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'An unknown error occurred';

    if (error.error instanceof ErrorEvent) {
      // Client-side or network error
      errorMessage = `Client Error: ${error.error.message}`;
    } else {
      // Backend returned an unsuccessful response code
      switch (error.status) {
        case 400:
          errorMessage = 'Bad Request: Invalid data provided';
          break;
        case 404:
          errorMessage = 'Not Found: User does not exist';
          break;
        case 500:
          errorMessage = 'Server Error: Please try again later';
          break;
        default:
          errorMessage = `Server Error: ${error.status} - ${error.message}`;
      }
    }

    // Log the error to console for debugging
    console.error('HTTP Error:', error);
    console.error('Error Message:', errorMessage);

    // Return an observable with a user-facing error message
    return throwError(() => new Error(errorMessage));
  }
}
