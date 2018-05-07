import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { Status } from '../status';
import { StatusService } from '../status.service';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit, OnDestroy {
  @Input() status: Status;
  interval: any;
  relay1 = 'OFF';
  relay2 = 'OFF';

  constructor(private statusService: StatusService) { }

  getCurrentData() {
    this.statusService.currentData()
      .subscribe(status => {
        this.status = status;
        if (this.status) {
          this.relay1 = this.status.relay1Status ? 'ON' : 'OFF';
          this.relay2 = this.status.relay2Status ? 'ON' : 'OFF';
        }
      });
  }

  ngOnInit() {
    this.getCurrentData();
    this.interval = setInterval(() => {
      this.getCurrentData();
      }, 10000);
  }

  ngOnDestroy() {
    clearInterval(this.interval);
  }

  changeRelay1() {
    this.statusService.setRelayState(1, this.relay1)
      .subscribe(result =>
        console.log(result)
      );
  }
  changeRelay2() {
    this.statusService.setRelayState(2, this.relay2)
    .subscribe(result =>
      console.log(result)
    );
  }
}
