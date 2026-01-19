import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';
import { User } from '../models/user';

/**
 * Service felelőssége:
 * - HTTP hívások (adatlekérés)
 * - hibák egységes kezelése/átalakítása
 * A komponens csak "fogyasztja" az adatot és reagál (loading/error megjelenítés).
 */
@Injectable({
  providedIn: 'root'
})
export class UserService {
  
  private readonly baseUrl = 'https://jsonplaceholder.typicode.com/users';

  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]>
  {
    return this.http.get<User[]>(this.baseUrl).pipe(
      catchError(err => this.handleHttpError(err))
    );
  }

  getUser(id: number): Observable<User>
  {
    return this.http.get<User>(`${this.baseUrl}/${id}`).pipe(
      catchError(err => this.handleHttpError(err))
    );
  }

  /**
   * Egyszerű, oktatási célú hibakezelés:
   * - külön kezeljük a hálózati hibát és a backend hibát
   * - egységes, emberi üzenetet adunk vissza
   */
  private handleHttpError(error: HttpErrorResponse)
  {
    // Ha status = 0, az jellemzően hálózati / CORS / DNS / offline hiba
    if (error.status === 0) {
      return throwError(() => new Error('Hálózati hiba: nem érhető el a szerver (internet / CORS / DNS probléma).'));
    }

    // Backend hibák (HTTP státuszkód alapján)
    if (error.status === 404) {
      return throwError(() => new Error('404 – A kért erőforrás nem található.'));
    }

    return throwError(() => new Error(`Szerver hiba (${error.status}): próbáld meg később.`));
  }
  
}
