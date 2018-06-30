import { Component, OnInit } from '@angular/core';
import { SECTIONS } from '../documentation-items';

const SECTIONS_KEYS = Object.keys(SECTIONS);

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.scss']
})
export class NavigationComponent implements OnInit {
  get sections() {
    return SECTIONS;
  }

  get sectionKeys() {
    return SECTIONS_KEYS;
  }

  constructor() { }

  ngOnInit() {
  }

}
