import { Component, OnInit } from '@angular/core';
import { Chart } from 'chart.js';
import { TranslateService } from '@ngx-translate/core';
import { DeviceService } from '../../shared/device.service';
import { HistoryService } from '../../shared/history.service';
import { Device, DeviceData } from '../../shared/documentation-items';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit {
  chart: Chart;
  devices: Device[];

  id: number;
  start = new Date();
  end = new Date();
  interval = 18;
  showSettings = false;

  chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
  };

  constructor(private historyService: HistoryService, private deviceService: DeviceService, private translate: TranslateService) { }

  ngOnInit() {
    this.deviceService.devicesInfo().subscribe((res: Device[]) => {
      this.devices = res;
      this.id = res[0].id;
      this.start.setTime(this.start.getTime() - 24 * 60 * 60 * 1000);
      this.drawChart(this.id, this.start, this.end, this.interval, this.showSettings);
    })
  }

  onClick() {
    this.drawChart(this.id, this.start, this.end, this.interval, this.showSettings);
  }

  drawChart(id: number, start: Date, end: Date, interval: number, showSettings: boolean) {
    const start_ep = Math.floor(start.getTime() / 1000);
    const end_ep = Math.floor(end.getTime() / 1000);

    this.historyService.historyData(id, start_ep, end_ep, interval)
      .subscribe((res: DeviceData[]) => {
        const datasets = [];
        const data = {};
        const time = [];
        const display = this.getDisplay();

        let colorNames = Object.keys(this.chartColors);

        res.forEach(devicedata => {
          time.push(new Date(devicedata.time));
          Object.keys(devicedata.data).forEach(key => {
            if (display[key][0] || showSettings) {
              if (!data[key]) data[key] = [];
              data[key].push(devicedata.data[key]);
            }
          })
        })

        Object.keys(data).forEach(key => {
          let translateName;
          let colorName = colorNames[key.length % colorNames.length];
          let newColor = this.chartColors[colorName];
          this.translate.get("device_status." + key).subscribe((res: string) => {
            translateName = res;
          })
          datasets.push(
            {
              "label": translateName,
              "data": data[key],
              "fill": false,
              "backgroundColor": newColor,
              "borderColor": newColor
            })
        })

        if (this.chart) this.chart.destroy(); // Destroy exist chart first
        this.chart = new Chart('canvas', {
          type: 'line',
          data: {
            labels: time,
            datasets: datasets,
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

  getRandomColor(): string {
    let letters = '0123456789ABCDEF'.split('');
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  getDisplay(): object {
    let display = {};
    this.devices.forEach(device => {
      if (device.id = this.id) {
        display = device.display;
      }
    })
    return display;
  }

}
