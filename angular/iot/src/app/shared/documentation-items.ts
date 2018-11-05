const HOME = '';
const STATUS = 'status';
const HISTORY = 'history';
export const SECTIONS = {
  [HOME]: 'Home',
  [STATUS]: 'Status',
  [HISTORY]: 'History',
};

export interface DeviceData {
  name: string;
  time: string;
  data: object;
}

export interface Device {
  name: string;
  schema: object;
  createOn: string;
  lastConnectOn: string;
  offlineOn: string;
  onlineStatus: string;
}

export enum DeviceDataType {
  integer = 0,
  float,
  string,
  boolean,
}
