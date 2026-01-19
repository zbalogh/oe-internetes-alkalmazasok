import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './components/home/home.component';
import { UsersComponent } from './components/users/users.component';
import { EditComponent } from './components/edit/edit.component';

/**
 * Root module of the application.
 * 
 * This module:
 * - Declares all components
 * - Imports necessary Angular modules (BrowserModule, HttpClientModule, FormsModule)
 * - Configures routing
 * - Bootstraps the application with AppComponent
 */
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    UsersComponent,
    EditComponent
  ],
  imports: [
    BrowserModule,     // Required for running the app in a browser
    AppRoutingModule,  // Application routing configuration
    HttpClientModule,  // Required for HTTP communication with backend
    FormsModule        // Required for template-driven forms (ngModel)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }

