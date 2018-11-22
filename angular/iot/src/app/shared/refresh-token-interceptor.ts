import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, mergeMap } from 'rxjs/operators';
import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { AuthorizationService } from './authorization.service';
import { TokenInterceptor } from './token.interceptor';

@Injectable()
export class RefreshTokenInterceptor implements HttpInterceptor {
  constructor(private authorizationService: AuthorizationService, private tokenInterceptor: TokenInterceptor) {
  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    return next.handle(req).pipe(
      catchError((err) => {
        const errorResponse = err as HttpErrorResponse;
        if (errorResponse.status === 401 && errorResponse.error.msg === 'Token has expired') {
          return this.authorizationService.refresh().pipe(mergeMap(() => {
            return this.tokenInterceptor.intercept(req, next);
          }));
        }
        return throwError(err);
      }));
  }
}
