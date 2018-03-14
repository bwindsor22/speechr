import React from 'react';
import Chart from './highcharts.js';

const options = {
  chart: {
      type: 'tilemap',
      height: '70%'
  },

  title: {
      text: 'Concentration by region'
  },

  subtitle: {
      text: 'subtext'
  },

  xAxis: {
      visible: false
  },

  yAxis: {
      visible: false
  },

  colorAxis: {
      dataClasses: [{
          to: 10000000,
          color: '#AFEEEE',
          name: '< 10 million'
      }, {
          from: 10000000,
          to: 100000000,
          color: '#00BFFF',
          name: '10 to 100 million'
      }, {
          from: 100000000,
          to: 1000000000,
          color: '#1E90FF',
          name: '100 million to 1 billion'
      }, {
          from: 1000000000,
          color: '#0000FF',
          name: '> 1 billion'
      }]
  },

  tooltip: {
      headerFormat: '<b>{point.key}</b><br/>',
      pointFormat: 'The total minutes spent is <b>{point.value}</b>.'
  },

  series: [{
      dataLabels: {
          enabled: true,
          format: '{point.hc-a2}',
          color: '#000000',
          style: {
              textOutline: false
          }
      },
      data: [{
          'hc-a2': 'AC',
          name: 'Acre',
          x: 1,
          y: 3,
          value: 13459000
      }, {
          'hc-a2': 'AL',
          name: 'Alagoas',
          x: 7,
          y: 3,
          value: 40975000
      }, {
          'hc-a2': 'AM',
          name: 'Amazonas',
          x: 2,
          y: 3,
          value: 86669000
      }, {
          'hc-a2': 'AP',
          name: 'Amapá',
          x: 3,
          y: 4,
          value: 13400000
      }, {
          'hc-a2': 'CE',
          name: 'Ceará',
          x: 5,
          y: 4,
          value: 126054000
      }, {
          'hc-a2': 'DF',
          name: 'Distrito Federal',
          x: 5,
          y: 2,
          value: 197432000
      }, {
          'hc-a2': 'MA',
          name: 'Maranhão',
          x: 4,
          y: 3,
          value: 76842000
      }, {
          'hc-a2': 'PA',
          name: 'Pará',
          x: 3,
          y: 3,
          value: 124585000
      }, {
          'hc-a2': 'PB',
          name: 'Paraíba',
          x: 7,
          y: 4,
          value: 52936000
      }, {
          'hc-a2': 'PE',
          name: 'Pernambuco',
          x: 6,
          y: 3,
          value: 155143000
      }, {
          'hc-a2': 'PI',
          name: 'Piauí',
          x: 5,
          y: 3,
          value: 37723000
      }, {
          'hc-a2': 'RN',
          name: 'Rio Grande do Norte',
          x: 6,
          y: 4,
          value: 54023000
      }, {
          'hc-a2': 'RO',
          name: 'Rondônia',
          x: 2,
          y: 2,
          value: 34031000
      }, {
          'hc-a2': 'RR',
          name: 'Roraima',
          x: 2,
          y: 4,
          value: 9744000
      }, {
          'hc-a2': 'SE',
          name: 'Sergipe',
          x: 6,
          y: 2,
          value: 37472000
      }, {
          'hc-a2': 'TO',
          name: 'Tocantins',
          x: 4,
          y: 2,
          value: 26189000
      }
    ]
  }]

  };

class Tiled extends React.Component{
  render() {
      return React.createElement( Chart,
              {
                container: 'chart-tilemap',
                options: options
              }
      );
  }
};


export default Tiled;
