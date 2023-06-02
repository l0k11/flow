class WebSocket {
    constructor(){
        this.url = `http://${window.location.hostname}:${window.location.port}/api/my-ip`;
        fetch(this.url, {
            method: "GET"
        })
        .then(response => response.json())
        .then(data => {
            this.ip = data.ip
        })
        .catch(error => console.error(error));
        this.websocket = new WebSocket(`http://${this.ip}:6004`)
    }
}
let socket = new WebSocket();
export default socket.websocket;