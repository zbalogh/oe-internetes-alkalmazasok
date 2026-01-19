import { Component } from '@angular/core';

/**
 * Root component of the application.
 * 
 * This component serves as the main container for the entire application.
 * It includes the navigation menu and router outlet for displaying
 * different components based on the current route.
 */
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  /**
   * Application title displayed in the header
   */
  title = 'User Management System';
}

