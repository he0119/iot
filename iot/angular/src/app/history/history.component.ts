import { Component, OnInit } from '@angular/core';
import { HistoryService } from '../history.service';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  chart = [];

  constructor(private _history: HistoryService) { }

  ngOnInit() {
    const start = new Date();
    const end = new Date();
    const interval = 18;
    start.setTime(start.getTime() - 24 * 60 * 60 * 1000);
    const start_ep = Math.floor((start.getTime() + start.getTimezoneOffset() * 60 * 1000) / 1000);
    const end_ep = Math.floor((end.getTime() + end.getTimezoneOffset() * 60 * 1000) / 1000);

    this._history.historyData(start_ep, end_ep, interval)
      .subscribe(res => {
        const temperature = res['list'].map(temp => temp.temperature);
        const relativeHumidity = res['list'].map(temp => temp.relative_humidity);
        const time = res['list'].map(temp => temp.time.split(' ')[1]);
        this.chart = new Chart('canvas', {
          type: 'line',
          data: {
            labels: time,
            datasets: [
              {
                label: 'Temperature',
                data: temperature,
                borderColor: '#3cba9f',
                fill: false
              },
              {
                label: 'Relative Humidity',
                data: relativeHumidity,
                borderColor: '#ffcc00',
                fill: false
              },
            ]
          },
        });
      });
  }
}
