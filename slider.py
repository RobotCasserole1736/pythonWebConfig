from abstractWebObjects import webUserInput
import textwrap

class Slider(webUserInput):
    
    def __init__(self, name, minVal, maxVal, defaultVal):
        self.name = name
        self.minVal = minVal
        self.maxVal = maxVal
        self.defaultVal = defaultVal
        
        self.value = self.defaultVal
        self.id = self.name.replace(" ", "_")
    
    def getHTML(self):
        text = """
                <!-- Slider {1} -->
                <div class="slidecontainer">
                    <h3>{1}</h3>
                    <div id="{0}_slider"></div>
                </div>
                <br>
               """.format(self.id, self.name)
        return textwrap.dedent(text)

    def getJS(self):
        text = """
                // Handle slider {0} instantiation, config, and websocket events
                sliderObjects[\"{0}\"] = document.getElementById('{0}_slider');

                noUiSlider.create(sliderObjects[\"{0}\"], {{
                    start: [{3}],
                    tooltips: [true],
                    range: {{
                        'min': [{1}],
                        'max': [{2}]
                    }},
                    pips: {{
                        mode: 'count',
                        values: 6,
                        density: 4
                    }}
                }});

                sliderObjects[\"{0}\"].noUiSlider.on('slide', function(values, handle, unencoded){{
                    if(websocket.readyState == WebSocket.OPEN){{
                        websocket.send(JSON.stringify({{action: 'set', id: \"{0}\", value: unencoded}}));
                    }}
                
                }});

               """.format(self.id, self.minVal, self.maxVal, self.defaultVal)
        return textwrap.dedent(text)

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def getID(self):
        return self.id
       

    def setValue(self, value):
        if(self.value != value):
            self.value = value
            if(self.value > self.maxVal):
                self.value = self.maxVal
            elif(self.value < self.minVal):
                self.value = self.minVal

