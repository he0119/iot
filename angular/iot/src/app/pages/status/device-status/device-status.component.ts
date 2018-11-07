import { Component, OnInit, Input } from '@angular/core';

import { StatusService } from '../../../shared/status.service';

import { DeviceData, Device, DeviceDataType } from '../../../shared/documentation-items';
import { element } from '@angular/core/src/render3';

@Component({
  selector: 'app-device-status',
  templateUrl: './device-status.component.html',
  styleUrls: ['./device-status.component.scss']
})
export class DeviceStatusComponent implements OnInit {
  @Input() device: Device;
  @Input() deviceData: DeviceData;
  deviceDataType = DeviceDataType;

  constructor(private statusService: StatusService) { }

  ngOnInit() {
  }

  changeStatus(id, key, value) {
    this.statusService.setDeviceStatus(id, key, value).subscribe(result =>
      console.log(result)
    );
  }

  showAll(){
      Object.keys(this.device.display).forEach(element => {
        this.device.display[element][0] = 1;
      })
  }
}
