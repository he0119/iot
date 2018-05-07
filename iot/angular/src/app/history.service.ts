import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class HistoryService {
  API_URL = 'api/history';

  constructor(private http: HttpClient) { }

  historyData(start, end, interval) {
    const params = new HttpParams()
    .set('start', start)
    .set('end', end)
    .set('interval', interval);

    return this.http.get(this.API_URL, {params});
  }
}
