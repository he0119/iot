import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { Observable } from 'rxjs';
import { DeviceData } from './documentation-items';

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
      // this.socket = io("http://127.0.0.1:5000/");
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
