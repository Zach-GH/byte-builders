# -r game resolution: max, med, min
# -t resolution type: full, sized, windowed
# -d game display: menu, gameboard, options, trophies, team
# -m Start the game with the music muted.

# Mac/Linux options
main: main.py
	./$@.py -r max -t full

main_1440: main.py
	./main.py -r med -t windowed -m

main_1080: main.py
	./main.py -r min -t sized

tc_server:
	./main.py -s

tc_question:
	./main.py -g

tc_database:
	./main.py -db

# Windows options
main_w:
	@python main.py -r max -t full

main_1440_w:
	@python main.py -r min -t sized -m

tc_server_w:
	@python main.py -s

tc_question_w:
	@python main.py -g

tc_database_w:
	@python main.py -db
