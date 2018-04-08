import React from 'react';
import Plot from 'react-plotly.js';
import fetchRates from '../../lib/fetch-rates'

export default class SummaryVolumes extends React.Component{
  state = {
      loaded:false,
      chart_data: [],
      layout:{
        autosize: true,
        title: 'Hate Speech Volume by Community',
      }
  }

  componentWillMount() {
    fetchRates('rolling_total_hate')
      .then((chart_data) => this.setState({chart_data}))
      .then(this.setState({loaded:true}))
  }

  render() {
    return (
      <div>
      { this.state.loaded ?
        <Plot
        data={this.state.chart_data}
        layout={this.state.layout}
        style={{width:'1200px', height:'600px'}}
        />
        : <h1> Loading .. </h1>
      }
    </div>   );
  }
};
