import time
from engine import Player, Team, Part_of_Pitch, team_profile_modifier, get_random_duelists, simulate_duel, simulate_shot

def main():
    # Real Madrid Player Array
    rm_players = [
        Player("Courtois", "gk", 45, 15, 10, 75, 10, 78, 90),
        Player("Carvajal", "RB", 80, 85, 78, 78, 54, 81, 10),
        Player("Rüdiger", "CB", 82, 87, 55, 71, 53, 86, 10),
        Player("Militao", "CB", 85, 85, 58, 70, 50, 82, 10),
        Player("Mendy", "LB", 89, 80, 75, 74, 62, 84, 10),
        Player("Tchouameni", "CDM", 72, 83, 74, 79, 69, 84, 10),
        Player("Valverde", "CM", 88, 80, 84, 85, 82, 85, 10),
        Player("Bellingham", "CAM", 80, 78, 87, 85, 85, 83, 10),
        Player("Rodrygo", "RW", 88, 42, 86, 80, 82, 70, 10),
        Player("Mbappe", "ST", 97, 36, 93, 80, 90, 78, 10),
        Player("Vinicius", "LW", 95, 30, 91, 81, 84, 68, 10)
    ]

    # Barcelona Player Array
    barca_players = [
        Player("Ter Stegen", "gk", 40, 10, 12, 85, 10, 76, 89),
        Player("Kounde", "RB", 80, 85, 70, 75, 45, 78, 10),
        Player("Araujo", "CB", 83, 86, 50, 65, 48, 85, 10),
        Player("Cubarsi", "CB", 72, 81, 62, 80, 38, 73, 10),
        Player("Balde", "LB", 91, 75, 78, 73, 48, 70, 10),
        Player("Casado", "CDM", 75, 78, 72, 81, 60, 76, 10),
        Player("De Jong", "CM", 82, 77, 83, 86, 69, 78, 10),
        Player("Pedri", "CAM", 78, 68, 86, 87, 70, 70, 10),
        Player("Yamal", "RW", 85, 35, 84, 81, 78, 65, 10),
        Player("Lewandowski", "ST", 75, 44, 88, 70, 88, 80, 10),
        Player("Raphinha", "LW", 89, 50, 85, 82, 80, 73, 10)
    ]

    # 3. Team objects
    real_madrid = Team(name="Real Madrid", players=rm_players, state="defending", profile="Balanced")
    barcelona = Team(name="Barcelona", players=barca_players, state="attacking", profile="Attacking")

    # 4. Apply One-Time Pre-Match Tactical Profile Multipliers
    for player in real_madrid.players:
        team_profile_modifier(player, real_madrid.profile)
        
    for player in barcelona.players:
        team_profile_modifier(player, barcelona.profile)

    # 5. Connect Teams to the Global Pitch Simulation Manager
    pitch = Part_of_Pitch(zone=0, possesion=real_madrid, team_1=real_madrid, team_2=barcelona)

    # Score Trackers
    score = {real_madrid.name: 0, barcelona.name: 0}