import React from "react";
import IncomeMessage from './IncomeMessage';
import OutcomeMessage from './OutcomeMessage';

class DateGroup extends React.Component {
    render(){
        return (
            <div className="date-group">
                {this.props.messages.map(msg => {
                    if (msg[0] !== "u37c64162-f8c1-4985-ae09-d67ef858c571") {
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