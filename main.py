class Player:
    def __init__(self,n,p,pac,dfn,atk,pas,sht,gk):
        self.name = n
        self.position = p

        # Base stats
        self.pac = pac
        self.dfn = dfn
        self.atk = atk
        self.pas = pas
        self.sht = sht
        self.gk = gk
        pass

        self.stamina = 100

    def get_effective_stat(self, stat_name):
        # Calculates stat penalty based on current stamina.
        base_stat = getattr(self, stat_name, 50)
        stamina_factor = max(0.2, self.stamina / 100.0) # Floor at 20% performance
        return int(base_stat * stamina_factor)

    def decay(self,amount): # decay stamina
        self.stamina = max(10, self.stamina - amount)
    
    def recover(self,amount): #recover in breaks
        self.stamina = min(10, self.stamina + amount)


