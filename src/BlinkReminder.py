class BlinkReminder():
    timerSettings = []
#    timerSettings = [(20, self.sendCalmMsg), (40, self.sendAngryMsg)]
    timers = []
    
    def __init__(self, blinkSource):
        self.timerSettings.extend([(20, self.sendCalmMsg), (40, self.sendAngryMsg)])
        for ts in self.timerSettings:
            self.timers.append(Timer(*ts))
        blinkSource.subscribe(self.handleBlink)

    def handleBlink(self):
        for t in Timers:
            t.cancel()
        timers = []
        for ts in timerSettings:
            timers.append(Timer(*ts))
        for t in Timers:
            t.start()

    def sendCalmMsg(self):
        print("Calm.")
         
    def sendAngryMsg(self):
        print("ANGRY")

