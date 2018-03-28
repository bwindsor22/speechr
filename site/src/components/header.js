import 'semantic-ui-css/semantic.min.css';

import React, { Component } from 'react'
import { Dropdown, Menu } from 'semantic-ui-react'

export default class MenuExampleSecondary extends Component {

  handleItemClick = (e, { name }) => this.setState({ activeItem: name })

  render() {
    return (
      <Menu pointing size='large'>
        <Dropdown item text='Community Metrics' onClick={this.handleItemClick}>
          <Dropdown.Menu>
            <Dropdown.Item href='/summary_volumes'>Summary - Volume by Community</Dropdown.Item>
            <Dropdown.Item href='/summary_percent'>Summary - % Hate by Community </Dropdown.Item>
            <Dropdown.Item href='/trends_bow'>Trends - BOW Detection</Dropdown.Item>
            <Dropdown.Item href='/trends_keyword'>Trends - Keyword Detection</Dropdown.Item>
            <Dropdown.Item href='/total_scanned'>Trends - Total Comments Scanned</Dropdown.Item>

          </Dropdown.Menu>
        </Dropdown>
        <Dropdown item text='User Metrics' onClick={this.handleItemClick}>
          <Dropdown.Menu>
            <Dropdown.Item href='/most_toxic_users'>Most Toxic Users</Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
        <Menu.Menu position='right'>
        <Menu.Item name='Blog' href='/blog' onClick={this.handleItemClick} />
        <Menu.Item name='About' href='/about' onClick={this.handleItemClick} />
        </Menu.Menu>
      </Menu>
    )
  }
}
