import React from "react";

class ContactBanner extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            name: this.props.name,
            id: this.props.id
        }
    }
    render(){
        return(
            <div className="banner">
                {this.props.name}
            </div>
        )
    }
}

export default ContactBanner