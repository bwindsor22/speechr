import React, { Component } from 'react';
import {
    BrowserRouter as Router,
    Route,
    Switch
 } from 'react-router-dom';

import Header from './header.js'

import HateVolumes from './community-metrics/summary-volumes.js'
import BOW from './community-metrics/bow.js'
import Keyword from './community-metrics/keyword.js'
import TotalScanned from './community-metrics/total-scanned.js'

import ToxicUsers from './user-metrics/most-toxic-users.js'

import Blog from './blog.js'
import About from './about.js'

class App extends Component {
  render() {
    return (
      <div>
          <Header />

          <Router onUpdate={() => window.scrollTo(0, 0)}>
            <Switch>
              <Route exact path="/" component={BOW} />

              <Route path="/summary_volumes" component={HateVolumes} />
              <Route path="/trends_bow" component={BOW} />
              <Route path="/trends_keyword" component = {Keyword} />
              <Route path="/total_scanned" component={TotalScanned} />

              <Route path="/most_toxic_users" component={ToxicUsers} />
              <Route path="/blog" component={Blog} />
              <Route path="/about" component={About} />
            </Switch>
          </Router>
      </div>
    );
  }
}

export default App;
