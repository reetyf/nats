from hweinschenk_nats_r_and_d import pitcher_summary,pitcher_matrix
import pandas as pd
import sys
import re

player_lookup = pd.read_csv('player_lookup.csv')
game_lookup =pd.read_csv('game_lookup.csv')
pitches= pd.read_csv('pitches.csv')

summary = pitcher_summary(player_lookup,game_lookup,pitches)

assert int(sys.argv[1]) in range(1,31)
assert re.match(r'\d{4}-\d{2}-\d{2}',sys.argv[2])

matrix = pitcher_matrix(summary,game_lookup,player_lookup,pitches,int(sys.argv[1]),sys.argv[2])
matrix.to_csv(f'pitcher_matrix_team{sys.argv[1]}_{sys.argv[2]}.csv')