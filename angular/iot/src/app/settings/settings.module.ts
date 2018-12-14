import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { MaterialModule } from '../shared/material.module';

import { SettingsRoutingModule } from './settings-routing.module';
import { SettingsComponent } from './settings/settings.component';

@NgModule({
  declarations: [SettingsComponent],
  imports: [
    SharedModule,
    MaterialModule,

    SettingsRoutingModule
  ]
})
export class SettingsModule { }
