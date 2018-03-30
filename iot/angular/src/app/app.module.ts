import { BrowserModule } from '@angular/platform-browser';
import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { StatusComponent } from './status/status.component';
import { HistoryComponent } from './history/history.component';
import { NotfoundComponent } from './notfound/notfound.component';

import { AppRoutingModule } from './/app-routing.module';

import { HistoryService } from './history.service';
import { StatusService } from './status.service';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    StatusComponent,
    HistoryComponent,
    NotfoundComponent,
  ],
  imports: [
    BrowserModule,
<<<<<<< HEAD
<<<<<<< HEAD
=======
    ServiceWorkerModule.register('/ngsw-worker.js', {enabled: environment.production}),
>>>>>>> 6c60934... Add Service Worker
=======
>>>>>>> c05af55... Disable Service Worker

    FormsModule,
    AppRoutingModule,
    HttpClientModule,

    MDBBootstrapModule.forRoot(),
  ],
  schemas: [ NO_ERRORS_SCHEMA ],
  providers: [
    HistoryService,
    StatusService,
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
