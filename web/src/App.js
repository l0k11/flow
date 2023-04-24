import './App.css';
import React from 'react';
import SideFrame from './SideFrame';
import MainFrame from './MainFrame';

class App extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            receiverID: null
        };
    };

    change_id = (id) => {
        this.setState({ id: id });
    }

    my_id(){
        
    }

    render(){
        return (
            <main>
                <SideFrame func_chid={this.change_id}/>
                <MainFrame id={this.state.receiverID}/>
            </main>
        );
    };
};

export default App;
