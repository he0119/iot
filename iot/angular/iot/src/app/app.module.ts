import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { NavigationComponent } from './shared/navigation/navigation.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './/app-routing.module';

import { MatListModule } from '@angular/material/list';
import { MatButtonModule, MatMenuModule } from '@angular/material';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';

import { HistoryComponent } from './pages/history/history.component';
import { HomeComponent } from './pages/home/home.component';
import { NotfoundComponent } from './pages/notfound/notfound.component';
import { StatusComponent } from './pages/status/status.component';

@NgModule({
  declarations: [
    AppComponent,
    NavigationComponent,
    HistoryComponent,
    HomeComponent,
    NotfoundComponent,
    StatusComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,

    MatListModule,
    MatButtonModule,
    MatMenuModule,
    MatIconModule,
    MatToolbarModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
