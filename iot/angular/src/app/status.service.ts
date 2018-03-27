import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { catchError, map, tap } from 'rxjs/operators';

import { Status } from './status';

@Injectable()
export class StatusService {

  constructor(private http: HttpClient) { }

  currentData(): Observable<Status> {
    return this.http.get<Status>('api/status')
    .pipe(
      catchError(this.handleError<Status>('getStatus'))
    );
  }

  private handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
}
