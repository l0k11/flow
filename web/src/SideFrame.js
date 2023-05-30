import React from 'react';
import ChatSelect from './ChatSelect';
import ContactItem from './ContactItem';

class SideFrame extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            addVisibility: false,
            nameValue: "",
            ipValue: "",
            error: "",
            listVisibility: false,
            listSearch: "",
            contactList: [],
            convList: []
        };
        this.toggleAdd = this.toggleAdd.bind(this);
        this.toggleList = this.toggleList.bind(this);
        this.handleNameChange = this.handleNameChange.bind(this)
        this.handleIPChange = this.handleIPChange.bind(this)
        this.addContact = this.addContact.bind(this)
    }

    toggleAdd(){
        if (this.state.addVisibility === true) {
            this.setState({
                addVisibility: false,
                nameValue: "",
                ipValue: "",
                error: ""                
            });
        } else {
            this.setState({
                addVisibility: true
            });
        };
    }
    toggleList(){
        if (this.state.listVisibility === true) {
            this.setState({
                listVisibility: false,
                listSearch: ""          
            });
        } else {
            this.setState({
                listVisibility: true
            });
        };
    }
    handleNameChange(event){
        this.setState({ nameValue: event.target.value });
    }   
    handleIPChange(event){
        this.setState({ ipValue: event.target.value });
    }
    updateContactList(value){
        this.setState({
            contactList: value
        })
    }
    updateConvList(value){
        this.setState({
            convList: value
        })
    }
    ValidateIPaddress(ipaddress) {  
        if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress)) {  
          return (true)  
        } return (false)  
    }
    componentDidMount(){
        this.getContacts();
        this.getConvs();
    }
    shouldComponentUpdate(nextProps, nextState){
        if (nextProps.newMSG !== this.props.newMSG){
            let supArray = [];
            let check = 0;
            this.state.convList.forEach((conv) => {
                let users = conv[6].split(",")
                let senderID = users[0] === this.props.myID ? users[1] : users[0]
                if (senderID === this.props.receiverID){
                    supArray.unshift(conv);
                } else {
                    supArray.push(conv);
                    check += 1;
                }
                if (check == this.state.convList.length){
                    let convData = [conv[4], conv[6], conv[5], conv[2], conv[3]];
                    supArray.unshift(convData);
                }
            })
            this.setState({convList: supArray,});
        }
    }

    addContact(){
        if (this.state.nameValue && this.ValidateIPaddress(this.state.ipValue)){
            fetch(this.props.APIURL + "/api/contacts", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: this.state.nameValue,
                    ip: this.state.ipValue
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "0"){
                    this.toggleAdd()
                    window.location.reload()
                }
                else if (data.status === "1"){this.setState({ error: "User already in contacts" })}
                else if (data.status === "2"){this.setState({ error: "User not found" })}
            })
        } else {this.setState({ error: "Invalid name or IP provided" })}
    }

    getContacts(){
        fetch(this.props.APIURL + "/api/contacts", {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {this.updateContactList(data)})
    }

    getConvs(){
        fetch(this.props.APIURL + "/api/convs", {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {this.updateConvList(data)})
    }


    render(){
        const contactsSVG = <span id="contacts-svg" className="clickable" title='Contact list' onClick={this.toggleList}><svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" viewBox="0 0 12 12"><g><path d="M 1.539062 11.675781 L 1.539062 10.960938 L 10.460938 10.960938 L 10.460938 11.675781 Z M 1.539062 1.023438 L 1.539062 0.3125 L 10.460938 0.3125 L 10.460938 1.023438 Z M 6 6.550781 C 6.433594 6.550781 6.796875 6.402344 7.09375 6.113281 C 7.390625 5.820312 7.539062 5.460938 7.539062 5.039062 C 7.539062 4.605469 7.390625 4.242188 7.09375 3.949219 C 6.796875 3.660156 6.433594 3.511719 6 3.511719 C 5.574219 3.511719 5.214844 3.660156 4.917969 3.949219 C 4.621094 4.242188 4.476562 4.605469 4.476562 5.039062 C 4.476562 5.460938 4.621094 5.820312 4.917969 6.113281 C 5.214844 6.402344 5.574219 6.550781 6 6.550781 Z M 1.800781 10.25 C 1.492188 10.25 1.226562 10.136719 1 9.90625 C 0.773438 9.675781 0.664062 9.414062 0.664062 9.113281 L 0.664062 2.886719 C 0.664062 2.5625 0.773438 2.292969 1 2.074219 C 1.226562 1.859375 1.492188 1.75 1.800781 1.75 L 10.210938 1.75 C 10.511719 1.75 10.773438 1.863281 11 2.09375 C 11.226562 2.324219 11.335938 2.585938 11.335938 2.886719 L 11.335938 9.113281 C 11.335938 9.414062 11.226562 9.675781 11 9.90625 C 10.773438 10.136719 10.511719 10.25 10.210938 10.25 Z M 2.664062 9.25 L 9.335938 9.25 C 8.972656 8.707031 8.476562 8.292969 7.855469 8 C 7.234375 7.707031 6.617188 7.5625 6 7.5625 C 5.375 7.5625 4.757812 7.707031 4.148438 8 C 3.542969 8.292969 3.046875 8.707031 2.664062 9.25 Z M 2.664062 9.25 "/></g></svg></span>
        const addSVG = <span id="add-svg" className="clickable" title='Add contact' onClick={this.toggleAdd}><svg xmlns="http://www.w3.org/2000/svg" width="30px" height="30px" viewBox="0 0 12 12" version="1.1"><g><path d="M 9.3125 6.585938 L 9.3125 5.039062 L 7.761719 5.039062 L 7.761719 4.175781 L 9.3125 4.175781 L 9.3125 2.636719 L 10.175781 2.636719 L 10.175781 4.175781 L 11.710938 4.175781 L 11.710938 5.039062 L 10.175781 5.039062 L 10.175781 6.585938 Z M 4.523438 5.835938 C 3.882812 5.835938 3.363281 5.636719 2.96875 5.238281 C 2.574219 4.835938 2.375 4.320312 2.375 3.6875 C 2.375 3.054688 2.574219 2.539062 2.96875 2.136719 C 3.363281 1.738281 3.882812 1.539062 4.523438 1.539062 C 5.160156 1.539062 5.675781 1.734375 6.082031 2.132812 C 6.484375 2.527344 6.6875 3.046875 6.6875 3.6875 C 6.6875 4.320312 6.488281 4.835938 6.085938 5.238281 C 5.6875 5.636719 5.167969 5.835938 4.523438 5.835938 Z M 0.25 10.375 L 0.25 8.925781 C 0.25 8.566406 0.339844 8.253906 0.519531 7.980469 C 0.699219 7.710938 0.949219 7.5 1.273438 7.351562 C 1.910156 7.058594 2.476562 6.855469 2.976562 6.742188 C 3.476562 6.632812 3.988281 6.574219 4.511719 6.574219 C 5.054688 6.574219 5.574219 6.632812 6.074219 6.75 C 6.574219 6.867188 7.140625 7.066406 7.773438 7.351562 C 8.101562 7.492188 8.355469 7.699219 8.539062 7.96875 C 8.722656 8.238281 8.8125 8.558594 8.8125 8.925781 L 8.8125 10.375 Z M 0.25 10.375 "/></g></svg></span>
        return (
            <div id="sideFrame">
                <div>
                    <div id="header">
                        <div id="logo">
                            flow
                        </div>
                        <div id="controls">
                            {contactsSVG}
                            {this.state.listVisibility && <div className='BGForToggle' onClick={this.toggleList}></div>}
                            {this.state.listVisibility && <div id='contactList'>
                                    <div>
                                        <h3>Contact List</h3>
                                        <ul>
                                            {this.state.contactList.map(contact => {
                                                return <ContactItem id={contact[0]} name={contact[1]} APIURL={this.props.APIURL}/>
                                            })}
                                        </ul>
                                    </div>
                                </div>}
                            
                            {addSVG}
                            {this.state.addVisibility && <div className='BGForToggle' onClick={this.toggleAdd}></div>}
                            {this.state.addVisibility &&
                                <div id='addContact'>
                                    <div>
                                        <h3>Add a new contact</h3>
                                        <form>
                                            <input type='text' id='name-input' name='name' placeholder='Name' onChange={this.handleNameChange} value={this.state.nameValue}/>
                                            <input type='text' id='ip-input' name='ip' placeholder='IP' onChange={this.handleIPChange} value={this.state.ipValue}/>
                                            {this.state.error && <span className='error'>{this.state.error}</span>}
                                            <div>
                                                <button className='add main-btn' type='button' onClick={this.addContact}>Add Contact</button>
                                                <button className='cancel' onClick={this.toggleAdd}>Cancel</button>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            }
                        </div>
                    </div>
                    <div id="chats">
                        {this.state.convList.map(conv => {
                            let contactsArray = conv[1].split(",")
                            let contactID = contactsArray[0] === this.props.myID ? contactsArray[1] : contactsArray[0]
                            return <ChatSelect id={contactID} name={conv[2]} lastMsg={conv[3]} lastMsgTime={conv[4]} func_chid={this.props.func_chid} APIURL={this.props.APIURL}/>
                        })}
                    </div>
                </div>
            </div>
        )
    }
}

export default SideFrame;