import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';

import { MatButtonModule } from '@angular/material/button';

import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatListModule } from '@angular/material/list';
import { MatRadioModule } from '@angular/material/radio';

import { MatDividerModule } from '@angular/material/divider';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';


import { NgModule } from '@angular/core';

import { ServiceWorkerModule } from '@angular/service-worker';
import { AppComponent } from './app.component';

import { environment } from '../environments/environment';
import { StatusService } from './status.service';
import { StatusComponent } from './status/status.component';
import { AppRoutingModule } from './/app-routing.module';
import { HistoryComponent } from './history/history.component';
import { NotfoundComponent } from './notfound/notfound.component';

@NgModule({
  declarations: [
    AppComponent,
    StatusComponent,
    HistoryComponent,
    NotfoundComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatTabsModule,
    MatCheckboxModule,
    MatRadioModule,
    MatMenuModule,
    MatToolbarModule,
    MatButtonModule,
    MatListModule,
    MatIconModule,
    MatDividerModule,
    MatSlideToggleModule,
    MatCardModule,
    MatGridListModule,
    ServiceWorkerModule.register('/ngsw-worker.js', { enabled: environment.production }),
    AppRoutingModule
  ],
  providers: [StatusService],
  bootstrap: [AppComponent]
})
export class AppModule { }
