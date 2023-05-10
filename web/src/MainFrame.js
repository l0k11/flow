import React from 'react';
import Prompt from './Prompt';
import DateGroup from './MessageDateGroup';

class MainFrame extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            senderID: this.props.senderID,
            receiverID: this.props.receiverID,
            MSGList: []
        }
    }

    shouldComponentUpdate(nextProps, nextState){
        if (nextProps.receiverID !== this.props.receiverID){
            this.setState({ receiverID: nextProps.receiverID });
            this.getMessages(nextProps.receiverID);
            return true;
        }
        return false;
    }
    // componentDidUpdate(prevProps) {
    //     if (prevProps.receiverID !== this.props.receiverID) {
    //         this.setState({ receiverID: this.props.receiverID });
    //         this.getMessages(this.props.receiverID);
    //     };
    // };
    updateMSGList(value){
        this.setState({
            contactList: value
        })
    }
    getMessages(id){
        fetch(this.props.APIURL + "/api/messages/" + id)
        .then(response => response.json())
        .then(data => {console.log(data); this.updateMSGList(data)})
    }
    
    render(){
        if (!this.state.receiverID && this.state.MSGList === []){
            return <div id="mainFrame"></div>
        }
        else {
            this.dateGroups = [];
            this.msgPerDate = {};

            this.state.MSGList.forEach(msg => {
                let date = new Date(msg.time * 1000).toLocaleDateString('en-US', {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                    timeStyle: undefined
                });
                if (!this.dateGroups.includes(date)) {
                    this.dateGroups.unshift(date);
                    this.msgPerDate[date] = []
                };
                this.msgPerDate[date].unshift(msg);
            });
            return (
                <div id="mainFrame">
                    <div id='bannerContainer'>
                        <div className="banner">
                            {this.props.receiverName}
                        </div>
                    </div>
                    <div id='chatContainer'>
                        <div>
                            <div id='chat'>
                                {this.dateGroups.map(date => <DateGroup date={date} messages={this.msgPerDate[date]} />)}
                            </div>
                            <Prompt receiverID={this.state.receiverID} senderID={this.state.senderID} />
                        </div>
                    </div>
                </div>
            )
        }
    }
}

export default MainFrame;