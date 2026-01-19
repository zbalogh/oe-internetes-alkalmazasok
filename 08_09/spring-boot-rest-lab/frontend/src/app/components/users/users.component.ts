import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../../models/user.model';
import { UserService } from '../../services/user.service';

/**
 * UsersComponent displays a list of all users and provides functionality
 * to add, edit, and delete users.
 * 
 * This component is the main user management interface where users can:
 * - View all existing users in a table
 * - Navigate to create a new user
 * - Navigate to edit an existing user
 * - Delete users from the system
 */
@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {

  /**
   * Array of users fetched from the backend
   */
  users: User[] = [];

  /**
   * Loading state indicator
   */
  loading = false;

  /**
   * Error message to display if an error occurs
   */
  errorMessage: string | null = null;

  /**
   * Success message to display after successful operations
   */
  successMessage: string | null = null;

  /**
   * Constructor with dependency injection.
   * 
   * @param userService - Service for user CRUD operations
   * @param router - Angular router for navigation
   */
  constructor(
    private userService: UserService,
    private router: Router
  ) { }

  /**
   * Angular lifecycle hook called after component initialization.
   * Loads all users when the component is created.
   */
  ngOnInit(): void {
    this.loadUsers();
  }

  /**
   * Loads all users from the backend via UserService.
   * Sets loading state and handles errors appropriately.
   */
  loadUsers(): void {
    this.loading = true;
    this.errorMessage = null;

    this.userService.getAllUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.loading = false;
        console.error('Error loading users:', error);
      }
    });
  }

  /**
   * Navigates to the edit page to create a new user.
   */
  onAddUser(): void {
    this.router.navigate(['/users/new']);
  }

  /**
   * Navigates to the edit page for a specific user.
   * 
   * @param userId - The ID of the user to edit
   */
  onEditUser(userId: number): void {
    this.router.navigate(['/users/edit', userId]);
  }

  /**
   * Deletes a user after confirmation.
   * Reloads the user list after successful deletion.
   * 
   * @param userId - The ID of the user to delete
   * @param userName - The name of the user (for confirmation message)
   */
  onDeleteUser(userId: number, userName: string): void {
    // Ask for confirmation before deleting
    const confirmDelete = confirm(`Are you sure you want to delete user "${userName}"?`);
    
    if (confirmDelete) {
      this.loading = true;
      this.errorMessage = null;

      this.userService.deleteUser(userId).subscribe({
        next: () => {
          this.successMessage = `User "${userName}" has been successfully deleted.`;
          this.loading = false;
          // Reload the user list to reflect the deletion
          this.loadUsers();
          
          // Clear success message after 3 seconds
          setTimeout(() => {
            this.successMessage = null;
          }, 3000);
        },
        error: (error) => {
          this.errorMessage = error.message;
          this.loading = false;
          console.error('Error deleting user:', error);
        }
      });
    }
  }

  /**
   * Clears the error message.
   */
  clearError(): void {
    this.errorMessage = null;
  }

  /**
   * Clears the success message.
   */
  clearSuccess(): void {
    this.successMessage = null;
  }
}

