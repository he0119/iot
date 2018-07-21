import { Component, OnInit, OnDestroy } from '@angular/core';

import { WebsocketService } from '../../shared/websocket.service';
import { DeviceData, Device } from '../../shared/documentation-items';
import { DeviceService } from '../../shared/device.service';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit, OnDestroy {
  connection;
  devices: Device[];
  status: DeviceData[] = [];

  constructor(private websocketService: WebsocketService, private deviceService: DeviceService) { }

  ngOnInit() {
    this.deviceService.devicesInfo().subscribe((res: Device[]) => {
      console.log(res);
      this.devices = res;
      for (const device of this.devices) {
        this.status.push({
          name: device.name,
          time: null,
          data: null
        });
      }
      // console.log(this.status);
      this.connection = this.websocketService.onNewMessage().subscribe((msg: DeviceData) => {
        console.log(msg);
        for (const device of this.status) {
          if (device.name === msg.name) {
            if (msg.time == null) {
              device.time = Date();
              device.data = { data: 'not exist' };
            } else {
              device.time = msg.time;
              device.data = msg.data;
            }
          }
        }
      });
      this.websocketService.send('request', 'hello, server!');
    });
  }

  ngOnDestroy() {
    this.connection.unsubscribe();
  }

  changeStatus() { }
}
