import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { WebsocketService } from '../../shared/websocket.service';
import { DeviceData } from '../../shared/documentation-items';


@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit, OnDestroy {
  connection;

  status: DeviceData[] = [];

  constructor(private websocketService: WebsocketService) { }

  ngOnInit() {
    this.connection = this.websocketService.onNewMessage().subscribe((msg: DeviceData) => {
      console.log(msg);
      let needAdd = true;
      for (const device of this.status) {
        if (device.name === msg.name) {
          needAdd = false;
          device.data = msg.data;
          device.time = msg.time;
        }
      }
      if (needAdd) {
        if (msg.time == null) {
          msg.time = Date();
          msg.data = { data: 'not exist' };
        }
      this.status.push(msg);
    }
  });
    this.websocketService.send('request', 'hello, server!');
  }

ngOnDestroy() {
  this.connection.unsubscribe();
}

changeStatus() { }
}
