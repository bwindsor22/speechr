import React from 'react';
import Chart from './highcharts.js';

const options = {

};

class Examples extends React.Component{

  render() {
      return React.createElement( Chart,
              {
                container: 'chart-name',
                options: options
              }
      );
  }
};


export default Examples;
