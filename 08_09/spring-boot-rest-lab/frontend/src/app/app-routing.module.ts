import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { UsersComponent } from './components/users/users.component';
import { EditComponent } from './components/edit/edit.component';

/**
 * Application routing configuration.
 * 
 * This module defines all the routes in the application:
 * - Home page: welcome screen
 * - Users page: list all users with CRUD operations
 * - Edit page: create/edit user form
 */
const routes: Routes = [
  // Default route - redirect to home
  { 
    path: '', 
    redirectTo: '/home', 
    pathMatch: 'full' 
  },
  
  // Home page route
  { 
    path: 'home', 
    component: HomeComponent 
  },
  
  // Users list page route
  { 
    path: 'users', 
    component: UsersComponent 
  },
  
  // Create new user route
  { 
    path: 'users/new', 
    component: EditComponent 
  },
  
  // Edit existing user route with ID parameter
  { 
    path: 'users/edit/:id', 
    component: EditComponent 
  },
  
  // Wildcard route - redirect to home if no match found
  { 
    path: '**', 
    redirectTo: '/home' 
  }
];

/**
 * Angular routing module configuration.
 * 
 * useHash: true - Enables hash-based routing (#/home, #/users)
 * This is required when the application is served by Spring Boot in production.
 * With hash-based routing, the browser never sends the route part (after #)
 * to the server, so F5 refresh and direct URL access always work.
 */
@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }

