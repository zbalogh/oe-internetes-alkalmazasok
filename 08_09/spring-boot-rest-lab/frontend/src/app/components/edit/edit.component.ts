import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { UserService } from '../../services/user.service';
import { User, UserRequest } from '../../models/user.model';

/**
 * EditComponent handles both creating new users and editing existing users.
 * 
 * This component:
 * - Determines if it's in "create" or "edit" mode based on the route
 * - Loads existing user data when editing
 * - Provides a form for user input (name and email)
 * - Validates user input
 * - Saves changes to the backend via UserService
 * - Navigates back to the users list after successful save
 */
@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent implements OnInit {

  /**
   * User object being edited/created
   */
  user: UserRequest = {
    name: '',
    email: ''
  };

  /**
   * ID of the user being edited (null if creating new user)
   */
  userId: number | null = null;

  /**
   * Flag indicating if component is in edit mode (true) or create mode (false)
   */
  isEditMode = false;

  /**
   * Loading state indicator
   */
  loading = false;

  /**
   * Error message to display if an error occurs
   */
  errorMessage: string | null = null;

  /**
   * Form validation errors
   */
  validationErrors: { [key: string]: string } = {};

  /**
   * Constructor with dependency injection.
   * 
   * @param userService - Service for user CRUD operations
   * @param route - ActivatedRoute for accessing route parameters
   * @param router - Router for navigation
   */
  constructor(
    private userService: UserService,
    private route: ActivatedRoute,
    private router: Router
  ) { }

  /**
   * Angular lifecycle hook called after component initialization.
   * Determines if in edit or create mode and loads user data if editing.
   */
  ngOnInit(): void {
    // Get the user ID from the route parameters
    const id = this.route.snapshot.paramMap.get('id');
    
    if (id && id !== 'new') {
      // Edit mode - load existing user
      this.isEditMode = true;
      this.userId = +id; // Convert string to number
      this.loadUser(this.userId);
    } else {
      // Create mode - start with empty user
      this.isEditMode = false;
    }
  }

  /**
   * Loads user data from the backend for editing.
   * 
   * @param id - The ID of the user to load
   */
  loadUser(id: number): void {
    this.loading = true;
    this.errorMessage = null;

    this.userService.getUserById(id).subscribe({
      next: (data) => {
        this.user = {
          name: data.name,
          email: data.email
        };
        this.loading = false;
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.loading = false;
        console.error('Error loading user:', error);
      }
    });
  }

  /**
   * Validates the user form data.
   * 
   * @returns true if valid, false otherwise
   */
  validateForm(): boolean {
    this.validationErrors = {};
    let isValid = true;

    // Validate name
    if (!this.user.name || this.user.name.trim().length === 0) {
      this.validationErrors['name'] = 'Name is required';
      isValid = false;
    } else if (this.user.name.trim().length < 2) {
      this.validationErrors['name'] = 'Name must be at least 2 characters';
      isValid = false;
    }

    // Validate email
    if (!this.user.email || this.user.email.trim().length === 0) {
      this.validationErrors['email'] = 'Email is required';
      isValid = false;
    } else {
      // Basic email validation
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailPattern.test(this.user.email)) {
        this.validationErrors['email'] = 'Please enter a valid email address';
        isValid = false;
      }
    }

    return isValid;
  }

  /**
   * Handles form submission.
   * Validates input and either creates or updates the user.
   */
  onSubmit(): void {
    // Validate form before submission
    if (!this.validateForm()) {
      return;
    }

    this.loading = true;
    this.errorMessage = null;

    if (this.isEditMode && this.userId !== null) {
      // Update existing user
      this.userService.updateUser(this.userId, this.user).subscribe({
        next: () => {
          this.loading = false;
          // Navigate back to users list
          this.router.navigate(['/users']);
        },
        error: (error) => {
          this.errorMessage = error.message;
          this.loading = false;
          console.error('Error updating user:', error);
        }
      });
    } else {
      // Create new user
      this.userService.createUser(this.user).subscribe({
        next: () => {
          this.loading = false;
          // Navigate back to users list
          this.router.navigate(['/users']);
        },
        error: (error) => {
          this.errorMessage = error.message;
          this.loading = false;
          console.error('Error creating user:', error);
        }
      });
    }
  }

  /**
   * Handles cancel button click.
   * Navigates back to the users list without saving.
   */
  onCancel(): void {
    this.router.navigate(['/users']);
  }

  /**
   * Clears the error message.
   */
  clearError(): void {
    this.errorMessage = null;
  }
}

