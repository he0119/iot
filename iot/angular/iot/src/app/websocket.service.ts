import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket: SocketIOClient.Socket;

  constructor() {
    this.socket = io();
  }
  // Message to server
  send(type: string, msg: any) {
    this.socket.emit('website', {
      type: type,
      data: msg
    });
  }

  // HANDLER
  onNewMessage() {
    return Observable.create(observer => {
      this.socket.on('status', msg => {
        observer.next(msg);
      });
    });
  }
}
