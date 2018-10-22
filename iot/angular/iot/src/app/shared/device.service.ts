import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { of } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Device } from './documentation-items';

@Injectable({
  providedIn: 'root'
})
export class DeviceService {
  API_URL = 'api/devices';

  constructor(private http: HttpClient) { }

  deviceInfo(name) {
    const params = new HttpParams()
      .set('name', name);

    return this.http.get<Device>(this.API_URL, { params });
  }

  devicesInfo() {
    return this.http.get<Device[]>(this.API_URL).pipe(
      map(res => {
        return res;
      })
    );
  }
}
