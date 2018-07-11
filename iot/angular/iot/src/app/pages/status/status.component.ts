import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { WebsocketService } from '../../websocket.service';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit, OnDestroy {
  status: Array<any> = [];
  connection;

  constructor(private websocketService: WebsocketService) {}

  ngOnInit() {
    this.connection = this.websocketService.onNewMessage().subscribe(msg => {
      console.log(msg);
      let needAdd = true;
      for (const device of this.status) {
        if (device['data'] === null) {
          device['data'] = {data: 'not exist'};
        } else if (device['name'] === msg['name']) {
          needAdd = false;
          device['data'] = msg['data'];
          device['time'] = msg['time'];
        }
      }
      if (needAdd) {
        this.status.push(msg);
      }
    });
    this.websocketService.send('request', 'hello, server!');
  }

  ngOnDestroy() {
    this.connection.unsubscribe();
  }

  changeRelay1() {}
  changeRelay2() {}
}
