import { InternalNgModuleRef } from "@angular/core/src/linker/ng_module_factory";

const HOME = '';
const STATUS = 'status';
const HISTORY = 'history';
export const SECTIONS = {
  [HOME]: 'Home',
  [STATUS]: 'Status',
  [HISTORY]: 'History',
};

export interface DeviceData {
  id: number;
  time: Date;
  data: object;
}

export interface Device {
  id: number;
  name: string;
  schema: object;
  display: object;
  createOn: Date;
  lastConnectOn: Date;
  offlineOn: Date;
  onlineStatus: Date;
}

export enum DeviceDataType {
  integer = 0,
  float,
  string,
  boolean,
}
