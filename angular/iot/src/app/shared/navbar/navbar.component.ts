import { Component } from '@angular/core';
import { SECTIONS } from '../documentation-items';
import { TranslateService } from '@ngx-translate/core';

const SECTIONS_KEYS = Object.keys(SECTIONS);

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss']
})
export class NavbarComponent {
  languageBtn;
  language;

  get sections() {
    return SECTIONS;
  }

  get sectionKeys() {
    return SECTIONS_KEYS;
  }

  constructor(public translateService: TranslateService) {
  }

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
    this.settingBtn(lang);
  }
}
