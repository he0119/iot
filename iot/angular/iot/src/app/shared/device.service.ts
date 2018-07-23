import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { of } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { LocalStorageService } from 'angular-web-storage';
import { Device } from './documentation-items';

@Injectable({
  providedIn: 'root'
})
export class DeviceService {
  API_URL = 'api/devices';

  constructor(private http: HttpClient, private local: LocalStorageService) { }

  deviceInfo(name) {
    const params = new HttpParams()
      .set('name', name);

    return this.http.get<Device>(this.API_URL, { params });
  }

  devicesInfo() {
    const value = this.local.get('devicesInfo');
    if (value) {
      return of(value);
    }
    return this.http.get<Device[]>(this.API_URL).pipe(
      map(res => {
        this.local.set('devicesInfo', res, 1, 'w');
        return res;
      })
    );
  }
}
