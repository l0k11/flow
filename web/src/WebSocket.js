class WebSocketConnection {
    constructor() {
        this.url = `http://${window.location.hostname}:${window.location.port}/api/my-ip`;
        this.websocket = null;
    }

    init() {
        return fetch(this.url, {
            method: "GET"
        })
            .then(response => response.json())
            .then(data => {
                this.websocket = new WebSocket(`ws://${data.ip}:6004`);
                return this.websocket;
            })
            .catch(() => { });
    }
}

const socketConnection = new WebSocketConnection();
socketConnection.init()
    .then(websocket => {
        console.log("WebSocket connection established:", websocket);
        window.globalWebSocket = websocket;
    })
    .catch(error => {
        console.error("Error initializing WebSocket connection:", error);
    });