import { NgModule } from '@angular/core';

import { SharedModule } from '../shared/shared.module';
import { MaterialModule } from '../shared/material.module';

import { HistoryRoutingModule } from './history-routing.module';
import { HistoryComponent } from './history/history.component';

import { ResizeService } from './resize.service';
import { HistoryService } from './history.service';

import 'chartjs-plugin-zoom';

@NgModule({
  declarations: [
    HistoryComponent
  ],
  imports: [
    SharedModule,
    MaterialModule,

    HistoryRoutingModule,
  ],
  providers: [
    ResizeService,
    HistoryService,
  ]
})
export class HistoryModule { }
