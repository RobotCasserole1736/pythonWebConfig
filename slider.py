from abstractWebObjects import webUserInput

class Slider(webUserInput):
    
    def __init__(self, name, minVal, maxVal, defaultVal):
        self.name = name
        self.minVal = minVal
        self.maxVal = maxVal
        self.defaultVal = defaultVal
        
        self.value = self.defaultVal
        self.id = self.name.replace(" ", "_")
    
    def getHTML(self):
        return """
                <div class="slidecontainer">
                    <h3>{1}</h3>
                    <div id="{0}_slider"></div>
                    <div id="{0}_readout"> ?? </div>
                </div>
                <br>
               """.format(self.id, self.name)

    def getJS(self):
        return """
                sliderObjects[\"{0}\"] = document.getElementById('{0}_slider');

                noUiSlider.create(sliderObjects[\"{0}\"], {{
                    start: [{3}],
                    range: {{
                        'min': [{1}],
                        'max': [{2}]
                    }}
                }});

                sliderObjects[\"{0}\"].noUiSlider.on('slide', function(values, handle, unencoded){{
                    if(websocket.readyState == WebSocket.OPEN){{
                        websocket.send(JSON.stringify({{action: 'set', id: \"{0}\", value: unencoded}}));
                    }}
                
                }});









               """.format(self.id, self.minVal, self.maxVal, self.defaultVal)

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def getID(self):
        return self.id
       

    def setValue(self, value):
        self.value = value
        if(self.value > self.maxVal):
            self.value = self.maxVal
        elif(self.value < self.minVal):
            self.value = self.minVal

