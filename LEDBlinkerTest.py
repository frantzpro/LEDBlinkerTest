import signal
import sys
from threading import Thread
from time import sleep

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer, formatPrint


class LEDBlinkerTest(AbstractVirtualCapability):

    '''blinkModes = {0: "Off",
                 1: "On",
                 2: "MediumBlink",
                 3: "SOS"}'''

    def __init__(self, server):
        super().__init__(server)
        self.uri = "LEDBlinkerTest"
        self.ledOn = False
        #self.blinkMode = 0

    '''def GetBlinkMode(self, params: dict) -> dict:
        return {"BlinkMode:": self.blinkMode}

    def SetBlinkMode(self, params: dict) -> dict:
        self.blinkMode = params["BlinkMode"]
        return {"BlinkMode:": self.blinkMode}'''

    def SetLED(self, param: dict) -> dict:
        self.ledOn = param["ledOn"]
        if self.ledOn:
            self.invoke_sync("turnOnLED", {})
        else:
            self.invoke_sync("turnOffLED", {})

    def loop(self):
        pass


if __name__ == "__main__":
    try:
        port = None
        if len(sys.argv[1:]) > 0:
            port = int(sys.argv[1])
        server = VirtualCapabilityServer(port)
        tf = LEDBlinkerTest(server)
        tf.start()
        while server.running:
            pass
        # Needed for properly closing, when program is being stopped wit a Keyboard Interrupt
    except KeyboardInterrupt:
        print("[Main] Received KeyboardInterrupt")
    except Exception as e:
        print(f"[ERROR] {repr(e)}")
