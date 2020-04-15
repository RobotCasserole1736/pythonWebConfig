from webConfig import WebConfig
import time

testCfg = WebConfig("Web Config Test")
testCfg.addSlider("Test 1", 0, 10, 5)
testCfg.addSlider("Test 2", -100, 100, 0)
testCfg.addSlider("Test 3", 0, 1, 0)
time.sleep(1.0)
input("Press enter to shutdown")
testCfg.shutdown()