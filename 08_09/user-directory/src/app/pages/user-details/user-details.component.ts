import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { UserService } from '../../core/user.service';
import { User } from '../../models/user';

@Component({
  selector: 'app-user-details',
  templateUrl: './user-details.component.html',
  styleUrls: ['./user-details.component.css']
})
export class UserDetailsComponent implements OnInit {

  user: User | null = null;

  isLoading = false;
  errorMessage: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private userService: UserService
  ) {}

  ngOnInit(): void
  {
    // route param olvasás
    const idParam = this.route.snapshot.paramMap.get('id');
    const id = Number(idParam);

    if (!id || Number.isNaN(id)) {
      this.errorMessage = 'Hibás ID a route paraméterben.';
      return;
    }

    this.loadUser(id);
  }

  private loadUser(id: number): void
  {
    this.isLoading = true;
    this.errorMessage = null;

    this.userService.getUser(id).subscribe({
      next: (data) => {
        this.user = data;
      },
      error: (err: Error) => {
        this.errorMessage = err.message;
      },
      complete: () => {
        this.isLoading = false;
      }
    });
  }

}
