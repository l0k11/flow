import './App.css';
import React from 'react';
import SideFrame from './SideFrame';
import MainFrame from './MainFrame';

class App extends React.Component{
    constructor(props){
        super(props)
        this.state = {
            id: null
        }
    }

    change_id = (id) => {
        this.setState({ id: id });
    }

    render(){
        console.log(this.state.id)
        return (
            <main>
                <SideFrame func_chid={this.change_id}/>
                <MainFrame id={this.state.id}/>
            </main>
        );
    };
};

export default App;
