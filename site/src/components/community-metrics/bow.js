import React from 'react';
import Plot from 'react-plotly.js';
import fetchRates from '../../lib/fetch-rates'

export default class BOW extends React.Component{
  state = {
      loaded:false,
      chart_data: [],
      layout:{
        autosize: true,
        title: 'Percent Hate Speech by Community (BOW Classifier)',
        yaxis: {
          tickformat: ',.0%',
        }
      }
  }

  updateChartData = (chart_data) => {
    console.log(chart_data);
    this.setState({chart_data:chart_data})
    this.setState({loaded:true})
  }

  componentWillMount() {
    fetchRates('percent_bow_hate')
      .then((data) => this.updateChartData(data))
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
      </div>
    );
  }
};
