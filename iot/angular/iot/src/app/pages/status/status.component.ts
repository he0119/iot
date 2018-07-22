import { Component, OnInit, OnDestroy } from '@angular/core';

import { WebsocketService } from '../../shared/websocket.service';
import { DeviceService } from '../../shared/device.service';
import { DeviceData, Device } from '../../shared/documentation-items';

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
      this.devices = res;
      this.devices.forEach(device => {
        this.status.push({
          name: device.name,
          time: null,
          data: null
        });
      })
      // console.log(this.status);
      this.connection = this.websocketService.onNewMessage().subscribe((msg: DeviceData) => {
        console.log(msg);
        this.status.forEach(device => {
          if (device.name === msg.name) {
            if (msg.time == null) {
              device.time = Date();
              device.data = { data: 'not exist' };
            } else {
              device.time = msg.time;
              device.data = msg.data;
            }
          }
        })
      });
      this.websocketService.send('request', 'hello, server!');
    });
  }

  ngOnDestroy() {
    this.connection.unsubscribe();
  }

  changeStatus() { }
}
