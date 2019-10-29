from threading import Timer
import GUICtl as gctl
#from make_call import make_call

class BlinkReminder():
    timerSettings = []
    timers = []

    blinkedRecently = False

    def __init__(self, blinkSource):
        self.timerSettings.extend([(5, self.sendCalmMsg), (10, self.sendAngryMsg)])
        for ts in self.timerSettings:
            self.timers.append(Timer(*ts))
        blinkSource.subscribe(blinkSource, self.handleBlink)

    def handleBlink(self):
        if self.blinkedRecently:
            print("Double blink")
            gctl.minimize()
            # Do double blink
        else:
            self.unsetRecentBlink()
            self.doubleBlinkTimer = Timer(0.7, self.unsetRecentBlink)
            self.doubleBlinkTimer.start()
            self.blinkedRecently = True

        for t in self.timers:
            t.cancel()
        self.timers = []
        for ts in self.timerSettings:
            self.timers.append(Timer(*ts))
        for t in self.timers:
            t.start()

    def unsetRecentBlink(self):
        # Here be concurrency issues, but ostrich them for now
        self.blinkedRecently = False

    def sendCalmMsg(self):
        print("You should really blink")
        #make_call(0)

    def sendAngryMsg(self):
        print("BLINK ALREADY!")
        #make_call(1)

