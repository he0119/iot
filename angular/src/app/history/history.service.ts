import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { DeviceData } from '../shared/documentation-items';

@Injectable()
export class HistoryService {
  API_URL = 'api/history';

  constructor(private http: HttpClient) { }

  historyData(id, start, end, interval) {
    const params = new HttpParams()
      .set('id', id)
      .set('start', start)
      .set('end', end)
      .set('interval', interval);

    return this.http.get<DeviceData[]>(this.API_URL, { params });
  }
}
