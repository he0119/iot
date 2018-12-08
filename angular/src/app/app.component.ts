import { Component, ViewEncapsulation, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { DateAdapter } from '@angular/material/core';
import { UpdateService } from "./_service/update.service";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  encapsulation: ViewEncapsulation.None,
})
export class AppComponent implements OnInit{

  constructor(private translateService: TranslateService, private adapter: DateAdapter<any>, private update: UpdateService) {
  }

  ngOnInit() {
    /* --- set i18n begin ---*/
    this.translateService.addLangs(['zh', 'en']);
    this.translateService.setDefaultLang('zh');
    const browserLang = this.translateService.getBrowserLang();

    let lang = browserLang.match(/zh|en/) ? browserLang : 'zh';
    this.translateService.use(lang);
    this.adapter.setLocale(lang);
    /* --- set i18n end ---*/
  }
}
