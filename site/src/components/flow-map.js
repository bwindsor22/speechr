import React from 'react';
import Plot from 'react-plotly.js';

class Examples extends React.Component{
  state = {
      data:[]
  }

  componentDidMount() {
    var proxyUrl = 'https://cors-anywhere.herokuapp.com/'
    var targetUrl = 'http://18.218.128.141:5000/percent_keyword_hate'
    fetch(proxyUrl + targetUrl)
      .then(response => response.json())
      .then(json => {
        console.log(json);
        this.setState({
          data: json,
        });
      })
      .catch((error) => {
          console.error(error);
      });
  }

  render() {
    var dates = this.state.data.map(function(data) {
      return (
        <div>
          {data.date}
        </div>
      );
    });

    return (
      <div>
        <div>
        <Plot
          data={[
            {
              type: 'scatter',
              mode: 'lines+points',
              x: [1, 2, 3],
              y: [2, 6, 3],
              marker: {color: 'red'}
            },
            {
              type: 'scatter',
              x: [1, 2, 3],
              y: [2, 5, 3]
            }
          ]}

          layout={{
            width: 600,
            height: 600,
            title: 'A Fancy Plot'
          }}
        />
        </div>
        <div>{dates}</div>
      </div>
    );
  }
};


export default Examples;
