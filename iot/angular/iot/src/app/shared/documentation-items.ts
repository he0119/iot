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
  time: Date;
  data: object;
}
