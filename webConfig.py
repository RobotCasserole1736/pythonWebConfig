import asyncio
import http.server
import socketserver
import threading
import websockets
import json
import logging

from slider import Slider

HTTP_PORT = 2006
WS_PORT = 6789

HTML_TEMPLATE_FILE = "./www/index_template.html"
CSS_TEMPLATE_FILE  = "./www/main.css"
JS_TEMPLATE_FILE   = "./www/main_template.js"

logging.basicConfig()

webObjectDict = {}


class CustomHTTPHandler(http.server.BaseHTTPRequestHandler):
    def do_HEAD(self, response_num=200):
        self.send_response(response_num)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    def do_GET(self):
        """Respond to a GET request."""
        sendText = ""

        if("index.html" in self.path or self.path == "/"):
            self.do_HEAD()
            userHTML = ""
            for obj in webObjectDict.values():
                userHTML += obj.getHTML() + "\n\n"
            with open(HTML_TEMPLATE_FILE, "r") as f:
                for line in f:
                    sendText += line.replace(r"{{user_content}}", userHTML)

        elif("main.js" in self.path):
            self.do_HEAD()
            userJS = ""
            for obj in webObjectDict.values():
                userJS += obj.getJS() + "\n\n"
            with open(JS_TEMPLATE_FILE, "r") as f:
                for line in f:
                    sendText += line.replace(r"{{user_content}}", userJS)

        elif("main.css" in self.path):
            self.do_HEAD()
            with open(CSS_TEMPLATE_FILE, "r") as f:
                for line in f:
                    sendText += line

        else:
            self.do_HEAD(404)
            sendText += "<html><head><title>Page not found</title></head>"
            sendText += "<body><p>404 Error - Page not found</p></body></html>"

        self.wfile.write(sendText.encode("utf-8"))


class WebConfig:

    def __init__(self):
        print("Starting up...")

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


    def users_event(self):
        return json.dumps({"type": "users", "count": len(self.connectedUsers)})

    def val_update_event(self):
        txData = {}
        for obj in webObjectDict:
            txData[obj.getName()] = obj.getValue()
        return txData


    async def notify_users(self):
        if self.connectedUsers:  # asyncio.wait doesn't accept an empty list
            message = self.users_event()
            await asyncio.wait([user.send(message) for user in self.connectedUsers])


    async def register(self, websocket):
        self.connectedUsers.add(websocket)
        await self.notify_users()


    async def unregister(self, websocket):
        self.connectedUsers.remove(websocket)
        await self.notify_users()


    async def counter(self, websocket, path):
        global webObjectDict
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                if data["action"] == "set":
                    webObjectDict[data["name"]].setValue(data["val"])
                else:
                    logging.error("unsupported event: {}".format(data))
        finally:
            await self.unregister(websocket)


    async def periodicDataTransmit(self):
        while self.wsThreadRun:
            if self.connectedUsers:  # asyncio.wait doesn't accept an empty list
                message = self.val_update_event()
                await asyncio.wait([user.send(message) for user in self.connectedUsers])
            await asyncio.sleep(0.25)


    def wsEntryFunc(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.counter, "localhost", WS_PORT)
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
        webObjectDict[name] = Slider(name, minVal, maxVal, defaultVal)

