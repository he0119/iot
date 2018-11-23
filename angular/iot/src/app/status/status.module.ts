import { NgModule } from '@angular/core';

import { SharedModule } from "../shared/shared.module";
import { MaterialModule } from "../shared/material.module";

import { StatusRoutingModule } from './status-routing.module';
import { StatusComponent } from "./status/status.component";
import { DeviceStatusComponent } from "./status/device-status/device-status.component";

// Translate
import { HttpClient } from '@angular/common/http';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
export function createTranslateHttpLoader(http: HttpClient) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}

@NgModule({
  declarations: [
    StatusComponent,
    DeviceStatusComponent,
  ],
  imports: [
    SharedModule,
    MaterialModule,

    StatusRoutingModule,

    TranslateModule.forChild({
      loader: {
        provide: TranslateLoader,
        useFactory: (createTranslateHttpLoader),
        deps: [HttpClient]
      }
    }),
  ]
})
export class StatusModule { }
