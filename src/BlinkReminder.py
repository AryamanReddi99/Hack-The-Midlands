from threading import Timer

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
        print("Calm.")
         
    def sendAngryMsg(self):
        print("ANGRY")

