import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AppRoutingModule } from './app-routing.module';

import { HistoryComponent } from './pages/history/history.component';
import { HomeComponent } from './pages/home/home.component';
import { NotfoundComponent } from './pages/notfound/notfound.component';
import { StatusComponent } from './pages/status/status.component';
import { DeviceStatusComponent } from './pages/status/device-status/device-status.component';

import { KeysPipe } from './shared/keys.pipe';

import { MatListModule } from '@angular/material/list';
import { MatButtonModule, MatMenuModule, MatNativeDateModule } from '@angular/material';
import { MatIconModule } from '@angular/material/icon';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatCheckboxModule } from '@angular/material/checkbox';

import { TranslateHttpLoader } from '@ngx-translate/http-loader';
import { TranslateLoader, TranslateModule } from '@ngx-translate/core';
import { LocalizedDatePipe } from './shared/localized-date.pipe';

// 这里配置
export function createTranslateHttpLoader(http: HttpClient) {
  return new TranslateHttpLoader(http, './assets/i18n/', '.json');
}
import { registerLocaleData } from '@angular/common';
import localeZh from '@angular/common/locales/zh';

// the second parameter 'zh' is optional
registerLocaleData(localeZh, 'zh');

//TODO: Rearrange the stuctrue
@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HistoryComponent,
    HomeComponent,
    NotfoundComponent,
    StatusComponent,
    KeysPipe,
    DeviceStatusComponent,
    LocalizedDatePipe,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,

    TranslateModule.forRoot({
      loader: {
        provide: TranslateLoader,
        useFactory: (createTranslateHttpLoader),
        deps: [HttpClient]
      }
    }),

    MatListModule,
    MatButtonModule,
    MatMenuModule,
    MatIconModule,
    MatSlideToggleModule,
    MatCardModule,
    MatFormFieldModule,
    MatDatepickerModule,
    MatInputModule,
    MatSelectModule,
    MatNativeDateModule,
    MatSnackBarModule,
    MatExpansionModule,
    MatCheckboxModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
