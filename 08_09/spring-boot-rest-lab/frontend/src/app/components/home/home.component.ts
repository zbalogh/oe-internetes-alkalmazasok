import { Component, OnInit } from '@angular/core';

/**
 * HomeComponent serves as the landing page of the application.
 * 
 * This component displays a welcome message and provides an overview
 * of the user management system.
 */
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  /**
   * Constructor - currently no dependencies needed
   */
  constructor() { }

  /**
   * Angular lifecycle hook called after component initialization.
   * Currently no initialization logic needed.
   */
  ngOnInit(): void {
    // Component initialization logic can be added here if needed
  }

}
