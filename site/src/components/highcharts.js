import React from 'react';
import Highcharts from 'highcharts';
import addHeatmap from 'highcharts/modules/heatmap'
import addTilemap from 'highcharts/modules/tilemap'
import addSankey from 'highcharts/modules/sankey'
addHeatmap(Highcharts)
addTilemap(Highcharts)
addSankey(Highcharts)

class MyCharts extends React.Component{
    // When the DOM is ready, create the chart.
    componentDidMount = () => {
        // Extend Highcharts with modules
        if (this.props.modules) {
            this.props.modules.forEach(function (module) {
                module(Highcharts);
            });
        }
        // Set container which the chart should render to.
        this.chart = new Highcharts[this.props.type || "Chart"](
            this.props.container,
            this.props.options
        );
    }
    //Destroy chart before unmount.
    componentWillUnmount = () => {
        this.chart.destroy();
    }
    //Create the div which the chart will be rendered to.
    render() {
        return React.createElement('div', { id: this.props.container });
    }
}
export default MyCharts
