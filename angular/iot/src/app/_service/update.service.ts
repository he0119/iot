import { Injectable } from '@angular/core';

import { MatSnackBar } from '@angular/material';
import { SwUpdate } from '@angular/service-worker';
import { TranslateService } from '@ngx-translate/core';

@Injectable({
  providedIn: 'root'
})
export class UpdateService {
  constructor(private swUpdate: SwUpdate, private snackbar: MatSnackBar, private translate: TranslateService) {
    this.swUpdate.available.subscribe(event => {
      let availableString;
      let reloadString;
      this.translate.get("update.available").subscribe((res: string) => {
        availableString = res;
      })
      this.translate.get("update.reload").subscribe((res: string) => {
        reloadString = res;
      })

      const snack = this.snackbar.open(availableString, reloadString);

      snack
        .onAction()
        .subscribe(() => {
          swUpdate.activateUpdate().then(() => document.location.reload());
        });

      setTimeout(() => {
        snack.dismiss();
      }, 6000);
    });
  }
}
