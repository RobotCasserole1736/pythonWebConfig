from webConfig import WebConfig
import time

testCfg = WebConfig("Web Config Test")
slider1 = testCfg.addSlider("Test 1", 0, 10, 5)
slider2 = testCfg.addSlider("Test 2", -100, 100, 0)
slider3 = testCfg.addDoubleSlider("Test 3", 0, 1, 0, 0.2)
time.sleep(1.0)

print("Press ctrl-C to quit")

try:
    while True:
        val1 = slider1.getValue()
        val2 = slider2.getValue()
        val3 = slider3.getValue()
        print("1: {}, 2: {}, 3:{} ".format(val1,val2,val3), end="\r", flush=True)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

testCfg.shutdown()