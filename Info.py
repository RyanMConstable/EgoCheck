from demoparser2 import DemoParser

if __name__ == "__main__":
    print("Main started")
    
    #Testing my local dem file (This can be on git it's not sensitive data)
    demoFile = "./match730_003714199228369600597_0393609323_122.dem"
    
    #Set up the base parser info
    parser = DemoParser(demoFile)
    event_df = parser.parse_event("player_death", player=["X", "Y"], other=["total_rounds_played"])
    print(parser.parse_skins())
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
    fired_df = parser.parse_event("weapon_fire")
    footstep_df = parser.parse_event("player_footstep")
    rank_df = parser.parse_event("rank_update")
    bomb_df = parser.parse_event("bomb_dropped")
    bomb_planted_df = parser.parse_event("bomb_planted")
    reload_df = parser.parse_event("weapon_reload")
    item_pickup_df = parser.parse_event("item_pickup")
    bomb_pickup_df = parser.parse_event("bomb_pickup")
    jump_df = parser.parse_event("player_jump")
    defused_df = parser.parse_event("bomb_defused")
    chat_df = parser.parse_event("chat_message")
    for player in playerInfo.keys():
        """Player_death_df"""
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
        playerInfo[player]["bulletsFired"] = len(fired_df.loc[fired_df["user_steamid"] == player])
        #Foodsteps
        playerInfo[player]["totalFootsteps"] = len(footstep_df.loc[footstep_df["user_steamid"] == player])
        #Ranks
        playerInfo[player]["newRank"] = rank_df.loc[rank_df["user_steamid"] == player, ["rank_new"]].values[0][0]
        playerInfo[player]["oldRank"] = rank_df.loc[rank_df["user_steamid"] == player, ["rank_old"]].values[0][0]
        #Bomb dropped
        playerInfo[player]["bombDropped"] = len(bomb_df.loc[bomb_df["user_steamid"] == player])
        #Bomb planted
        playerInfo[player]["bombPlanted"] = len(bomb_planted_df.loc[bomb_planted_df["user_steamid"] == player])
        #Reloads
        playerInfo[player]["gunReloads"] = len(reload_df.loc[reload_df["user_steamid"] == player])
        #Item pickups
        playerInfo[player]["itemPickups"] = len(item_pickup_df.loc[item_pickup_df["user_steamid"] == player])
        #bomb pickups
        playerInfo[player]["bombPickups"] = len(bomb_pickup_df.loc[bomb_pickup_df["user_steamid"] == player])
        #Bomb defused
        playerInfo[player]["bombDefused"] = len(defused_df.loc[defused_df["user_steamid"] == player])
        #Jumps
        playerInfo[player]["jumps"] = len(jump_df.loc[jump_df["user_steamid"] == player])
        #Chat messages
        playerInfo[player]["messages"] = []
        for iter, row in chat_df.loc[chat_df["user_steamid"] == player].iterrows():
            playerInfo[player]["messages"].append(row["chat_message"])
        
        
    #Testing things
    temp_df = parser.parse_event("chat_message")
    print(f"{temp_df.columns} \n")
    print(temp_df.head)
    
    print(playerInfo)