class Rate_Limiter:
    def __init__(self, maxRequest=3, window_seconds=2):
        self.maxRequest=maxRequest
        self.window_seconds=window_seconds
        self.history={}

    def is_allowed(self, ipAdrress) -> bool:
        import time
        currentTime= time.time()
        batasWaktu= currentTime - self.window_seconds
        if ipAdrress not in self.history:
            self.history[ipAdrress] = []            
        self.history[ipAdrress]= [x for x in self.history[ipAdrress] if x > batasWaktu]
        if len(self.history[ipAdrress]) >= self.maxRequest:
            return False
        else:
            self.history[ipAdrress].append(currentTime)
            return True