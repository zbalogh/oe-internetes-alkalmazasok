import { Component, OnInit } from '@angular/core';
import { UserService } from '../../core/user.service';
import { User } from '../../models/user';

/**
 * Oktatási cél:
 * - Komponens: UI state (loading, error, data)
 * - Service: adatlekérés, hibakezelés
 */
@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements OnInit {
  
  users: User[] = [];

  // UI state
  isLoading = false;
  errorMessage: string | null = null;

  // Keresés (two-way binding)
  searchTerm = '';

  constructor(private userService: UserService) {}

  ngOnInit(): void
  {
    this.loadUsers();
  }

  loadUsers(): void
  {
    this.isLoading = true;
    this.errorMessage = null;

    this.userService.getUsers().subscribe({
      next: (data) => {
        this.users = data;
      },
      error: (err: Error) => {
        this.errorMessage = err.message;
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }

  // Egyszerű kliens oldali szűrés: név / email alapján
  get filteredUsers(): User[]
  {
    const term = this.searchTerm.trim().toLowerCase();
    if (!term) return this.users;

    return this.users.filter(u =>
      u.name.toLowerCase().includes(term) ||
      u.email.toLowerCase().includes(term)
    );
  }

}
