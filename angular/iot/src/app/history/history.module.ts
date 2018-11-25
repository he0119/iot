import { NgModule } from '@angular/core';

import { SharedModule } from "../shared/shared.module";
import { MaterialModule } from "../shared/material.module";

import { HistoryRoutingModule } from './history-routing.module';
import { HistoryComponent } from "./history/history.component";

@NgModule({
  declarations: [
    HistoryComponent
  ],
  imports: [
    SharedModule,
    MaterialModule,

    HistoryRoutingModule,
  ]
})
export class HistoryModule { }
