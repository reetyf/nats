This submission is in response to the Washington Nationals R&D questionnaire for the winter of 2023.

To complete this, the workflow is in this order and can be mirrored on the reviewers machine by following this methodology:
1. mySQL script creates the table skeletons
2. Jupyter Notebook contains logic for player, game and pitch data and subsequently creates the tables.
3. Python scripts uses same algorithm generation and logic to return pitching matrices for various team and date combos determined by the user. hweinsch_nats_r_and_d.py and driver.py. Requirements are contained in the requirements.txt file. To run: 
	conda install -c conda-forge --file requirements.txt

4. Shell Script automates the team/date combos to obtain the matrix from. Therefore, teams can be selected by simply changing the contents of the arrays in the .sh script.

	NOTE: Python script can be ran manually instead by way of the shell script with command:
	          		    python driver.py team date
	      where team is an integer 1-30 and date is of the form "yyyy-mm-dd"