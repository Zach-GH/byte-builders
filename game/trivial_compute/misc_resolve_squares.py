def resolve_square(Player, Square):
    event = get_square(Square)
    if "category" in event:
        event_parts = event.split('|')
        correct = run_question_gui_instance(event_parts[1])
        if correct:
            return "reroll"
        else:
            return "end"
        
    if "HQ" in event:
        event_parts = event.split('|')
        correct = run_question_gui_instance(event_parts[1])
        if correct:
            addScore(event_parts[1],Player)
            return "reroll"
        else:
            return "end"
    
    if event == "Roll Again":
        return "reroll"
    
    if event == "Trivial Compute":
        if check_win_condition(Player) == False:
            return "end"
        category = run_category_selection_gui()
        correct = run_question_gui_instance(category)
        if correct:
            return "win game"
        else:
            return "end"
