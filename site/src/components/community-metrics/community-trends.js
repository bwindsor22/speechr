import React from 'react';
import Plot from 'react-plotly.js';
import Select from 'react-select';
import 'react-select/dist/react-select.css';

import fetchRates from '../../lib/fetch-rates'

export default class CommunityTrends extends React.Component{
  state = {
      loaded:false,
      classifierEndpoint: 'percent_bow_hate',
      chart_data: [],
      layout:{
        autosize: true,
        title: 'Percent Hate Speech by Community',
        yaxis: {
          tickformat: ',.0%',
        }
      }
  }

  selectOptions = [
    { value: 'percent_bow_hate', label: 'Bag of Words' },
    { value: 'percent_keyword_hate', label: 'Keyword Classifier' },
  ]

  handleChange = (classifierEndpoint) => {
    this.setState({ classifierEndpoint });
    this.setDataFromEndpoint(classifierEndpoint.value);
    console.log(`Selected: ${classifierEndpoint.label}`);
  }


  setDataFromEndpoint = (endpoint) => {
    fetchRates(endpoint)
      .then((data) => this.updateChartData(data))
      .then(() => this.setState({loaded:true}))
  }

  updateChartData = (chart_data) => {
    console.log(chart_data);
    this.setState({chart_data:chart_data})
  }

  componentWillMount() {
    this.setDataFromEndpoint('percent_bow_hate')
  }


  render() {
    return (
      <div>
      <Select
        value={this.state.classifierEndpoint}
        onChange={this.handleChange}
        clearable={false}
        options={this.selectOptions}
      />
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
