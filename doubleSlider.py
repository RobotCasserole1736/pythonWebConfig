from abstractWebObjects import webUserInput
import textwrap

class DoubleSlider(webUserInput):
    
    def __init__(self, name, minVal, maxVal, defaultVal1, defaultVal2):
        self.name = name
        self.minVal = minVal
        self.maxVal = maxVal
        self.defaultVal1 = defaultVal1
        self.defaultVal2 = defaultVal2
        
        self.value1 = self.defaultVal1
        self.value2 = self.defaultVal2
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
                //////////////////////////////////////////////////////////////////////////////////////////
                // Handle slider {0} instantiation, config, and websocket events
                sliderObjects[\"{0}\"] = document.getElementById('{0}_slider');

                noUiSlider.create(sliderObjects[\"{0}\"], {{
                    start: [{3},{4}],
                    tooltips: [false, false],
                    connect: true,
                    behaviour: 'drag-tap',
                    animate: true,
                    animationDuration: 100,
                    range: {{
                        'min': [{1},{1}],
                        'max': [{2},{2}]
                    }},
                    pips: {{
                        mode: 'count',
                        values: 6,
                        density: 4
                    }}
                }});


                sliderObjects[\"{0}\"].noUiSlider.on('slide', function(values, handle, unencoded){{
                    if(websocket.readyState == WebSocket.OPEN){{
                        websocket.send(JSON.stringify({{action: 'set', id: \"{0}\", value: [JSON.parse(values[0]), JSON.parse(values[1])]}}));
                    }}
                }});

                updateInhibitFlags[\"{0}\"] = false;

                sliderObjects[\"{0}\"].noUiSlider.on('start', function(values, handle, unencoded){{
                    updateInhibitFlags[\"{0}\"] = true;
                }});
                sliderObjects[\"{0}\"].noUiSlider.on('end', function(values, handle, unencoded){{
                    updateInhibitFlags[\"{0}\"] = false;
                }});

                // End slider {0}
                //////////////////////////////////////////////////////////////////////////////////////////


               """.format(self.id, self.minVal, self.maxVal, self.defaultVal1, self.defaultVal2)
        return textwrap.dedent(text)

    def getValue(self):
        return [self.value1, self.value2]

    def getName(self):
        return self.name

    def getID(self):
        return self.id
       

    def setValue(self, value):
        value1 = value[0]
        value2 = value[1]
        if(self.value1 != value1):
            self.value1 = value1
            if(self.value1 > self.maxVal):
                self.value1 = self.maxVal
            elif(self.value1 < self.minVal):
                self.value1 = self.minVal

        if(self.value2 != value2):
            self.value2 = value2
            if(self.value2 > self.maxVal):
                self.value2 = self.maxVal
            elif(self.value2 < self.minVal):
                self.value2 = self.minVal

