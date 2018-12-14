import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { of } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Device } from '../shared/documentation-items';

@Injectable({
  providedIn: 'root'
})
export class DeviceService {
  API_URL = 'api/devices';

  constructor(private http: HttpClient) { }

  deviceInfo(id) {
    let key = 'device';
    key = key + id;
    const value: Device = JSON.parse(sessionStorage.getItem(key));

    if (value) {
      return of(value);
    }

    const params = new HttpParams()
      .set('id', id);

    return this.http.get<Device>(this.API_URL, { params }).pipe(
      map(res => {
        sessionStorage.setItem(key, JSON.stringify(res));
        return res;
      })
    );
  }

  devicesInfo() {
    const value: Device[] = JSON.parse(sessionStorage.getItem('devicesInfo'));

    if (value) {
      return of(value);
    }

    return this.http.get<Device[]>(this.API_URL).pipe(
      map(res => {
        sessionStorage.setItem('devicesInfo', JSON.stringify(res));
        return res;
      })
    );
  }
}
