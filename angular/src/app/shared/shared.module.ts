import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { TranslateModule } from '@ngx-translate/core';

import { KeysPipe } from '../_helpers/keys.pipe';
import { LocalizedDatePipe } from '../_helpers/localized-date.pipe';

@NgModule({
  imports: [
    CommonModule,
  ],
  declarations: [
    LocalizedDatePipe,
    KeysPipe
  ],
  exports: [
    CommonModule,
    FormsModule,
    TranslateModule,

    LocalizedDatePipe,
    KeysPipe,
  ]
})
export class SharedModule { }
