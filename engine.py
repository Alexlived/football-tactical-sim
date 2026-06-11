import random

position_groups = {
    "attacking": ["RW", "LW", "ST", "CAM"],
    "defensive": ["CB", "CDM", "LB", "RB"],
    "Mid": ["CM","CDM","CAM"]
}
class Player:
    def __init__(self,n,p,pac,dfn,atk,pas,sht,gk,phy):
        self.name = n
        self.position = p

        # Base stats
        self.pac = pac
        self.dfn = dfn
        self.atk = atk
        self.pas = pas
        self.sht = sht
        self.phy = phy
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

    def decay(self):
        for player in self.players:
            player.decay(random.randint(3, 10)) # Decay each player's stamina by a random amount of points per duel
    

       
        

class Part_of_Pitch:   
    def __init__(self,zone,team_1,team_2):
        self.zone = zone
        self.team_1 = team_1
        self.team_2 = team_2

    def update_zone(self, duel_outcome):
        if duel_outcome in self.team_1.players:
            self.zone += 1
            pass
        else:
            self.zone -= 1
            pass
\


def get_players_by_zone(team_1, team_2, zone):
    # For central zones, we want to select midfielders from both teams
    if 0 <= zone <= 2:
        relevant_team_1_players = [player for player in team_1.players if player.position in position_groups["Mid"]]
        relevant_team_2_players = [player for player in team_2.players if player.position in position_groups["Mid"]]
    elif -2 <= zone <= 0:
        relevant_team_1_players = [player for player in team_1.players if player.position in position_groups["Mid"]]
        relevant_team_2_players = [player for player in team_2.players if player.position in position_groups["Mid"]]

    # For attacking zones, we want to select attackers from the attacking team and defenders from the defending team
    elif zone >= 3:
        relevant_team_1_players = [player for player in team_1.players if player.position in position_groups["attacking"]]
        relevant_team_2_players = [player for player in team_2.players if player.position in position_groups["defensive"]]
    else: # zone <= -3
        relevant_team_1_players = [player for player in team_1.players if player.position in position_groups["defensive"]]
        relevant_team_2_players = [player for player in team_2.players if player.position in position_groups["attacking"]]
    return relevant_team_1_players, relevant_team_2_players

def get_random_duelists(team_1, team_2, zone):
    relevant_team_1_players, relevant_team_2_players = get_players_by_zone(team_1, team_2, zone) # Using the function
    attacker = random.choice(relevant_team_1_players)
    defender = random.choice(relevant_team_2_players)
    return attacker, defender

def team_profile_modifier(player, profile):
    atk_stats = ["atk","pac","phy", "sht"]
    mid_stats = ["pas", "pac"]
    dfn_stats = ["dfn", "pac","phy"]


    if profile == "Attacking":
        for stat in atk_stats:
            setattr(player, stat, getattr(player, stat)*1.4)
        for stat in mid_stats:
            setattr(player, stat, getattr(player, stat)*1.2)
        for stat in dfn_stats:
            setattr(player, stat, getattr(player, stat)*0.6)
    elif profile == "Defensive":
        for stat in atk_stats:
            setattr(player, stat, getattr(player, stat)*0.6)
        for stat in mid_stats:
            setattr(player, stat, getattr(player, stat)*1.2)
        for stat in dfn_stats:
            setattr(player, stat, getattr(player, stat)*1.4)
    else: # Balanced
        for stat in atk_stats:
            setattr(player, stat, getattr(player, stat)*1.2)
        for stat in mid_stats:
            setattr(player, stat, getattr(player, stat)*1.2)
        for stat in dfn_stats:
            setattr(player, stat, getattr(player, stat)*1.2)

    

        
        

def simulate_duel(attacker, defender, team_attacking, team_defending,zone):
    if 0 <= zone <= 2:
        attacker_stat = attacker.get_effective_stat("pas") + attacker.get_effective_stat("atk") # Midfield duels rely on passing and intelligence
        defender_stat = defender.get_effective_stat("pas") + defender.get_effective_stat("dfn") 
    elif -2 <= zone <= 0:
        attacker_stat = attacker.get_effective_stat("pas") + attacker.get_effective_stat("dfn") 
        defender_stat = defender.get_effective_stat("pas") + defender.get_effective_stat("atk")

    
    elif zone >= 3:
        attacker_stat = attacker.get_effective_stat("atk") + attacker.get_effective_stat("pac") + attacker.get_effective_stat("phy") 
        defender_stat = defender.get_effective_stat("dfn") + defender.get_effective_stat("pac") + defender.get_effective_stat("phy") 
    elif zone <= -3:
        attacker_stat = attacker.get_effective_stat("dfn") + attacker.get_effective_stat("pac") + attacker.get_effective_stat("phy") 
        defender_stat = defender.get_effective_stat("atk") + defender.get_effective_stat("pac") + defender.get_effective_stat("phy")

    winners = [attacker, defender]
    weights = [attacker_stat, defender_stat]
    random_winner = random.choices(winners, weights=weights, k=1)[0]
    return random_winner

def simulate_shot(attacker, goalkeeper):
    shot_stat = attacker.get_effective_stat("sht")
    gk_stat = goalkeeper.get_effective_stat("gk")
    winners = [attacker, goalkeeper]
    weights = [shot_stat, gk_stat]
    random_winner = random.choices(winners, weights=weights, k=1)[0]
    if random_winner == attacker:
        return 'Goal'
    else:
        return 'Saved'

def main():
    