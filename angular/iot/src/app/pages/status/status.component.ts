import { Component, OnInit, OnDestroy } from '@angular/core';

import { WebsocketService } from '../../shared/websocket.service';
import { DeviceService } from '../../shared/device.service';
import { StatusService } from '../../shared/status.service';
import { DeviceData, Device, DeviceDataType } from '../../shared/documentation-items';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit, OnDestroy {
  connection;
  devices: Device[];
  status = {};
  deviceDataType = DeviceDataType;

  constructor(private websocketService: WebsocketService, private deviceService: DeviceService, private statusService: StatusService) { }

  ngOnInit() {
    this.deviceService.devicesInfo().subscribe((res: Device[]) => {
      this.devices = res;
      this.devices.forEach(device => {
        this.status[device.id] = {
          time: null,
          data: null
        }
      })
      // console.log(this.status);
      this.connection = this.websocketService.onNewMessage().subscribe((msg: DeviceData) => {
        console.log(msg);
        if (this.status[msg.id]) {
          if (msg.time == null) {
            this.status[msg.id].time = Date();
            this.status[msg.id].data = null;
          } else {
            this.status[msg.id].time = msg.time;
            this.status[msg.id].data = msg.data;
          }
        }
      });
      this.websocketService.send('request', 'hello, server!');
    });
  }

  ngOnDestroy() {
    this.connection.unsubscribe();
  }

  changeStatus(id, key) {
    this.statusService.setDeviceStatus(id, key, !this.status[id]['data'][key]).subscribe(result =>
      console.log(result)
    );
  }
}
