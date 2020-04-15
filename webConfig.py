import asyncio
import http.server
import socketserver
import mimetypes
import threading
import websockets
import json
import logging
import os

from slider import Slider

HTTP_PORT = 2006
WS_PORT = 6789

WEB_ROOT = "./www"
HTML_TEMPLATE_FILE = os.path.join(WEB_ROOT, "index_template.html")
JS_TEMPLATE_FILE   = os.path.join(WEB_ROOT, "main_template.js")
ERR_404_FILE       = os.path.join(WEB_ROOT, "404.html")

logging.basicConfig()

webObjectDict = {}
title = "Default"


class CustomHTTPHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self, response_num, filename):
        contentInfo = mimetypes.guess_type(filename)
        if(contentInfo is not None):
            contentType = contentInfo[0]
        else:
            contentType = "text/html" #meh

        self.send_response(response_num)
        self.send_header("Content-type", contentType)
        self.end_headers()

        
    def do_GET(self):
        """Respond to a GET request."""
        sendText = ""

        if("/index.html" == self.path or "/" == self.path):
            self.do_HEAD(200, HTML_TEMPLATE_FILE)
            userHTML = ""
            for obj in webObjectDict.values():
                userHTML += obj.getHTML() + "\n\n"
            with open(HTML_TEMPLATE_FILE, "r") as f:
                for line in f:
                    sendText += line.replace(r"{{user_content}}", userHTML).replace(r"{{title}}", title)
                sendBytes = sendText.encode("utf-8")


        elif("/main.js" == self.path):
            self.do_HEAD(200, JS_TEMPLATE_FILE)
            userJS = ""
            for obj in webObjectDict.values():
                userJS += obj.getJS() + "\n\n"
            with open(JS_TEMPLATE_FILE, "r") as f:
                for line in f:
                    sendText += line.replace(r"{{user_content}}", userJS).replace(r"{{ws_port}}", str(WS_PORT))
                sendBytes = sendText.encode("utf-8")
        else:
            # Handle generic file request, or return 404 if not found.
            reqFile = os.path.join(WEB_ROOT, self.path.strip("/\\"))
            if os.path.isfile(reqFile):
                self.do_HEAD(200, reqFile)
            else:
                reqFile = ERR_404_FILE
                self.do_HEAD(404, reqFile)
            
            with open(reqFile, "rb") as f:
                sendBytes = f.read()

        self.wfile.write(sendBytes)


class WebConfig:

    def __init__(self, title_in):
        global title

        print("Starting up {}...".format(title_in))
        title = title_in

        self.connectedUsers = set()

        self.httpHandler = CustomHTTPHandler
        self.httpHandler

        self.wsThreadRun = True
        self.wsThread = threading.Thread(target=self.wsEntryFunc)
        self.wsThread.start()

        self.httpServer = None
        self.httpThread = threading.Thread(target=self.httpEntryFunc)
        self.httpThread.start()
        print("Startup complete!")

    async def register(self, websocket):
        self.connectedUsers.add(websocket)

    async def unregister(self, websocket):
        self.connectedUsers.remove(websocket)

    async def counter(self, websocket, path):
        global webObjectDict
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "set":
                    print("Message: {}".format(str(data)))
                    webObjectDict[data["id"]].setValue(data["value"][0])
                else:
                    logging.error("unsupported event: {}".format(data))
        finally:
            await self.unregister(websocket)


    def val_update_event(self):
        txData = {}
        for obj in webObjectDict.values():
            txData[obj.getID()] = obj.getValue()
        return json.dumps(txData)


    async def periodicDataTransmit(self):
        while self.wsThreadRun:
            if self.connectedUsers:  # asyncio.wait doesn't accept an empty list
                message = self.val_update_event()
                await asyncio.wait([user.send(message) for user in self.connectedUsers])
            await asyncio.sleep(0.25)


    def wsEntryFunc(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.counter, "127.0.0.1", WS_PORT)
        loop.run_until_complete(start_server)

        task = loop.create_task(self.periodicDataTransmit())
        try:
            loop.run_until_complete(task)
        except asyncio.CancelledError:
            pass



    def httpEntryFunc(self):
            self.httpServer = socketserver.TCPServer(("", HTTP_PORT), self.httpHandler)
            print("serving at port", HTTP_PORT)
            self.httpServer.serve_forever()

    def shutdown(self):
        print("Shutting Down...")
        self.wsThreadRun = False
        asyncio.get_event_loop().stop()
        asyncio.get_event_loop().close()
        self.wsThread.join()

        self.httpServer.shutdown()
        self.httpThread.join()
        print("done!")


    def addSlider(self, name, minVal, maxVal, defaultVal):
        global webObjectDict
        newSliderObj = Slider(name, minVal, maxVal, defaultVal)
        webObjectDict[newSliderObj.id] = newSliderObj

