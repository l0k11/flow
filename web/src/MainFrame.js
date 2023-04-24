import React from 'react';
import ContactBanner from './ContactBanner';
import Prompt from './Prompt';
import DateGroup from './MessageDateGroup';

class MainFrame extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            id: this.props.id
        }
    }
    
    componentDidUpdate(prevProps) {
        if (prevProps.id !== this.props.id) {
            this.setState({ id: this.props.id });
        }
    }
      
    
    render(){
        if (!this.state.id){
            return <div id="mainFrame"></div>
        }
        else {
            this.APIResp = [
                {
                    "id": "838",
                    "type": "income",
                    "content": "Hola",
                    "time": "1678227604"
                },
                {
                    "id": "839",
                    "type": "outcome",
                    "content": "Que tal?",
                    "time": "1678227920"
                },
                {
                    "id": "840",
                    "type": "outcome",
                    "content": "Que tal?",
                    "time": "1678308399"
                },
                {
                    "id": "838",
                    "type": "income",
                    "content": "Hola",
                    "time": "1678538144"
                },
                {
                    "id": "838",
                    "type": "outcome",
                    "content": "aDIOS",
                    "time": "1678538144"
                },
            ]

            this.users = {
                "123": "Luis",
                "321": "Isaac"
            }

            this.dateGroups = [];
            this.msgPerDate = {};

            this.APIResp.forEach(msg => {
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
                        <ContactBanner name={this.users[this.state.id]}/>
                    </div>
                    <div id='chatContainer'>
                        <div>
                            <div id='chat'>
                                {this.dateGroups.map(date => <DateGroup date={date} messages={this.msgPerDate[date]} />)}
                            </div>
                            <Prompt  />
                        </div>
                    </div>
                </div>
            )
        }
    }
}

export default MainFrame;