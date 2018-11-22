import { NgModule } from '@angular/core';
import { SharedModule } from "../shared.module";
import { MaterialModule } from "../material.module";

import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login/login.component';

import { ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [LoginComponent],
  imports: [
    LoginRoutingModule,
    SharedModule,
    MaterialModule,
    ReactiveFormsModule,
  ]
})
export class LoginModule { }
