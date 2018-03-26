import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { StatusComponent } from './status/status.component';
import { HistoryComponent } from './history/history.component';
import { NotfoundComponent } from './notfound/notfound.component';

const routes: Routes = [
  { path: '', redirectTo: '/status', pathMatch: 'full' },
  { path: 'status', component: StatusComponent },
  { path: 'history', component: HistoryComponent },
  { path: '**', component: NotfoundComponent},
];


@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
