import React from "react";

class ContactItem extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            id: this.props.id,
            name: this.props.name,
            editVisibility: false,
            deleteVisibility: false,
            nameValue: this.props.name,
            error: ""
        };
        this.toggleEdit = this.toggleEdit.bind(this);
        this.handleChange = this.handleChange.bind(this);
        this.toggleDelete = this.toggleDelete.bind(this);
        this.editContact = this.editContact.bind(this);
        this.deleteContact = this.deleteContact.bind(this);
    }

    toggleEdit(){
        if (this.state.editVisibility === true) {
            this.setState({
                editVisibility: false,
                nameValue: this.props.name,
                error: ""
            });
        } else {
            this.setState({
                editVisibility: true
            });
        };
    }
    toggleDelete(){
        if (this.state.deleteVisibility === true) {
            this.setState({
                deleteVisibility: false
            });
        } else {
            this.setState({
                deleteVisibility: true
            });
        };
    }
    handleChange(event){this.setState({nameValue: event.target.value});};
    
    editContact(){
        if (this.state.nameValue){
            fetch(this.props.APIURL + "/api/contacts", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: this.state.nameValue,
                    id: this.state.id
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "0"){
                    this.toggleEdit()
                    window.location.reload()
                }
                else if (data.status === "1"){this.setState({ error: `Username ${this.state.nameValue} already in contacts` })}
            })
        } else {this.setState({ error: "Invalid name provided" })}
    }

    deleteContact(){
        fetch(this.props.APIURL + "/api/contacts", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                id: this.state.id
            })
        })
        .then(window.location.reload())
    }

    render(){
        const editSVG = <span id="edit-svg" className='clickable' title='Edit contact' onClick={this.toggleEdit}><svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 96 960 960" width="20px"><path d="M794 390 666 262l42-42q17-17 42.5-16.5T793 221l43 43q17 17 17 42t-17 42l-42 42Zm-42 42L248 936H120V808l504-504 128 128Z"/></svg></span>
        const deleteSVG = <span id="edit-svg" className='clickable' title='Delete contact' onClick={this.toggleDelete}><svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 96 960 960" width="20px"><path d="M261 936q-24 0-42-18t-18-42V306h-41v-60h188v-30h264v30h188v60h-41v570q0 24-18 42t-42 18H261Zm106-146h60V391h-60v399Zm166 0h60V391h-60v399Z"/></svg></span>

        return <li>
            <p>{this.state.name}</p>{editSVG}{deleteSVG}
            
            {this.state.editVisibility && <div className='BGForToggle' onClick={this.toggleEdit}></div>}
            {this.state.editVisibility && <div id="editContact">
                <div>
                    <h3>Edit contact</h3>
                    <input type="text" value={this.state.nameValue} onChange={this.handleChange}/>
                    {this.state.error && <span className='error'>{this.state.error}</span>}
                    <div>
                        <button className='edit main-btn' type='button' onClick={this.editContact}>Edit Contact</button>
                        <button className='cancel' onClick={this.toggleEdit}>Cancel</button>
                    </div>
                </div>
            </div>}

            {this.state.deleteVisibility && <div className='BGForToggle' onClick={this.toggleDelete}></div>}
            {this.state.deleteVisibility && <div id="deleteContact">
                <div>
                    <h3>Delete contact</h3>
                    <p>Are you sure you want to delete {this.state.name}?</p>
                    {this.state.error && <span className='error'>{this.state.error}</span>}
                    <div>
                        <button className='delete' type='button' onClick={this.deleteContact}>Delete</button>
                        <button className='cancel' onClick={this.toggleDelete}>Cancel</button>
                    </div>
                </div>    
            </div>}
        </li>
    }
}

export default ContactItem;