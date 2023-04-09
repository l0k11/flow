import React from "react";
import EmojiPicker from "emoji-picker-react";

class Prompt extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            message: this.props.message,
            id: this.props.id,
            emojiVisibility: false,
            inputValue: ""
        };
        this.emojiToggle = this.emojiSelect.bind(this);
        this.handleEmojiClick = this.handleEmojiClick.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);
    };

    emojiSelect(){
        if (this.state.emojiVisibility === true) {
            this.setState({
                emojiVisibility: false
            });
        } else {
            this.setState({
                emojiVisibility: true
            });
        };
    };

    handleEmojiClick(emojiObject, event){
        this.setState({ inputValue: this.state.inputValue + emojiObject.emoji });
    };

    handleInputChange(event) {
        this.setState({ inputValue: event.target.value });
    }
    
    render(){
        const emojiSVG = 
            <span id="emoji-svg" className="clickable" onClick={this.emojiToggle}>
                <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" viewBox="0 96 960 960" version="1.1">
                    <path d="M626 523q22.5 0 38.25-15.75T680 469q0-22.5-15.75-38.25T626 415q-22.5 0-38.25 15.75T572 469q0 22.5 15.75 38.25T626 523Zm-292 0q22.5 0 38.25-15.75T388 469q0-22.5-15.75-38.25T334 415q-22.5 0-38.25 15.75T280 469q0 22.5 15.75 38.25T334 523Zm146 272q66 0 121.5-35.5T682 663H278q26 61 81 96.5T480 795Zm0 181q-83 0-156-31.5T197 859q-54-54-85.5-127T80 576q0-83 31.5-156T197 293q54-54 127-85.5T480 176q83 0 156 31.5T763 293q54 54 85.5 127T880 576q0 83-31.5 156T763 859q-54 54-127 85.5T480 976Zm0-400Zm0 340q142.375 0 241.188-98.812Q820 718.375 820 576t-98.812-241.188Q622.375 236 480 236t-241.188 98.812Q140 433.625 140 576t98.812 241.188Q337.625 916 480 916Z"/>
                </svg>
            </span>

        const sendSVG = 
            <span id="send-svg" className="clickable">
                <svg xmlns="http://www.w3.org/2000/svg" width="20px" height="20px" viewBox="0 96 960 960" version="1.1">
                    <path d="M120 896V256l760 320-760 320Zm60-93 544-227-544-230v168l242 62-242 60v167Zm0 0V346v457Z"/>
                </svg>
            </span>

        return (
            <div id='prompt'>
                {emojiSVG}
                {this.state.emojiVisibility && <div id="emojiPicker"><EmojiPicker onEmojiClick={this.handleEmojiClick} theme="dark"/></div>}
                {this.state.emojiVisibility && <div id="emojiBGToggle" onClick={this.emojiToggle}></div>}
                <input type='text' placeholder="Type your message..." value={this.state.inputValue} onChange={this.handleInputChange}/>
                {sendSVG}
            </div>
        )
    };
};

export default Prompt;