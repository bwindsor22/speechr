import React from 'react';

export default class About extends React.Component{
  render() {
    return (
      <div>
      <p> Speechr tracks hateful or toxic comments on Reddit, the world's 7th most visited website. </p>
      <h3> Purpose </h3>
      <p> Speechr has two goals: </p>
      <ul> Provide visibility to communities of content in violation of Reddit's Terms of Service.
      </ul>
      <ul>
        Be an open source resource for the study of hate in online communities.
      </ul>

      <h3> Inspiration </h3>
      <p> Speechr was inspired by a 2017 post by Reddit's CEO,
          indicating he was unaware of the extent of how toxic some communities
          were getting. At the same time, Facebook was hiring an extra 10,000 consultants
          to scan through comments.
          <br/> <br/>
          Reddit (the company) has always taken a more hands-off approach, prefering
          to let communities regulate themselves. This site provides tooling to help
          do this. </p>
      <h3> Contact </h3>
      <p> To get involved, join us on GitHub</p>
      </div>
    );
  }
};
