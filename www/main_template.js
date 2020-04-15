
// Instantiate a websocket connection to the server
var websocket = new WebSocket("ws://"+window.location.hostname+":{{ws_port}}/");

var sliderObjects = {};

///////////////////////////////////////////////////////////////////////////////////////
// Auto-generated content for user-defined IO

{{user_content}}

// End Auto-generated content
///////////////////////////////////////////////////////////////////////////////////////

// Websocket rx message handler
websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    for(sliderID in data){
        val = data[sliderID];
        sliderObjects[sliderID].noUiSlider.set(val);
    }
};