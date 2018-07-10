import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class WebsocketService {
  private socket: SocketIOClient.Socket;

  constructor() {
    this.socket = io('http://192.168.31.12:5000');
  }
  // EMITTER
  sendMessage(msg: string) {
    this.socket.emit('control', { message: msg });
  }

  // HANDLER
  onNewMessage() {
    return Observable.create(observer => {
      this.socket.on('data', msg => {
        observer.next(msg);
      });
    });
  }

}
