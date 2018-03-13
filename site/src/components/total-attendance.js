import React from 'react';
import Chart from './highcharts.js';

const options = {
  chart: {
      type: 'area'
  },
  title: {
      text: 'Total Attendance by Quarter'
  },
  xAxis: {
      categories: ['2016 Avg', 'Q1', 'Q2', 'Q3', 'Q4']
  },
  credits: {
      enabled: false
  },
  series: [{
      name: 'East',
      data: [5, 3, 4, 7, 2]
  }, {
      name: 'South',
      data: [2, 7, 3, 2, 1]
  }, {
      name: 'North',
      data: [3, 4, 4, 2, 5]
  }]
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
