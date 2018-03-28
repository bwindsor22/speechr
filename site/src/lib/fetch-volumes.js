function getMock(endpoint) {
  console.log(endpoint);
  var mock = {}
  mock['rolling_total_hate'] =
  [{"subreddit":"uncensorednews","total_keyword_hate":17.0,"total_bow_hate":203.0},{"subreddit":"milliondollarextreme","total_keyword_hate":808.0,"total_bow_hate":5487.0},{"subreddit":"13451452251849519","total_keyword_hate":0.0,"total_bow_hate":31.0},{"subreddit":"todayilearned","total_keyword_hate":7.0,"total_bow_hate":84.0},{"subreddit":"aznidentity","total_keyword_hate":59.0,"total_bow_hate":1607.0},{"subreddit":"fatacceptance","total_keyword_hate":27.0,"total_bow_hate":180.0},{"subreddit":"news","total_keyword_hate":2.0,"total_bow_hate":680.0},{"subreddit":"politics","total_keyword_hate":3.0,"total_bow_hate":245.0},{"subreddit":"h3h3productions","total_keyword_hate":1.0,"total_bow_hate":7.0},{"subreddit":"cringeanarchy","total_keyword_hate":2.0,"total_bow_hate":113.0},{"subreddit":"samandtolki","total_keyword_hate":9.0,"total_bow_hate":386.0},{"subreddit":"sjwhate","total_keyword_hate":40.0,"total_bow_hate":758.0},{"subreddit":"the_donald","total_keyword_hate":5.0,"total_bow_hate":329.0},{"subreddit":"billionshekelsupreme","total_keyword_hate":3.0,"total_bow_hate":11.0},{"subreddit":"worldnews","total_keyword_hate":1.0,"total_bow_hate":145.0},{"subreddit":"conspiracy","total_keyword_hate":0.0,"total_bow_hate":225.0},{"subreddit":"imgoingtohellforthis","total_keyword_hate":30.0,"total_bow_hate":373.0},{"subreddit":"hapas","total_keyword_hate":36.0,"total_bow_hate":1208.0},{"subreddit":"debatereligion","total_keyword_hate":16.0,"total_bow_hate":1640.0},{"subreddit":"conservative","total_keyword_hate":36.0,"total_bow_hate":1544.0},{"subreddit":"documentaries","total_keyword_hate":72.0,"total_bow_hate":4485.0},{"subreddit":"communism","total_keyword_hate":0.0,"total_bow_hate":161.0},{"subreddit":"mgtow","total_keyword_hate":6.0,"total_bow_hate":208.0},{"subreddit":"lectures","total_keyword_hate":0.0,"total_bow_hate":85.0},{"subreddit":"gentilesunited","total_keyword_hate":0.0,"total_bow_hate":304.0}];


  return mock[endpoint]
}

function fetchVolumes( endpoint ) {
  var environment = 'LOCAL_NO_API'

  console.log("loading data");
  var data = []
  var url
  if (environment === 'LOCAL_NO_API') {
    data = getMock(endpoint)
  } else {
    if (environment === 'PROD') {
      var proxyUrl = 'https://cors-anywhere.herokuapp.com/'
      var targetUrl = 'http://18.218.128.141:5000/'
      url = proxyUrl + targetUrl + endpoint
    } else if (environment === 'LOCAL'){
      var localUrl = 'localhost:5000/'
      url = localUrl + endpoint
    }
    fetch(url)
      .then(response => response.json())
      .then(json => {
        data = json
      })
      .catch((error) => {
          console.error(error);
      });
  }

  console.log('loaded data');

  var keys = Object.keys(data[0]);
  keys = keys.filter(key => key !== "subreddit")

  var communities = data.map(data => data.subreddit);
  console.log(keys);

  var chart_data = []
  keys.forEach( key => {
      var series_data = data.map(data => data[key]);
      var series_obj = {
        type: 'bar',
        x: communities,
        y: series_data,
        name: key
      }
      chart_data.push(series_obj)
  })

  return(chart_data)
}
export default fetchVolumes
