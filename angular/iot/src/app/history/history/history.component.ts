import { Component, OnDestroy, OnInit } from '@angular/core';
import { Chart } from 'chart.js';
import { DeviceService } from '../../_service/device.service';
import { HistoryService } from '../history.service';
import { Device, DeviceData } from '../../shared/documentation-items';
import { normalizeArray } from '../../_helpers/normalize-array';
import { ResizeService } from '../resize.service';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent implements OnInit, OnDestroy {
  chart: Chart;
  devices: Array<Device>;
  schema: object;

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

  chartHeight;
  chartWidth;
  resizeSubscription;

  constructor(
    private historyService: HistoryService,
    private deviceService: DeviceService,
    private resizeService: ResizeService
  ) { }

  ngOnInit() {
    this.resizeSubscription = this.resizeService.onResize$
      .subscribe(size => {
        this.getChartSize();
      });
    this.getChartSize();

    this.deviceService.devicesInfo()
      .subscribe((res: Array<Device>) => {
        this.devices = res;
        this.id = res[0].id;
        this.schema = this.getDeviceSchema();
        this.start.setTime(this.start.getTime() - 24 * 60 * 60 * 1000);
        this.drawChart(this.id, this.start, this.end, this.interval, this.showSettings);
      });
  }

  ngOnDestroy() {
    if (this.resizeSubscription) {
      this.resizeSubscription.unsubscribe();
    }
  }

  getChartSize() {
    const narbarHeight = document.getElementById('navbar').clientHeight;
    const headerHeight = document.getElementById('history-header').clientHeight;
    const innerHeight = window.innerHeight;
    const innerWidth = window.innerWidth;
    this.chartHeight = `${innerHeight - narbarHeight - headerHeight - 16}px`;
    this.chartWidth = `${innerWidth}px`;
  }

  onClick() {
    this.schema = this.getDeviceSchema();
    this.drawChart(this.id, this.start, this.end, this.interval, this.showSettings);
  }

  drawChart(id: number, start: Date, end: Date, interval: number, showSettings: boolean) {
    const startEp = Math.floor(start.getTime() / 1000);
    const endEp = Math.floor(end.getTime() / 1000);

    this.historyService.historyData(id, startEp, endEp, interval)
      .subscribe((res: Array<DeviceData>) => {
        const datasets = [];
        const time = [];
        const data = {};

        const colorNames = Object.keys(this.chartColors);

        res.forEach(devicedata => {
          time.push(new Date(devicedata.time));
          Object.keys(devicedata.data)
            .forEach(key => {
              if (this.schema[key].show || showSettings) {
                if (!data[key]) { data[key] = []; }
                data[key].push(devicedata.data[key]);
              }
            });
        });

        Object.keys(data)
          .forEach(key => {
            const colorName = colorNames[key.length % colorNames.length];
            const newColor = this.chartColors[colorName];

            datasets.push(
              {
                label: this.schema[key].displayName,
                data: data[key],
                fill: false,
                backgroundColor: newColor,
                borderColor: newColor
              });
          });

        if (this.chart) { this.chart.destroy(); }  // destroy exist chart first
        this.chart = new Chart('chart', {
          type: 'line',
          data: {
            labels: time,
            datasets
          },
          options: {
            maintainAspectRatio: false,
            tooltips: {
              mode: 'index',
              intersect: false
            },
            elements: {
              point: {
                radius: 0
              }
            },
            scales: {
              xAxes: [{
                type: 'time',
                distribution: 'linear'
              }]
            },
            pan: {
              enabled: true,
              mode: 'x',
              speed: 5,
              threshold: 10
            },
            zoom: {
              enabled: true,
              mode: 'x',
              limits: {
                max: 10,
                min: 0.5
              }
            }
          }
        });
      });
  }

  getRandomColor(): string {
    const letters = '0123456789ABCDEF'.split('');
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }

    return color;
  }

  getDeviceSchema(): object {
    let schema;
    this.devices.forEach(item => {
      if (item.id === this.id) {
        schema = normalizeArray(item.schema, 'name');
      }

    });

    return schema;
  }
}
