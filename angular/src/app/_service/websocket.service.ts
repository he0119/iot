import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { Observable } from 'rxjs';
import { DeviceData } from '../shared/documentation-items';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket: SocketIOClient.Socket;

  constructor() { }
  // Message to server
  send(type: string, msg: any) {
    this.socket.emit('website', {
      type: type,
      data: msg
    });
  }

  // HANDLER
  onNewMessage() {
    const observable = new Observable(observer => {
      this.socket = io();
      this.socket.on('status', (data: DeviceData) => {
        observer.next(data);
      });
      return () => {
        this.socket.disconnect();
      };
    });
    return observable;
  }
}
