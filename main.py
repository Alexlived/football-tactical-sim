import random
list_of_matchups = {'CB': 'ST',
                    'ST': 'CB',
                    'CDM': 'CAM',
                    'CAM': 'CDM',
                    'LB': 'RW',
                    'RW': 'LB',
                    'RB': 'LW',
                    'LW': 'RB',
                    'CM': 'CM',}
position_groups = {
    "attacking": ["RW", "LW", "ST", "CAM"],
    "defensive": ["CB", "CDM", "LB", "RB"],
    "Mid": ["CM","CDM","CAM"]
}
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
        self.stamina = min(100, self.stamina + amount)


class Team:
    def __init__(self,name,players,state,profile):
        self.name = name
        self.players = players
        self.state = state
        self.profile = profile

    def get_random_attacker_in_postion(self): # get a random attacker to start a duel
        players = [player for player in self.players if player.position in position_groups["attacking"]]
        return random.choice(players)
    
    def calc_modifier(self, stat_name):
        profiles = ["Attacking", "Defensive", "Balanced"]
        if self.profile == "Attacking":
            if stat_name in ["atk", "sht"]:
                atk_amount = 1.4
            elif stat_name in ["pas", "pac"]:
                mid_amount = 1.2
            if stat_name in ["dfn", "gk"]:
                def_amount = 0.6
        elif self.profile == "Defensive":
            if stat_name in ["dfn", "gk"]:
                def_amount = 1.4
            if stat_name in ["pas", "pac"]:
                mid_amount = 1.0
            if stat_name in ["atk", "sht"]:
                atk_amount = 0.8
        else: # Balanced
            if stat_name in ["pas", "pac"]:
                mid_amount = 1.2
            if stat_name in ["atk", "sht"]:
                atk_amount = 1.2
            if stat_name in ["dfn", "gk"]:
                def_amount = 1.0

        return atk_amount, mid_amount, def_amount

class Part_of_Pitch:   
    def __init__(self,zone,possesion,team_1,team_2):
        self.zone = zone
        self.possesion = possesion
        self.team_1 = team_1
        self.team_2 = team_2
    
    def update_possession(self, new_possession):
        self.possesion = new_possession

    def update_zone(self, duel_outcome):
        if duel_outcome in self.team_1.players:
            self.zone += 1
        else:
            self.zone -= 1
        if self.zone == 5:
            pass # Team 1 scores
        elif self.zone == -5:
            pass # Team 2 scores

    def get_required_position(self,):
        if self.zone >= 3:
            attacker = self.team_1.get_random_attacker_in_postion()
            return list_of_matchups[attacker.position]
        elif self.zone <= -3:
            attacker = self.team_2.get_random_attacker_in_postion()
            return list_of_matchups[attacker.position]
        else:
            return random.choice(position_groups["Mid"])

def simulate_duel(attacker, defender, team_attacking, team_defending):
    
            

