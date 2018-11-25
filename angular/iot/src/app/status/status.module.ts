import { NgModule } from '@angular/core';

import { SharedModule } from "../shared/shared.module";
import { MaterialModule } from "../shared/material.module";

import { StatusRoutingModule } from './status-routing.module';
import { StatusComponent } from "./status/status.component";
import { DeviceStatusComponent } from "./status/device-status/device-status.component";

@NgModule({
  declarations: [
    StatusComponent,
    DeviceStatusComponent,
  ],
  imports: [
    SharedModule,
    MaterialModule,

    StatusRoutingModule,
  ]
})
export class StatusModule { }
