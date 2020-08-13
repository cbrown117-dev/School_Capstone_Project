import React, { Component } from 'react';
import { connect } from 'react-redux';

//imported house components
import overall from "./overallView.png";
import LightBulb from "./lightbulb.jpg";

class House extends Component{

  render(){
    return(
      <div className='House'>
      <img 
      src={overall} 
      style={{
        backgroundImage: `url(require("./houseComponents/overallView.png"))`,
        backgroundPosition: 'left',
        backgroundSize: '200px 200px'
      }}/>

      </div>
    );
  }
}



//for every page you need a mapStateToProps for every component
const mapStateToProps = (state) => {
  return {
      oven: state.oven,
      frontDoor: state.frontDoor
  }
}

const mapStateToProps = state => {
  return {
    age: state.age,
    oven: state.oven,
    frontDoor: state.frontDoor,
    devices: state.devices,
    devicelist: state.rawdevicelist,
    hvac: state.hvac
  };
};

export default connect(mapStateToProps)(House);
