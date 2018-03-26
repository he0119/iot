import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import 'rxjs/add/operator/map';

@Injectable()
export class HistoryService {

  constructor(private _http: HttpClient) { }

  historyData(start, end, interval) {
    const params = new HttpParams()
    .set('start', start)
    .set('end', end)
    .set('interval', interval);

    return this._http.get('api/history', {params})
      .map(result => result);
  }
}
