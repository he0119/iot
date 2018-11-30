import { Component, OnInit } from '@angular/core';
import { TranslateService } from '@ngx-translate/core';
import { DateAdapter } from '@angular/material/core';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  languageBtn;
  language;

  constructor(public translateService: TranslateService, private adapter: DateAdapter<any>) { }

  ngOnInit() {
    const browserLang = this.translateService.getBrowserLang();
    this.settingBtn(browserLang);
  }

  /*设置btn的文字和需要传递的参数*/
  settingBtn(language: string) {
    if (language === 'zh') {
      this.languageBtn = 'English';
      this.language = 'en';
    } else {
      this.languageBtn = '中文';
      this.language = 'zh';
    }
  }

  /*切换语言*/
  changeLanguage(lang: string) {
    this.translateService.use(lang);
    this.adapter.setLocale(lang);
    this.settingBtn(lang);
  }
}
