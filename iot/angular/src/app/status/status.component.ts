import { Component, OnInit, Input, OnDestroy } from '@angular/core';

import { Status } from '../status';
import { StatusService } from '../status.service';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.scss']
})
export class StatusComponent implements OnInit, OnDestroy {
  @Input() status: Status;

  interval: any;

  constructor(private statusService: StatusService) { }

  getCurrentData() {
    this.statusService.currentData()
      .subscribe(status => this.status = status);
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
}
