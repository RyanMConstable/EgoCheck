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
    
    #List of lists
    #The main list contains lists of the format [steam username, steamid, team number]
    players = parser.parse_event("player_team")
    playerInfo = {}
    for row in players.iterrows:
        row["username"]
    list_players = players[["user_name", "user_steamid", "team"]].values.tolist()
    print(f"list_players = {list_players} \n")
    
    #Add kills for each user (added to the end of the current list for a player)
    player_death_df = parser.parse_event("player_death")
    print(player_death_df.columns)
    print()
    print(player_death_df.head(10))
    print()
    for player in list_players:
        player.append(len(player_death_df.loc[player_death_df["attacker_steamid"] == player[1]]))

    print(list_players)
    print()
    
    #Testing things
    temp_df = parser.parse_event("player_hurt")
    print(temp_df)
    print()
    print(temp_df.columns)
    print()