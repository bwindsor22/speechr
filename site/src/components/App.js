import React, { Component } from 'react';
import {
    BrowserRouter as Router,
    Route,
    Switch
 } from 'react-router-dom';


import Header from './header.js'

import TiledHeatMap from './tiled-heat-map.js'
import Attendance from './total-attendance.js'
import FlowMap from './flow-map.js'
import Blog from './my-blog.js'

class App extends Component {
  render() {
    return (
      <div>
          <Header />

          <Router onUpdate={() => window.scrollTo(0, 0)}>
            <Switch>
              <Route exact path="/" component={TiledHeatMap} />
              <Route path="/attendance" component={Attendance} />
              <Route path="/flow" component={FlowMap} />
              <Route path="/blog" component={Blog} />
            </Switch>
          </Router>
      </div>
    );
  }
}

export default App;
