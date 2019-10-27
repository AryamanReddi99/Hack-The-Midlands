from threading import Timer
from make_call import make_call

class BlinkReminder():
    timerSettings = []
    timers = []

    def __init__(self, blinkSource):
        self.timerSettings.extend([(5, self.sendCalmMsg), (10, self.sendAngryMsg)])
        for ts in self.timerSettings:
            self.timers.append(Timer(*ts))
        blinkSource.subscribe(blinkSource, self.handleBlink)

    def handleBlink(self):
        for t in self.timers:
            t.cancel()
        self.timers = []
        for ts in self.timerSettings:
            self.timers.append(Timer(*ts))
        for t in self.timers:
            t.start()

    def sendCalmMsg(self):
        make_call(0)

    def sendAngryMsg(self):
        make_call(1)
