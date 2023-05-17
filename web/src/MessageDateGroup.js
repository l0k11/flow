import React from "react";
import IncomeMessage from './IncomeMessage';
import OutcomeMessage from './OutcomeMessage';

class DateGroup extends React.Component {
    render(){
        return (
            <div className="date-group">
                {this.props.messages.map(msg => {
                    if (msg[0] !== this.props.my_id) {
                        return <IncomeMessage content={msg[2]} time={msg[3]} />
                    } else {
                        return <OutcomeMessage content={msg[2]} time={msg[3]} />
                    }
                })}
                <div className="date"><p>{this.props.date}</p></div>
            </div>
        );
    };
};

export default DateGroup