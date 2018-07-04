import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Status } from './status';

@Injectable({
  providedIn: 'root'
})
export class StatusService {
  API_URL = 'api/status';

  constructor(private http: HttpClient) { }

  setRelayState(id: number, input: boolean) {
    return this.http.put(this.API_URL, {'id' : id, 'status' : input ? '1' : '0'});
  }

  currentData(): Observable<Status> {
    return this.http.get<Status>(this.API_URL)
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
