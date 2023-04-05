#!/bin/bash

dates=("2023-04-30" "2023-05-30" "2023-06-30" "2023-07-30" "2023-08-30")

for team in $(seq 1 5 30)
do
    for date in ${dates[@]}
    do
    echo "Creating Pitching Matrix for Team $team for the week preceding $date"
    python driver.py $team $date
    done
done