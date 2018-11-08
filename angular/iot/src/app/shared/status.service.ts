import { Injectable } from '@angular/core';
import { map } from 'rxjs/operators';
import { of } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class StatusService {
  API_URL = 'api/status';
  // API_URL = 'http://127.0.0.1:5000/api/status';

  constructor(private http: HttpClient) { }

  setDeviceStatus(id, key, value) {
    return this.http.put(this.API_URL, { 'id': id, 'data': { [key]: value } });
  }
}
