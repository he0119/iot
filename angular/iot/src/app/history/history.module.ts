import { NgModule } from '@angular/core';

import { SharedModule } from "../shared.module";
import { MaterialModule } from "../material.module";

import { HistoryRoutingModule } from './history-routing.module';
import { HistoryComponent } from "./history/history.component";

// Translate
import { HttpClient } from '@angular/common/http';
import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
export function createTranslateHttpLoader(http: HttpClient) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}

@NgModule({
  declarations: [
    HistoryComponent
  ],
  imports: [
    SharedModule,
    MaterialModule,

    HistoryRoutingModule,

    TranslateModule.forChild({
      loader: {
        provide: TranslateLoader,
        useFactory: (createTranslateHttpLoader),
        deps: [HttpClient]
      }
    }),
  ]
})
export class HistoryModule { }
