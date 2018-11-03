import { Component, OnInit } from '@angular/core';
import { HistoryService } from '../../shared/history.service';
import { Chart } from 'chart.js';
import { Device, DeviceData } from '../../shared/documentation-items';
import { DeviceService } from '../../shared/device.service';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {
  chart: Chart;
  devices: Device[];

  name = '';
  start = new Date();
  end = new Date();
  interval = 18;

  constructor(private historyService: HistoryService, private deviceService: DeviceService) { }

  ngOnInit() {
    this.deviceService.devicesInfo().subscribe((res: Device[]) => {
      this.devices = res;
      this.name = res[0].name;
      this.start.setTime(this.start.getTime() - 24 * 60 * 60 * 1000);
      this.drawChart(this.name, this.start, this.end, this.interval);
    })
  }

  onClick() {
    this.drawChart(this.name, this.start, this.end, this.interval);
  }

  drawChart(name: string, start: Date, end: Date, interval: number) {
    const start_ep = Math.floor(start.getTime() / 1000);
    const end_ep = Math.floor(end.getTime() / 1000);

    this.historyService.historyData(name, start_ep, end_ep, interval)
      .subscribe((res: DeviceData[]) => {
        const temperature = [];
        const relativeHumidity = [];
        const time = [];

        res.forEach(entry => {
          temperature.push(entry.data["temperature"]);
          relativeHumidity.push(entry.data["relative_humidity"]);
          time.push(new Date(entry.time));
        })

        if (this.chart) this.chart.destroy(); // Destroy exist chart first
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
                distribution: 'linear'
              }],
            }
          }
        });
      })
  }
}
