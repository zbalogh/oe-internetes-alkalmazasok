import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { NavbarComponent } from './shared/navbar/navbar.component';
import { HomeComponent } from './pages/home/home.component';
import { UserListComponent } from './pages/user-list/user-list.component';
import { UserDetailsComponent } from './pages/user-details/user-details.component';

import { AuthInterceptor } from './core/auth.interceptor';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    UserListComponent,
    UserDetailsComponent
  ],
  imports: [
    BrowserModule,      // Alap modul a böngészőben futó appokhoz
    AppRoutingModule,   // App Routing modul (útvonalak kezelése)
    HttpClientModule,   // HttpClient használatához
    FormsModule         // Form-ok kezelése, [(ngModel)] miatt
  ],
  providers: [
    // Interceptor globális regisztrálása
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true }
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
