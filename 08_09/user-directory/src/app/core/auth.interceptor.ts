import { Injectable } from '@angular/core';
import {
  HttpEvent, HttpHandler, HttpInterceptor, HttpRequest, HttpErrorResponse
} from '@angular/common/http';
import { Observable, catchError, tap, throwError } from 'rxjs';

/**
 * Interceptor felelőssége:
 * - "cross-cutting concern": minden HTTP kérésre érvényes szabály
 * - itt demonstráljuk: header hozzáadás + logolás + globális error log
 */
@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>>
  {
    // 1) Header hozzáadás (oktatási "fake token")
    const withHeader = req.clone({
      setHeaders: {
        'X-Demo-Token': '12345'
      }
    });

    // 2) Logolás + globális hiba log
    return next.handle(withHeader).pipe(
      tap({
        next: () => console.log(`[HTTP] ${req.method} ${req.url}`),
      }),
      catchError((err: HttpErrorResponse) => {
        console.error('[HTTP ERROR]', req.url, err.status, err.message);
        return throwError(() => err);
      })
    );
  }

}
