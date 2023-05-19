import './App.css';
import React from 'react';
import SideFrame from './SideFrame';
import MainFrame from './MainFrame';

class App extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            myID: null,
            myIP: null,
            receiverID: null,
            receiverName: null
        };
        this.APIURL = "http://localhost:5000"
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
                myID: data.id,
                receiverID: this.state.receiverID
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

    render(){
        if (!this.state.myID){
            this.my_id();
            this.my_ip();
        }
        return (
            <main>
                {this.state.myID && <SideFrame myID={this.state.myID} func_chid={this.change_id} APIURL={this.APIURL}/>}
                {this.state.myID && <MainFrame receiverID={this.state.receiverID} receiverName={this.state.receiverName} senderID={this.state.myID} ip={this.state.myIP} APIURL={this.APIURL}/>}
            </main>
        );
    };
};

export default App;
