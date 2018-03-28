import React from 'react';
import Plotly from 'plotly.js'
import fetchVolumes from '../../lib/fetch-volumes'

export default class SummaryVolumes extends React.Component{
  state = {
      chart_data: [],
      layout:{}
  }

  componentWillMount() {
    var chart_data = fetchVolumes('rolling_total_hate')
    this.setState({chart_data:chart_data})
    this.setState({layout:{
      autosize: true,
      title: 'Hate Speech Volume by Community',
    }})
  }

  componentDidMount() {
    Plotly.newPlot('volume-plot', this.state.chart_data, this.state.layout);
  }

  render() {
    return (
      <div id="volume-plot" style={{width:'1200px', height:'600px'}}> </div>
    );
  }
};
