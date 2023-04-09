import React from "react";
import IncomeMessage from './IncomeMessage';
import OutcomeMessage from './OutcomeMessage';

class DateGroup extends React.Component {
    constructor(props){
        super(props);
    };
    render(){
        return (
            <div className="date-group">
                {this.props.messages.map(msg => {
                    if (msg.type === "income") {
                        return <IncomeMessage content={msg.content} time={msg.time} />
                    } else {
                        return <OutcomeMessage content={msg.content} time={msg.time} />
                    }
                })}
                <div className="date"><p>{this.props.date}</p></div>
            </div>
        );
    };
};

export default DateGroup