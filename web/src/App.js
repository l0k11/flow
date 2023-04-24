import './App.css';
import React from 'react';
import SideFrame from './SideFrame';
import MainFrame from './MainFrame';

class App extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            myID: null,
            receiverID: null
        };
        // this.my_id = this.my_id.bind(this)
    };

    change_id = (id) => {
        this.setState({ receiverID: id });
    }

    my_id = () => {
        let url = "http://localhost:5000/api/my-id";
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

    render(){
        if (!this.state.myID){
            this.my_id()
        }
        return (
            <main>
                <SideFrame func_chid={this.change_id}/>
                {this.state.myID && <MainFrame receiverID={this.state.receiverID} senderID={this.state.myID}/>}
            </main>
        );
    };
};

export default App;
