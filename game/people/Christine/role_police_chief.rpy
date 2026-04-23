
label mc_arrested_penalties(the_person = None):
    if christine_can_offer_fine_alternative(the_person):
        if police_chief.progress.lust_step == 0:
            $ police_chief.draw_person(position = "sitting")
            police_chief "Well... this is supposed to end with a fine."
            "Before she reaches for the paperwork, [police_chief.title] looks past you and slowly studies [the_person.title]."
            police_chief "But seeing what you two were up to has me thinking there might be another way to settle this."
            menu:
                "Pay the fine":
                    pass
                "Take her alternative":
                    call police_chief_alternative_fine_label(the_person) from _call_police_chief_alt_fine_01
                    return "alternative"
        elif police_chief.progress.lust_step == 1:
            $ police_chief.draw_person(position = "sitting")
            police_chief "You know, this is getting predictable."
            police_chief "You get caught with a hot girl, I haul you in, and suddenly I have to decide if I want to do my job... or enjoy the evidence."
            menu:
                "Pay the fine":
                    pass
                "Take her alternative":
                    call police_chief_alternative_fine_label(the_person) from _call_police_chief_alt_fine_02
                    return "alternative"
        else:
            $ police_chief.draw_person(position = "sitting")
            police_chief "You didn't really think I was going to let a girl like that leave without taking my cut, did you?"
            police_chief "Either you pay the fine, or the three of us go somewhere private and I forget the paperwork exists."
            menu:
                "Pay the fine":
                    pass
                "Take her alternative":
                    call police_chief_alternative_fine_label(the_person) from _call_police_chief_alt_fine_03
                    return "alternative"

    if mc_times_arrested() == 0:
        $ mc.business.change_funds(-100, stat = "City Fines")
        "Since this is your first offence, you get off with a light fine."
        $ police_chief.event_triggers_dict["times_arrested"] = 0
    elif mc_times_arrested() == 1:
        $ mc.business.change_funds(-500, stat = "City Fines")
        "Since this is your second offence, you get fined."
        police_chief "Seriously, don't do that again. You can't be doing that stuff in public!"
    elif mc_times_arrested() == 2:
        $ mc.business.change_funds(-5000, stat = "City Fines")
        "Since this is your third offence, you receive a heavy fine."
        police_chief "I guess you still haven't learned your lesson. I'm fining you the maximum amount under the law."
        police_chief "If this happens again, I'll have to let the city know you got problems with authority. Catch my drift?"
    elif mc_times_arrested() == 3:
        $ mc.business.change_funds(-5000, stat = "City Fines")
        "You once again receive a heavy fine."
        police_chief "Damn, you just can't keep your hands to yourself, can you?"
        police_chief "Guess I'll have to call this in to the city. Where did you say you work again?"
        $ mc.business.attention += 20
    elif mc_times_arrested() == 3:
        $ mc.business.change_funds(-5000, stat = "City Fines")
        "You once again receive a heavy fine."
        police_chief "Still screwing around with whores in public are you?"
        police_chief "Guess last time I didn't word my request with the city strongly enough."
        $ mc.business.attention += 50
    else:
        $ mc.business.change_funds(-5000, stat = "City Fines")
        "You once again receive a heavy fine."
        police_chief "Again. You're here AGAIN."
        police_chief "Enough is enough. Get out of here, I'm sure the city will be checking out your business now soon enough."
        $ mc.business.attention += 100
    $ police_chief.event_triggers_dict["times_arrested"] += 1
    return "fine"

label police_chief_alternative_fine_label(the_person):
    if police_chief.progress.lust_step == 0:
        police_chief "Here's what happens. I close the blinds, lose this report, and the two of you help me work off some stress."
        mc.name "That's one hell of an alternative."
        police_chief "It's generous, considering the amount of paperwork you just caused me."
    elif police_chief.progress.lust_step == 1:
        police_chief "Hands on the desk. Both of you."
        police_chief "If I'm going to keep waiving your fines, I'm going to start enjoying it properly."
    else:
        police_chief "Clothes off. I want both of you naked before I change my mind."
        police_chief "At this point, public indecency is basically just your way of booking me a threesome."

    $ police_chief.event_triggers_dict["times_arrested"] += 1
    $ scene_manager.clear_scene()
    $ scene_manager.add_actor(police_chief, display_transform = character_center_flipped)
    $ scene_manager.add_actor(the_person)
    "You and [the_person.title] exchange a quick look, then decide to take the deal."
    $ scene_manager.strip_to_vagina(person = police_chief)
    $ scene_manager.strip_to_vagina(person = the_person)
    $ police_chief.draw_person()
    if police_chief.progress.lust_step == 0:
        police_chief "Good. Now show me what kind of trouble you were causing before I interrupted."
    elif police_chief.progress.lust_step == 1:
        police_chief "Much better. I knew there was a reason I kept stopping by these calls myself."
    else:
        police_chief "That's it. If you insist on breaking the law, the least you can do is make it worth my time."
    call start_threesome(police_chief, the_person, start_position = Threesome_standing_embrace, start_object = make_desk(), private = True, affair_ask_after = False) from _call_start_threesome_police_chief_fine
    $ police_chief.progress.lust_step += 1
    $ police_chief.change_slut(10, 80)
    $ the_person.change_slut(2)
    $ the_person.change_stats(happiness = 3)
    $ police_chief.change_stats(happiness = 5, love = 1, max_love = 30)
    $ police_chief.apply_planned_outfit()
    $ the_person.apply_planned_outfit()
    $ scene_manager.clear_scene()
    $ scene_manager.add_actor(police_chief, position = "sitting")
    $ police_chief.draw_person()
    police_chief "Alright. We're done here."
    if police_chief.progress.lust_step == 1:
        police_chief "Officially, you paid your fine."
    elif police_chief.progress.lust_step == 2:
        police_chief "Don't look so surprised. You brought me exactly the kind of company I like."
    else:
        police_chief "Next time you get caught, skip the excuses and just assume I'm taking a more hands-on approach."
    return
