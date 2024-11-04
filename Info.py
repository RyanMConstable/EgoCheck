from demoparser2 import DemoParser

if __name__ == "__main__":
    print("Main started")
    
    #Testing my local dem file (This can be on git it's not sensitive data)
    demoFile = "./match730_003716174692134945057_0469028642_129.dem"
    
    #Set up the base parser info
    parser = DemoParser(demoFile)
    event_df = parser.parse_event("player_death", player=["X", "Y"], other=["total_rounds_played"])
    ticks_df = parser.parse_ticks(["X", "Y"])
    
    #List all events in the game
    events = parser.list_game_events()
    
    #List of lists
    #The main list contains lists of the format [steam username, steamid, team number]
    players = parser.parse_event("player_team")
    list_players = players[["user_name", "user_steamid", "team"]].values.tolist()