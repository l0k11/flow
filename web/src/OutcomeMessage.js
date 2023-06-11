import React from "react";

class OutcomeMessage extends React.Component{
    constructor(props){
        super(props);
        this.hour = new Date(parseInt(this.props.time)).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    };
    render(){
        return (
            <div className="outcome message">
                <p>{this.props.content}</p>
                <div className="hour">{this.hour}</div>
            </div>
        );
    };
};

export default OutcomeMessage;