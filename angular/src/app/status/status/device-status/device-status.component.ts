import { Component, OnInit, Input } from '@angular/core';

import { StatusService } from '../../../_service/status.service';

import { DeviceData, Device, DeviceDataType } from '../../../shared/documentation-items';

@Component({
  selector: 'app-device-status',
  templateUrl: './device-status.component.html',
  styleUrls: ['./device-status.component.scss']
})
export class DeviceStatusComponent implements OnInit {
  @Input() device: Device;
  @Input() deviceData: DeviceData;
  deviceDataType = DeviceDataType;
  settingVisibility = 0;


  constructor(private statusService: StatusService) { }

  ngOnInit() {
  }

  changeStatus(id, key, value) {
    this.statusService.setDeviceStatus(id, key, value).subscribe();
  }

  showSettings() {
    this.settingVisibility = 1;
  }
  hideSettings() {
    this.settingVisibility = 0;
  }
}
