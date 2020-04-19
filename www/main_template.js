
// Instantiate a websocket connection to the server
var websocket = new WebSocket("ws://"+window.location.hostname+":{{ws_port}}/");

var sliderObjects = {};
var updateInhibitFlags = {};

///////////////////////////////////////////////////////////////////////////////////////
// Auto-generated content for user-defined IO

{{user_content}}

// End Auto-generated content
///////////////////////////////////////////////////////////////////////////////////////

// Websocket rx message handler
websocket.onmessage = function (event) {
    data = JSON.parse(event.data);
    for(sliderID in data){
        if(updateInhibitFlags[sliderID] == false){
            val = data[sliderID];
            curSliderVals = sliderObjects[sliderID].noUiSlider.get();
            if(!Array.isArray(curSliderVals)){
                if(!(JSON.parse(curSliderVals) === (val))){
                    //Each call to set() disables the user from being able to click the slider for 300ms. 
                    // To prevent user interaction woes, only call it if it's actually needed.
                    sliderObjects[sliderID].noUiSlider.set(val); 
                }
            } else {
                if(!(JSON.parse(curSliderVals[0]) === (val[0])) || !(JSON.parse(curSliderVals[1]) === (val[1]))){
                    //Each call to set() disables the user from being able to click the slider for 300ms. 
                    // To prevent user interaction woes, only call it if it's actually needed.
                    sliderObjects[sliderID].noUiSlider.set(val); 
                }
            }

        }
    }
};