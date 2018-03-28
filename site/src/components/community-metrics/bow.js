import React from 'react';
import Plotly from 'plotly.js'
import fetchRates from '../../lib/fetch-rates'

export default class BOW extends React.Component{
  state = {
      chart_data: [],
      layout:{}
  }

  componentWillMount() {
    var chart_data = fetchRates('percent_bow_hate')
    this.setState({chart_data:chart_data})
    this.setState({layout:{
      autosize: true,
      title: 'Percent Hate Speech by Community (BOW Classifier)',
      yaxis: {
        tickformat: ',.0%',
      }
    }})
  }

  componentDidMount() {
    Plotly.newPlot('bow-plot', this.state.chart_data, this.state.layout);
  }

  render() {
    return (
      <div id="bow-plot" style={{width:'1200px', height:'600px'}}> </div>
    );
  }
};
