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
        console.log(nextState.MSGList)
        console.log(this.state.MSGList)
        if (nextProps.receiverID !== this.props.receiverID){
            this.setState({ receiverID: nextProps.receiverID });
            this.getMessages(nextProps.receiverID);
            return true;
        } if (nextState.MSGList === this.state.MSGList) {
            return true;
        }
        return false;
    }
    updateMSGList(value){
        this.setState({
            MSGList: value
        })
    }
    getMessages(id){
        fetch(this.props.APIURL + "/api/messages/" + id)
        .then(response => response.json())
        .then(data => {this.updateMSGList(data)})
    }
    update_msgList = (msg) => {
        let newList = this.state.MSGList
        newList.push(msg)
        this.setState({ MSGList: newList });
    }
    
    render(){
        if (!this.state.receiverID){
            return <div id="mainFrame"></div>
        }
        else {
            this.dateGroups = [];
            this.msgPerDate = {};
            this.state.MSGList.forEach(msg => {
                let date = new Date(msg[3] * 1000).toLocaleDateString('en-US', {
                    year: "numeric",
                    month: "long",
                    day: "numeric",
                    timeStyle: undefined
                });
                if (!this.dateGroups.includes(date)) {
                    this.dateGroups.push(date);
                    this.msgPerDate[date] = []
                };
                this.msgPerDate[date].unshift(msg)
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
                            <Prompt receiverID={this.state.receiverID} senderID={this.state.senderID} update_msgList={this.update_msgList}/>
                        </div>
                    </div>
                </div>
            )
        }
    }
}

export default MainFrame;