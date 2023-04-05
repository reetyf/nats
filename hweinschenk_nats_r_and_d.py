import pandas as pd
import numpy as np
import datetime

def create_date(split):
    return datetime.date(int(split[0]),int(split[1]),int(split[2]))

def pitcher_summary(player_lookup, game_lookup, pitches, start_date= '2023-03-30', end_date = '2023-09-07'):
    return_df = pd.DataFrame([])
    
    main = pd.merge(game_lookup, pitches, on='game_id', how='inner')
    main = pd.merge( main,  player_lookup, left_on='pitcher_id', right_on ='player_id', how='inner')
    
    date_start = create_date(start_date.split('-'))
    date_end = create_date(end_date.split('-'))

    main['game_date'] = pd.to_datetime(main['game_date'],format='%Y-%m-%d').dt.date
    date_window = main.loc[main['game_date'].between(date_start,date_end,inclusive='both')]

    grouped = date_window.groupby('pitcher_id')
    num_pitches = grouped.count().iloc[:,0]
    ids = num_pitches.index
    name = grouped.max()['name']
    avg_velo =grouped.mean()['velo']
    
    game_count = {}
    for an_id in ids:
        num_games = len(list(date_window.groupby(['pitcher_id','game_id']).count().loc[an_id].index))
        game_count[an_id] = num_games
    temp = {'name':name,'game_count':pd.Series(game_count),'num_pitches':num_pitches,'avg_velo':avg_velo}
    return_df = pd.DataFrame(temp)
    return return_df


def pitcher_matrix(pitcher_summary,game_lookup,player_lookup, pitches,team_id,end_date):
    
    # set up row and col labels (useful for entry later)
    team_id = team_id
    end_date = create_date(end_date.split('-'))
    six_days_earlier = end_date - pd.Timedelta(days=6)
    date_range = pd.date_range(six_days_earlier,end_date).date
    team_pitcher_ids = pitcher_summary.loc[30*(team_id - 1):30*(team_id - 1)+14,:]['name']

    # rows are all pitchers, cols are dates
    return_df = pd.DataFrame(index =team_pitcher_ids, columns=date_range)

    # merge on ids to get info
    main = pd.merge(game_lookup, pitches, on='game_id', how='inner')
    main = pd.merge( main,  player_lookup, left_on='pitcher_id', right_on ='player_id', how='inner',)
    main['game_date'] = pd.to_datetime(main['game_date'],format='%Y-%m-%d').dt.date

    main.drop(['Unnamed: 0_x','Unnamed: 0_y','Unnamed: 0'],axis = 1,inplace=True)

    # filter to date window
    date_window = main.loc[main['game_date'].between(six_days_earlier,end_date,inclusive='both')]

    # all away games played for team, with relevant inning bottoms aka, away team pitching
    away_games_played = date_window.loc[(date_window['away_team_id'] == team_id)]
    inning_bottoms = away_games_played.loc[away_games_played['top_inning'] == 0]
    
    # group by the date and name (result : 3/31/2023 Pitcher 1 | 12 pitches
    #                                                Pitcher 2 | 30 pitches
    #                                                etc. )
    per_game_data = inning_bottoms.groupby(['game_date','name']).count()

    # game date, name, pitches with index reset
    relevant_data = per_game_data.iloc[:,0:1].reset_index()

    # read into dateframe 
    for name in return_df.index:
        temp = relevant_data.loc[relevant_data['name'] == name]
        for one_game in temp.index:
             return_df.loc[temp.loc[one_game,'name'],temp.loc[one_game,'game_date']] = temp.loc[one_game,'game_id']

    # repeat for home team (top inning pitcher pitches)
    home_games_played = date_window.loc[(date_window['home_team_id'] == team_id)]
    inning_tops = home_games_played.loc[home_games_played['top_inning'] == 1]
    per_game_data = inning_tops.groupby(['game_date','name']).count()
    relevant_data = per_game_data.iloc[:,0:1].reset_index()
    for name in return_df.index:
        temp = relevant_data.loc[relevant_data['name'] == name]
        for one_game in temp.index:
             return_df.loc[temp.loc[one_game,'name'],temp.loc[one_game,'game_date']] = temp.loc[one_game,'game_id']          
   
    # fill in NaN with 0
    return_df = return_df.fillna(0)  
    
    # create sum columns
    return_df['Last 3 Days'] =return_df.iloc[:,[-1,-2,-3]].sum(axis = 1)
    return_df['Last 7 Days'] = return_df.sum(axis = 1)
    
    
    
    # add a flag for availability
    back_to_back = ((return_df.iloc[:,-3]!= 0) & (return_df.iloc[:,-4]!= 0)) 
    # only case need to account for (due to above already flagging) is pitch, pitch, rest, pitch and p,p,p,r
    three_of_four = ((return_df.iloc[:,-3] != 0) & (return_df.iloc[:,-4] == 0) & (return_df.iloc[:,-5] != 0) & (return_df.iloc[:,-6] != 0)) |         ((return_df.iloc[:,-3] == 0) & (return_df.iloc[:,-4] != 0) & (return_df.iloc[:,-5] != 0) & (return_df.iloc[:,-6] != 0))
    return_df['unavailable'] = np.where(back_to_back |three_of_four ,1,0)

    return return_df


