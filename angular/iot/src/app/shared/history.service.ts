import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { DeviceData } from './documentation-items';

@Injectable({
  providedIn: 'root'
})
export class HistoryService {
  API_URL = 'api/history';
  // API_URL = 'http://127.0.0.1:5000/api/history';

  constructor(private http: HttpClient) { }

  historyData(name, start, end, interval) {
    const params = new HttpParams()
      .set('name', name)
      .set('start', start)
      .set('end', end)
      .set('interval', interval);

    return this.http.get<DeviceData[]>(this.API_URL, { params });
  }
}
