import React from "react";

class ChatSelect extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            "name": this.props.name,
            "lastMsg": this.props.lastMsg,
            "id": this.props.id
        }
    }
    render(){
        return (
            <div id={this.state.id} className="chat-select clickable">
                <h2>{this.state.name}</h2>
                {this.state.lastMsg && <h3>{this.state.lastMsg}</h3>}
            </div>
        );
    };
};

export default ChatSelect;