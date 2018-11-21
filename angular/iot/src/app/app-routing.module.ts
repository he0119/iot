import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { HomeComponent } from './pages/home/home.component';
import { NotfoundComponent } from './pages/notfound/notfound.component';

const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'status', loadChildren: './status/status.module#StatusModule' },
  { path: 'history', loadChildren: './history/history.module#HistoryModule' },
  { path: '**', component: NotfoundComponent},
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule {}
