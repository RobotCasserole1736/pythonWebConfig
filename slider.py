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
                    <h3>{}</h3>
                    <input type="range" min="{}" max="{}" value="{}" class="slider" id="{}">
                    <div id="{}_readout"> ?? </div>
                </div>
                <br>
               """.format(self.name, self.minVal, self.maxVal, self.defaultVal, self.id, self.id)

    def getJS(self):
        return """
                var slider_{} = document.getElementById("{}");
                var output_{} = document.getElementById("{}_readout");
                output_{}.innerHTML = slider_{}.value; // Display the default slider value

                // Update the current slider value (each time you drag the slider handle)
                slider_{}.oninput = function() {{
                    output_{}.innerHTML = this.value;
                }}
               """.format(self.id, self.id, self.id, self.id, self.id, self.id, self.id, self.id)

    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def setValue(self, value):
        self.value = value
        if(self.value > self.maxVal):
            self.value = self.maxVal
        elif(self.value < self.minVal):
            self.value = self.minVal

