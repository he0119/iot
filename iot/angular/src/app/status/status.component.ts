import { Component, OnInit, Input } from '@angular/core';

import { Status } from '../status';
import { StatusService } from '../status.service';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit {
  @Input() status: Status;

  constructor(
    private statusService: StatusService
  ) { }

  ngOnInit(): void {
    this.getStatus();
  }

  getRelayText(relay: boolean): string {
    if (relay) {
      return 'ON';
    }
    return 'OFF';
  }

  getStatus(): void {
    this.statusService.getStatus()
      .subscribe(status => this.status = status);
  }
}
