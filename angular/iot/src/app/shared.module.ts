import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { KeysPipe } from "./shared/keys.pipe";
import { LocalizedDatePipe } from "./shared/localized-date.pipe";

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

    LocalizedDatePipe,
    KeysPipe,
  ]
})
export class SharedModule { }
