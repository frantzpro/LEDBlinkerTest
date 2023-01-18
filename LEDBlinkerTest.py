import signal
import sys
from threading import Thread
from time import sleep

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer, formatPrint


class LEDBlinkerTest(AbstractVirtualCapability):
    blinkModes = {0: "Off",
                  1: "On",
                  2: "MediumBlink",
                  3: "SOS"}

    def __init__(self, server):
        super().__init__(server)
        self.uri = "LEDBlinkerTest"
        self.ledOn = False
        self.endMode = True
        self.blinkMode = 0

    '''def GetBlinkMode(self, params: dict) -> dict:
        return {"BlinkMode:": self.blinkMode}

    def SetBlinkMode(self, params: dict) -> dict:
        self.blinkMode = params["BlinkMode"]
        return {"BlinkMode:": self.blinkMode}'''

    def EndMode(self, param: dict) -> dict:
        self.endMode = True

    def StartMode(self, param: dict) -> dict:
        self.endMode = False

        # Just for testing the mediumBlink mode
        self.blinkMode = 2

    def RunMode(self, param: dict) -> dict:
        while not self.endMode:
            '''Implement the different modes'''
            if self.blinkModes[self.blinkMode] == "MediumBlink":
                self.MediumBlink(0.5)
            elif self.blinkModes[self.blinkMode] == "FastBlink":
                self.Blink(0.1)
            elif self.blinkModes[self.blinkMode] == "SlowBlink":
                self.Blink(1.5)
            elif self.blinkModes[self.blinkMode] == "On":
                self.invoke_sync("turnOnLED", {})
            elif self.blinkModes[self.blinkMode] == "Off":
                self.invoke_sync("turnOffLED", {})
            elif self.blinkModes[self.blinkMode] == "SOS":
                self.SOS()


    def SOS(self, waitingTime: float):
        self.invoke_sync("turnOffLED", {})
        sleep(0.5)
        for i in range(9):
            self.invoke_sync("turnOnLED", {})
            if 3 <= i <= 6:
                sleep(0.25)
            else:
                sleep(0.5)
            self.invoke_sync("turnOffLED", {})
            sleep(0.5)

    def Blink(self, waitingTime: float):
        sleep(waitingTime)
        self.invoke_sync("turnOnLED", {})
        sleep(waitingTime)
        self.invoke_sync("turnOffLED", {})

    def SetLED(self, param: dict) -> dict:
        self.ledOn = param["SimpleBooleanParameter"]
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
