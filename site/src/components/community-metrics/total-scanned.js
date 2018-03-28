import React from 'react';
import Plotly from 'plotly.js'
import fetchRates from '../../lib/fetch-rates'

export default class BOW extends React.Component{
  state = {
      chart_data: [],
      layout:{}
  }

  componentWillMount() {
    var chart_data = fetchRates('daily_total_scanned')
    this.setState({chart_data:chart_data})
    this.setState({layout:{
      autosize: true,
      title: 'Total Comments Scanned',
    }})
  }

  componentDidMount() {
    Plotly.newPlot('total-scanned-plot', this.state.chart_data, this.state.layout);
  }

  render() {
    return (
      <div id="total-scanned-plot" style={{width:'1200px', height:'600px'}}> </div>
    );
  }
};
