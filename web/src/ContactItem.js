import React from "react";

class ContactItem extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            id: this.props.id,
            name: this.props.name,
            editVisibility: false,
            nameValue: "",
            error: ""
        }
        this.toggleVisibility = this.toggleVisibility.bind(this)
    }

    toggleVisibility(){
        if (this.state.editVisibility === true) {
            this.setState({
                editVisibility: false,
                nameValue: "",
                error: ""
            });
        } else {
            this.setState({
                editVisibility: true
            });
        };
    }

    render(){
        const editSVG = <span id="edit-svg" className='clickable' title='Edit contact' onClick={this.toggleVisibility}><svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 96 960 960" width="20px"><path d="M794 390 666 262l42-42q17-17 42.5-16.5T793 221l43 43q17 17 17 42t-17 42l-42 42Zm-42 42L248 936H120V808l504-504 128 128Z"/></svg></span>
        return <li>
            <p>{this.state.name}</p>{editSVG}
            {this.state.editVisibility && <div className='BGForToggle' onClick={this.toggleVisibility}></div>}
            {this.state.editVisibility && <div id="editContact">
                <div>
                    <h3>Edit contact</h3>
                    
                </div>
            </div>}
        </li>
    }
}

export default ContactItem;