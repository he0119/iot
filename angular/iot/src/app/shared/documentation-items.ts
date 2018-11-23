const HOME = 'home';
const STATUS = 'status';
const HISTORY = 'history';
export const SECTIONS = {
  [HOME]: 'navbar.home',
  [STATUS]: 'navbar.status',
  [HISTORY]: 'navbar.history',
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
  integer = 1,
  float,
  boolean,
  string,
}
