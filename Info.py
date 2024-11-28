from demoparser2 import DemoParser

if __name__ == "__main__":
    print("Main started")
    
    #Testing my local dem file (This can be on git it's not sensitive data)
    demoFile = "./match730_003714199228369600597_0393609323_122.dem"
    
    #Set up the base parser info
    parser = DemoParser(demoFile)
    event_df = parser.parse_event("player_death", player=["X", "Y"], other=["total_rounds_played"])
    ticks_df = parser.parse_ticks(["X", "Y"])
    
    #List all events in the game
    events = parser.list_game_events()
    print(events)
    print()
    
    #Setup map information or single information that might be needed
    gameInfo = []
    headers = parser.parse_header()
    gameInfo.append(headers["map_name"])
    
    #Creates a dictionary of each player in the game
    players = parser.parse_event("player_team")
    playerInfo = {}
    for index, row in players.iterrows():
        userID = players.loc[index, "user_steamid"]
        playerInfo[userID] = {}
        playerInfo[userID]["name"] = players.loc[index, "user_name"]
        playerInfo[userID]["team"] = players.loc[index, "team"]
    
    #Add kills for each user (added to the end of the current list for a player)
    player_death_df = parser.parse_event("player_death")
    print(player_death_df.columns)
    print()
    print(player_death_df.head())
    for player in playerInfo.keys():
        #Basic kill stats
        playerInfo[player]["totalKills"] = len(player_death_df.loc[player_death_df["attacker_steamid"] == player])
        playerInfo[player]["assists"] = len(player_death_df.loc[player_death_df["assister_steamid"] == player])
        playerInfo[player]["totalDeaths"] = len(player_death_df.loc[player_death_df["user_steamid"] == player])
        #Specific types of kill stats
        playerInfo[player]["smokeKills"] = len(player_death_df.loc[(player_death_df["attacker_steamid"] == player) & (player_death_df["thrusmoke"] == True)])
        playerInfo[player]["headshotKills"] = len(player_death_df.loc[(player_death_df["attacker_steamid"] == player) & (player_death_df["headshot"] == True)])
        playerInfo[player]["noscopeKills"] = len(player_death_df.loc[(player_death_df["attacker_steamid"] == player) & (player_death_df["noscope"] == True)])
        playerInfo[player]["noscopeKills"] = len(player_death_df.loc[(player_death_df["attacker_steamid"] == player) & (player_death_df["noscope"] == True)])
        playerInfo[player]["blindKills"] = len(player_death_df.loc[(player_death_df["attacker_steamid"] == player) & (player_death_df["attackerblind"] == True)])
        #Average stats
        playerInfo[player]["avgKillDistance"] = "%0.2f" % (sum(player_death_df.loc[(player_death_df["attacker_steamid"] == player), ["distance"]]["distance"])/(playerInfo[player]["totalKills"]))
        #Can find out what weapon people killed with here: Field: "weapon"
    
    #Testing things
    temp_df = parser.parse_event("player_hurt")
    
    print(playerInfo)