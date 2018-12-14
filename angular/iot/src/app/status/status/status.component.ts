import { Component, OnInit, OnDestroy } from '@angular/core';

import { WebsocketService } from '../../_service/websocket.service';
import { DeviceService } from '../../_service/device.service';

import { DeviceData, Device } from '../../shared/documentation-items';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit, OnDestroy {
  connection;
  devices: Device[];
  devicesData = {};

  constructor(private websocketService: WebsocketService, private deviceService: DeviceService) { }

  ngOnInit() {
    this.deviceService.devicesInfo().subscribe((res: Device[]) => {
      this.devices = res;
      this.devices.forEach(device => {
        this.devicesData[device.id] = {
          time: null,
          data: null
        };
      });
      // console.log(this.status);
      this.connection = this.websocketService.onNewMessage().subscribe((msg: DeviceData) => {
        // console.log(msg);
        if (this.devicesData[msg.id]) {
          if (msg.time == null) {
            this.devicesData[msg.id].time = Date();
            this.devicesData[msg.id].data = null;
          } else {
            this.devicesData[msg.id].time = msg.time;
            this.devicesData[msg.id].data = msg.data;
          }
        }
      });
      this.websocketService.send('request', 'hello, server!');
    });
  }

  ngOnDestroy() {
    if (this.connection) {
      this.connection.unsubscribe();
    }
  }

}
