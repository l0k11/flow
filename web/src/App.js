import './App.css';
import React from 'react';
import SideFrame from './SideFrame';
import MainFrame from './MainFrame';
import websocket from './WebSocket';

class App extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            myID: null,
            myIP: null,
            receiverID: null,
            receiverName: null,
            newMSG: null,
        };
        this.APIURL = `http://${window.location.hostname}:${window.location.port}`
    };

    change_id = (id, name) => {
        this.setState({ receiverID: id, receiverName: name });
    }

    my_id = () => {
        let url = this.APIURL + "/api/my-id";
        fetch(url, {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {
            this.setState({
                myID: data.id
            })
        })
        .catch(error => console.error(error));
    }

    my_ip = () => {
        let url = this.APIURL + "/api/my-ip";
        fetch(url, {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {
            this.setState({
                myIP: data.ip
            })
        })
        .catch(error => console.error(error));
    }

    componentDidUpdate() {
        console.log("Connected to ws")
        websocket.onmessage = (event) => {
            let message = event.data.split("/n/n");
            this.setState({ newMSG: message });
        }

    }

    componentWillUnmount() {
        this.websocket.close();
    }

    render(){
        if (!this.state.myID && !this.state.myIP){
            this.my_id();
            this.my_ip();
            return (<main></main>)
        }
        console.log(`Creds: ${this.state.myID} ${this.state.myIP}`)
        return (
            <main>
                {(this.state.myID && this.state.myIP) && 
                <SideFrame 
                    myID={this.state.myID}
                    func_chid={this.change_id}
                    APIURL={this.APIURL}
                    newMSG={this.state.newMSG}
                    receiverID={this.state.receiverID}
                />}
                
                {(this.state.myID && this.state.myIP) && 
                <MainFrame 
                    receiverID={this.state.receiverID} 
                    receiverName={this.state.receiverName}
                    senderID={this.state.myID}
                    ip={this.state.myIP}
                    APIURL={this.APIURL}
                    newMSG={this.state.newMSG}
                />}
            </main>
        );
    };
};

export default App;
