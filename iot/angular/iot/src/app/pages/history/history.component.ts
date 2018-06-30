import { Component, OnInit } from '@angular/core';
import { HistoryService } from '../../history.service';
import { Chart } from 'chart.js';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {

  chart = [];

  constructor(private historyService: HistoryService) { }

  ngOnInit() {
    const start = new Date();
    const end = new Date();
    const interval = 18;
    start.setTime(start.getTime() - 24 * 60 * 60 * 1000);
    const start_ep = Math.floor((start.getTime() + start.getTimezoneOffset() * 60 * 1000) / 1000);
    const end_ep = Math.floor((end.getTime() + end.getTimezoneOffset() * 60 * 1000) / 1000);

    this.historyService.historyData(start_ep, end_ep, interval)
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
                backgroundColor: '#3cba9f',
                borderColor: '#3cba9f',
                fill: false,
              },
              {
                label: 'Relative Humidity',
                data: relativeHumidity,
                backgroundColor: '#ffcc00',
                borderColor: '#ffcc00',
                fill: false,
              },
            ]
          },
          options: {
            tooltips: {
              mode: 'index',
              intersect: false,
            },
            elements: {
              point: {
                radius: 0,
              },
            },
          },
        });
      });
  }
}
