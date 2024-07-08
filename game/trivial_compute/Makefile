# -r game resolution: max, med, min
# -t resolution type: full, sized, windowed
# -d game display: menu, gameboard, options, trophies, team
# -m Start the game with the music muted.

main: main.py
	./$@.py -r max -t full

# Windows option
main_w:
	@python main.py -r max -t full

main_1440: main.py
	./main.py -r med -t sized

main_1080: main.py
	./main.py -r min -t windowed

tc_server:
	./main.py -s