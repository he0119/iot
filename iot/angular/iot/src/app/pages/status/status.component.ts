import { Component, OnInit, OnDestroy } from '@angular/core';

import { WebsocketService } from '../../shared/websocket.service';
import { DeviceService } from '../../shared/device.service';
import { StatusService } from '../../shared/status.service';
import { DeviceData, Device } from '../../shared/documentation-items';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit, OnDestroy {
  connection;
  devices: Device[];
  status = {};

  constructor(private websocketService: WebsocketService, private deviceService: DeviceService, private statusService: StatusService) { }

  ngOnInit() {
    this.deviceService.devicesInfo().subscribe((res: Device[]) => {
      this.devices = res;
      this.devices.forEach(device => {
        this.status[device.name] = {
          time: null,
          data: null
        }
      })
      // console.log(this.status);
      this.connection = this.websocketService.onNewMessage().subscribe((msg: DeviceData) => {
        console.log(msg);
        if (this.status[msg.name]) {
          if (msg.time == null) {
            this.status[msg.name].time = Date();
            this.status[msg.name].data = null;
          } else {
            this.status[msg.name].time = msg.time;
            this.status[msg.name].data = msg.data;
          }
        }
      });
      this.websocketService.send('request', 'hello, server!');
    });
  }

  ngOnDestroy() {
    this.connection.unsubscribe();
  }

  changeStatus(name, key) {
    this.statusService.setDeviceStatus(name, key, !this.status[name]['data'][key]).subscribe(result =>
      console.log(result)
    );
  }
}
