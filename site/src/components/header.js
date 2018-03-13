import 'semantic-ui-css/semantic.min.css';


import React, { Component } from 'react'
import { Dropdown, Menu } from 'semantic-ui-react'

export default class MenuExampleSecondary extends Component {
  state = { activeItem: 'home' }

  handleItemClick = (e, { name }) => this.setState({ activeItem: name })

  render() {
    const { activeItem } = this.state

    return (
      <Menu pointing size='large' style={{margin:'0px'}}>
        <Menu.Item name='Tiled heat map' href='/' onClick={this.handleItemClick} />
        <Menu.Item name='Attendance' href='/attendance' onClick={this.handleItemClick} />
        <Menu.Item name='Flow' href='/flow' onClick={this.handleItemClick} />
      </Menu>
    )
  }
}
