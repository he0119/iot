import { Component, OnInit } from '@angular/core';
import { HistoryService } from '../../shared/history.service';
import { Chart } from 'chart.js';
import { DeviceData } from '../../shared/documentation-items';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {

  chart = [];

  constructor(private historyService: HistoryService) { }
  //TODO: Add support for multidevice
  ngOnInit() {
    const name = 'test';
    const start = new Date();
    const end = new Date();
    const interval = 18;
    start.setTime(start.getTime() - 24 * 60 * 60 * 1000);
    const start_ep = Math.floor(start.getTime() / 1000);
    const end_ep = Math.floor(end.getTime() / 1000);

    this.historyService.historyData(name, start_ep, end_ep, interval)
      .subscribe((res: DeviceData[]) => {
        const temperature = [];
        const relativeHumidity = [];
        const time = [];

        for (const entry of res) {
          temperature.push(entry.data["temperature"]);
          relativeHumidity.push(entry.data["relative_humidity"]);
          time.push(new Date(entry.time));
        };

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
            scales: {
              xAxes: [{
                type: 'time',
                time: {
                  displayFormats: {
                    quarter: 'MMM D h:mm a'
                  }
                }
              }],
            }
          }
        });
      })
  }
}
