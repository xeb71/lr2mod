init 2 python:
    # Follow Me Requirements
    def mc_start_follow_requirement(person):
        return not person.follow_mc and person.love > 20 and person.obedience >= 120

    def mc_stop_follow_requirement(person):
        return person.follow_mc

    def mc_action_lasik_surgery_person_requirement(person):
        if person.love < 20: # you need have some connection with her to offer this
            return False
        if person.has_event_day("lasik_surgery"):
            return False

        if isinstance(person.base_outfit, Outfit) and person.base_outfit.has_glasses:
            if person.love < 30:
                return "Requires: 30 Love"
            if not mc.business.has_funds(5000):
                return "Not enough money"
            return True
        return False

    def perform_lasik_surgery_requirement(start_day):
        return day > start_day

    def after_lasik_surgery_requirement(person):
        return True

    #REMOVED: Feature would mess-up dynamic function binding
    def mc_action_rename_person_requirement(person):
        return False

    # Spend the Night Requirements
    def mc_action_spend_the_night_requirement(person):
        if time_of_day == 4 and person.love > 50 and mc.is_at(person.home): #Has to be night, need to have some love and be in the_person's home location
            return True
        return False

    def mc_remove_person_requirement(person):
        return person in known_people_in_the_game(unique_characters())

    def favour_success_chance(obedience, offset=0, love=0):
        # Base: 80 obedience = 0%, 100 obedience = 40%, 150+ obedience = 100%
        # Moderate favour adds offset=10; Large favour adds offset=20 (so Large: 100=0%, 120=40%, 170+=100%)
        # Every 20 love adds +5% to the final chance (uncapped at 100%)
        low = 80 + offset
        mid = 100 + offset
        high = 150 + offset
        if obedience >= high:
            base = 1.0
        elif obedience >= mid:
            base = 0.4 + (obedience - mid) * (0.6 / (high - mid))
        elif obedience >= low:
            base = (obedience - low) * (0.4 / (mid - low))
        else:
            base = 0.0
        love_bonus = (love // 20) * 0.05
        return min(1.0, base + love_bonus)

    def _photo_favour_opinion_chance(person):
        """Returns the chance (0.0–1.0) that a photo favour will nudge a sexy opinion.
        Base ~10% from suggestibility, +5% per trance level."""
        base = getattr(person, 'suggestibility', 10) / 100.0  # usually ~0.10
        trance_bonus = 0.0
        if person.has_exact_role(very_heavy_trance_role):
            trance_bonus = 0.15
        elif person.has_exact_role(heavy_trance_role):
            trance_bonus = 0.10
        elif person.has_exact_role(trance_role):
            trance_bonus = 0.05
        return min(base + trance_bonus, 1.0)

    def _try_photo_opinion_increase(person, topics):
        """Roll once; on success, increase opinion for each topic in the list."""
        if renpy.random.random() < _photo_favour_opinion_chance(person):
            for topic in topics:
                person.increase_opinion_score(topic, max_value=2)

    def do_a_favour_tooltip(person):
        chance_pct = int(favour_success_chance(person.obedience, love=person.love) * 100)
        truncated = (chance_pct // 10) * 10
        return "Ask for a favour. Successfully asking for a favour tends to build obedience in your relationship. (about {}% chance)".format(truncated)

    def do_a_favour_requirement(person):
        if not ActionMod.is_mod_enabled(do_a_favour_action):
            return False

        if mc.energy < 15:
            return "Requires: {energy=15}"
        if person.has_event_delay("obedience_favour", 1): #once per day
            return True
        return "Asked for a favour too recently"

init 5 python:
    mc_start_follow_action = ActionMod("Follow me", mc_start_follow_requirement, "mc_start_follow_label", menu_tooltip = "Ask a girl to follow you around town.", category = "Generic People Actions")
    mc_stop_follow_action = ActionMod("Stop following me", mc_stop_follow_requirement, "mc_stop_follow_label", menu_tooltip = "Ask the girl stop following you.", allow_disable = False, category = "Generic People Actions")

    # Spend the Night | Allows you to sleep in the home of a person you have increased the love stat.
    mc_spend_the_night_action = ActionMod("Spend the night with girl", mc_action_spend_the_night_requirement, "mc_spend_the_night_label", menu_tooltip = "Allows you to sleep in this location.", category = "Generic People Actions", initialization = init_action_mod_disabled)

    mc_lasik_surgery_action = ActionMod("Pay for LASIK surgery\n{menu_red}Costs: $5000{/menu_red}", mc_action_lasik_surgery_person_requirement, "mc_action_lasik_surgery_label", menu_tooltip = "You don't like a girl wearing glasses, offer to pay for LASIK surgery.", category = "Generic People Actions")

    mc_remove_person_action = ActionMod("Remove from game", mc_remove_person_requirement, "mc_remove_person_label", menu_tooltip = "You are not interested in a girl. This will remove her from the game.", category = "Generic People Actions", initialization = init_action_mod_disabled)

    main_character_actions_list = [mc_start_follow_action, mc_stop_follow_action, mc_spend_the_night_action, mc_lasik_surgery_action, mc_remove_person_action]

    do_a_favour_action = ActionMod("Ask for a Favour   {energy=-15}", do_a_favour_requirement, "do_a_favour_label", category = "Generic People Actions", initialization = init_action_mod_disabled,
        menu_tooltip = do_a_favour_tooltip)
    chat_actions.append(do_a_favour_action)

# NOTE: Not sure where to place these actions yet. Basically actions that could fit on any person regardless of role.
label mc_spend_the_night_label(person): # Consider adding the sleep_action to the_person's room, but stats jump all over the place so doesn't necessarily make sense.
    "You go to sleep in [person.home.formal_name]."
    $ the_person.change_stats(happiness = 5, love = 3)
    call advance_time() from _call_advance_time_spend_the_night
    return

# Follower Labels
label mc_start_follow_label(person):
    "You tell [person.title] to follow you around."

    $ the_person.follow_mc = True
    person "Ok, let's go."
    jump game_loop      # exit talk menu

label mc_stop_follow_label(person):
    python:
        if the_person.get_destination() is the_person.home:
            schedule_destination = "my room"
        elif the_person.get_destination():
            schedule_destination = f"the {the_person.get_destination().formal_name}"
        else:
            schedule_destination = "somewhere else"

    "You tell [person.title] to stop following you around."

    $ the_person.follow_mc = False

    $ the_person.draw_person(position = "walking_away")

    $ the_person.run_move() # This will trigger stat changes based on clothing, but shouldn't be problematic although it can be exploited.

    the_person.title "Okay [the_person.mc_title], I'll head over to [schedule_destination]."


    return

label mc_action_lasik_surgery_label(the_person):
    mc.name "[the_person.title], you have beautiful eyes, but they are always hidden behind your glasses."
    the_person "Don't you like them? I can wear different glasses tomorrow."
    mc.name "I mean, that I really would like to see you without any glasses."
    if renpy.random.randint(1,2) == 1:
        the_person "I'm sorry, but I can't wear lenses."
        mc.name "That's fine."
    else:
        the_person "If you like, I can start wearing lenses."
        mc.name "I don't think that's the right solution."

    mc.name "Could you take them off for a minute?"
    the_person "Sure."
    $ the_person.outfit.remove_glasses()
    $ the_person.draw_person()
    mc.name "Absolutely lovely."
    "She blushes a little at your comment."
    menu:
        "Offer LASIK surgery\n{menu_red}Costs: $5000{/menu_red}":
            mc.name "I made an appointment for you in the clinic for a LASIK surgery where your eyesight will be corrected."
            "[the_person.title] gives you a spontaneous hug."
            $ the_person.draw_person(position = "kissing")
            the_person "You make me so happy [the_person.mc_title], thank you so much!"
            "She puts her glasses back on, but she will let you know when the surgery is completed."
            python:
                the_person.change_stats(happiness = 10, love = 5, max_love = 80)
                mc.business.change_funds(-5000, stat = "Cosmetic Surgery")
                the_person.apply_planned_outfit()
                the_person.set_event_day("lasik_surgery")
                mc.business.add_mandatory_crisis(
                    Action("Perform LASIK surgery",
                        perform_lasik_surgery_requirement,
                        "perform_lasik_surgery_label",
                        requirement_args = [day + 2],
                        args = [the_person])
                )
        "Don't":
            mc.name "Thank you, [the_person.title]."
            the_person "Anytime, [the_person.mc_title]."
            $ the_person.apply_planned_outfit()
    return

label perform_lasik_surgery_label(the_person):
    python:
        the_person.base_outfit.remove_glasses()
        the_person.add_unique_on_room_enter_event(
            Action("After LASIK surgery", after_lasik_surgery_requirement, "after_lasik_surgery_label"),
        )
    return

label after_lasik_surgery_label(the_person):
    $ the_person.draw_person()
    the_person "Hello [the_person.mc_title], what do you think? Do I look good without glasses?"
    mc.name "Absolutely, you look amazing without glasses."
    the_person "Thank you."
    $ clear_scene()
    return

label mc_remove_person_label(person):
    menu:
        "Are you sure?":
            $ person.remove_person_from_game()
            $ jump_game_loop()
        "Reconsider":
            pass
    return

#Obedience Actions
label do_a_favour_label(the_person):
    mc.name "Hey. I was wondering if you would be willing to do me a favour."
    if the_person.obedience < 70:
        "[the_person.possessive_title!c] scoffs and rolls her eyes."
        the_person "Probably not, but shoot your shot, [the_person.mc_title]."
    elif the_person.obedience < 100:
        the_person "Maybe, what do you need?"
    elif the_person.obedience < 130:
        "[the_person.possessive_title!c] smiles."
        the_person "If I have time. What do you need?"
    else:
        "[the_person.possessive_title!c] smiles wide."
        the_person "Anything for you, [the_person.mc_title]."
    $ _small_chance = (int(favour_success_chance(the_person.obedience, 0, the_person.love) * 100) // 10) * 10
    $ _mod_chance   = (int(favour_success_chance(the_person.obedience, 10, the_person.love) * 100) // 10) * 10
    $ _large_chance = (int(favour_success_chance(the_person.obedience, 20, the_person.love) * 100) // 10) * 10
    $ small_fav_tooltip = "A small request. About {}% success. Obedience +1 on success.".format(_small_chance)
    $ mod_fav_tooltip   = "Get her phone number, take her photo, or other moderate requests. About {}% success. Obedience +2 on success. Requires 3 successful small favours.".format(_mod_chance)
    $ large_fav_tooltip = "Ask for something personal - address, chores, or social media. About {}% success. Obedience +3 on success. Requires phone number and 3 successful moderate favours.".format(_large_chance)
    menu:
        "Small Favour (tooltip)[small_fav_tooltip]":
            menu:
                "Borrow $5":
                    $ mc.change_energy(-15)
                    $ favour_success = renpy.random.random() < favour_success_chance(the_person.obedience, 0, the_person.love)
                    $ the_person.favour_count_small += 1
                    if mc.is_home:
                        mc.name "Hey, I'm a little short. Any chance I can borrow $5 to grab some coffee?"
                        if favour_success:
                            the_person "Uhh, yeah I guess that would be okay."
                            "[the_person.possessive_title!c] grabs her purse and hands you a $5 bill from it."
                            mc.name "Thanks!"
                            $ mc.business.change_funds(5)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "I'm not your personal bank account, [the_person.mc_title]."
                            mc.name "Ah, sorry."
                    elif mc.is_at_office:
                        mc.name "I accidentally left my wallet at home. Can I borrow $5 to grab something from the vending machine?"
                        if favour_success:
                            the_person "Oh, sure. I'm sure you're good for it, right?"
                            mc.name "Of course."
                            $ mc.business.change_funds(5)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "Aren't you supposed to be paying me? Sorry, I don't carry cash, anyway..."
                            mc.name "Right, sorry."
                    else:
                        mc.name "Hey, I left my wallet at home. Can you spot me $5 for a coffee?"
                        if favour_success:
                            the_person "Oh, sure. I'm sure you're good for it, right?"
                            mc.name "Of course."
                            $ mc.business.change_funds(5)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "Sorry, I don't carry cash [the_person.mc_title]."
                            mc.name "Right, sorry."
                    if favour_success:
                        $ the_person.favour_count_small_success += 1

                "Ask her to grab you a coffee":
                    $ mc.change_energy(-15)
                    $ favour_success = renpy.random.random() < favour_success_chance(the_person.obedience, 0, the_person.love)
                    $ the_person.favour_count_small += 1
                    if mc.is_home:
                        mc.name "Hey, you wouldn't mind making me a coffee, would you?"
                        if favour_success:
                            the_person "Sure, how do you take it?"
                            mc.name "Just milk, thanks."
                            "[the_person.possessive_title!c] heads to the kitchen and comes back a few minutes later with a hot cup."
                            $ mc.change_energy(mc.max_energy * 0.05)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "Make your own coffee, [the_person.mc_title]."
                            mc.name "Fair enough."
                    elif mc.is_at_office:
                        mc.name "I'm swamped right now. Any chance you could grab me a coffee from the break room?"
                        if favour_success:
                            the_person "Sure, I was just heading that way anyway."
                            "[the_person.possessive_title!c] comes back a few minutes later with a steaming cup."
                            mc.name "Thank you, I really needed that."
                            $ mc.change_energy(mc.max_energy * 0.05)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "I'm not your assistant, [the_person.mc_title]."
                            mc.name "Right, sorry."
                    else:
                        mc.name "Hey, could you grab me a coffee? I'll pay you back."
                        if favour_success:
                            the_person "Okay, what do you want?"
                            mc.name "Just a regular coffee, thanks."
                            "[the_person.possessive_title!c] comes back with a coffee and hands it to you."
                            $ mc.change_energy(mc.max_energy * 0.05)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "Get your own coffee, [the_person.mc_title]."
                            mc.name "Worth a shot."
                    if favour_success:
                        $ the_person.favour_count_small_success += 1

                "Borrow something small":
                    $ mc.change_energy(-15)
                    $ favour_success = renpy.random.random() < favour_success_chance(the_person.obedience, 0, the_person.love)
                    $ the_person.favour_count_small += 1
                    if mc.is_home:
                        mc.name "Hey, do you have any aspirin? I've got a bit of a headache."
                        if favour_success:
                            the_person "Yeah, one second."
                            "[the_person.possessive_title!c] rummages around and produces a couple of aspirin."
                            mc.name "Thanks, you're a lifesaver."
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "Sorry, I don't have any on me."
                            mc.name "No worries."
                    elif mc.is_at_office:
                        mc.name "Hey, could I borrow a pen real quick? Mine just ran out."
                        if favour_success:
                            the_person "Sure, here."
                            "[the_person.possessive_title!c] hands you a pen."
                            mc.name "Thanks, I'll bring it right back."
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "Sorry, this is my only one."
                            mc.name "No problem."
                    else:
                        mc.name "My phone is almost dead. Could I borrow your charger for a bit?"
                        if favour_success:
                            the_person "Yeah, sure. Don't go too far though."
                            "[the_person.possessive_title!c] hands you a charging cable."
                            mc.name "Thanks, I'll be quick."
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "Sorry, mine probably won't fit your phone."
                            mc.name "Worth a try."
                    if favour_success:
                        $ the_person.favour_count_small_success += 1

                "Ask for a small hand":
                    $ mc.change_energy(-15)
                    $ favour_success = renpy.random.random() < favour_success_chance(the_person.obedience, 0, the_person.love)
                    $ the_person.favour_count_small += 1
                    if mc.is_home:
                        mc.name "Hey, could you give me a hand bringing in the groceries?"
                        if favour_success:
                            the_person "Sure, no problem."
                            "The two of you make short work of the groceries."
                            mc.name "Thanks, appreciate it."
                            if mc.arousal < 50:
                                $ mc.change_arousal(5)
                            if the_person.arousal < 50:
                                $ the_person.change_arousal(5)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "I'm a bit busy right now, sorry."
                            mc.name "No worries."
                    elif mc.is_at_office:
                        mc.name "Hey, could you give me a hand with this for just a second?"
                        if favour_success:
                            the_person "Sure, what do you need?"
                            "She helps you out for a moment."
                            mc.name "Perfect, thanks."
                            if mc.arousal < 50:
                                $ mc.change_arousal(5)
                            if the_person.arousal < 50:
                                $ the_person.change_arousal(5)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "I've got my own work to get through, sorry."
                            mc.name "No problem."
                    else:
                        mc.name "Hey, could you give me a quick hand with something?"
                        if favour_success:
                            the_person "Sure, what is it?"
                            "She helps you with the small task without complaint."
                            mc.name "Thanks, that really helped."
                            if mc.arousal < 50:
                                $ mc.change_arousal(5)
                            if the_person.arousal < 50:
                                $ the_person.change_arousal(5)
                            if the_person.obedience < 130:
                                $ the_person.change_obedience(1)
                        else:
                            the_person "Sorry, I'm in a bit of a rush."
                            mc.name "No worries."
                    if favour_success:
                        $ the_person.favour_count_small_success += 1

                "Never mind":
                    mc.name "Never mind, it's okay."
                    return

        "Moderate Favour (tooltip)[mod_fav_tooltip]" if the_person.favour_count_small_success >= 3 and the_person.has_event_delay("obedience_med_favour", TIER_1_TIME_DELAY):
            $ mc.change_energy(-15)
            $ favour_success = renpy.random.random() < favour_success_chance(the_person.obedience, 10, the_person.love)
            $ the_person.favour_count_moderate += 1
            if not mc.phone.has_number(the_person):
                mc.name "I was just wondering if I could get your number."
                if favour_success:
                    the_person "I suppose that would be okay. Just no drunk 3 am phone calls, okay?"
                    mc.name "Of course."
                    "You grab your phone and quickly put her number in as she lists it off for you."
                    $ mc.phone.register_number(the_person)
                    if the_person.obedience < 150:
                        $ the_person.change_obedience(2)
                else:
                    the_person "Yeah right, I don't think we're close enough for something like that."
                    "Ouch."
            elif not the_person.has_phone_photo:
                mc.name "You look amazing in that outfit. Can I snap a picture to update your profile on my phone?"
                if favour_success:
                    the_person "Yeah, I can do that!"
                    $ _contact_outfit = the_person.outfit.get_copy()
                    $ the_person.draw_person(position = "stand3")
                    "You quickly snap a picture of [the_person.possessive_title]."
                    $ add_insta_photo_to_history(the_person, "outfit", _contact_outfit, "stand3", reply="This is me in my work outfit — just for your contact list!", source="favour")
                    $ the_person.draw_person()
                    $ the_person.has_phone_photo = True
                    if the_person.obedience < 150:
                        $ the_person.change_obedience(2)
                else:
                    the_person "Sorry, I'm not here to play dress up for you."
                    "Ouch."
            else:
                menu:
                    "Update her contact photo":
                        mc.name "Hey, I need to update your contact photo. Can I take a quick pic?"
                        if favour_success:
                            the_person "Sure, let me fix my hair real quick."
                            $ _contact_outfit = the_person.outfit.get_copy()
                            $ the_person.draw_person(position = "stand3")
                            "You snap a fresh photo of [the_person.possessive_title]."
                            $ add_insta_photo_to_history(the_person, "outfit", _contact_outfit, "stand3", reply="Fresh contact photo, as requested!", source="favour")
                            $ the_person.draw_person()
                            if the_person.obedience < 150:
                                $ the_person.change_obedience(2)
                        else:
                            the_person "Sorry, I'm really not in the mood for photos right now."
                            "Ouch."
                    "Ask for playlist recommendations":
                        mc.name "I'm trying to put together a playlist. Can you send me some of your favourite songs?"
                        if favour_success:
                            the_person "Oh fun! Yeah, give me a minute."
                            "Your phone lights up with a list of song recommendations from [the_person.possessive_title]."
                            if the_person.obedience < 150:
                                $ the_person.change_obedience(2)
                            $ the_person.change_love(1)
                        else:
                            the_person "Sorry, my music taste is kind of private."
                            "Ouch."
                    "Ask to grab a snack together":
                        mc.name "Hey, do you want to grab a snack together? I could use a quick break."
                        if favour_success:
                            the_person "Yeah, that sounds nice actually. Let me know when you're ready."
                            if the_person.obedience < 150:
                                $ the_person.change_obedience(2)
                            call advance_time() from _call_advance_time_mod_favour_lunch
                        else:
                            the_person "I'm good, thanks though."
                            "Ouch."
                    "Take a topless photo" if the_person.sluttiness >= (45 if not the_person.outfit.wearing_bra else 35):
                        mc.name "I know this is a little forward, but... could I take a quick photo of just your chest? Just for me."
                        if favour_success:
                            if the_person.opinion.showing_her_tits >= 1:
                                the_person "Ha, I thought you might ask something like that eventually. Fine, just for you."
                            else:
                                the_person "I... I guess, just this once. Don't share it."
                            $ _saved_outfit = the_person.outfit
                            $ _snap_outfit = _saved_outfit.get_copy()
                            $ _snap_outfit.strip_to_tits(prefer_half_off = True)
                            $ the_person.outfit = _snap_outfit
                            $ the_person.draw_person(position = "stand4", display_transform = character_right(zoom = 2.5, yoffset = 0.65))
                            "You snap a quick photo of [the_person.possessive_title]."
                            $ add_insta_photo_to_history(the_person, "topless", _snap_outfit, "stand4", reply="I let you take this when we were alone... don't show anyone.", source="favour")
                            $ the_person.outfit = _saved_outfit
                            $ the_person.draw_person()
                            $ the_person.change_slut(1)
                            if the_person.obedience < 150:
                                $ the_person.change_obedience(2)
                            $ _try_photo_opinion_increase(the_person, ["showing her tits"])
                        else:
                            the_person "Are you serious? No way."
                            "Ouch."
                    "Take a backside photo" if the_person.sluttiness >= (40 if not the_person.outfit.wearing_panties else 30):
                        mc.name "You have an incredible figure. Could I take a photo of just... your backside? Just between us."
                        if favour_success:
                            if the_person.opinion.showing_her_ass >= 1:
                                the_person "Oh you like the view back there? Alright, go for it."
                            else:
                                the_person "I... okay, just don't make this weird."
                            $ _saved_outfit = the_person.outfit
                            $ _snap_outfit = _saved_outfit.get_copy()
                            $ _snap_outfit.strip_bottom_to_underwear()
                            $ the_person.outfit = _snap_outfit
                            $ the_person.draw_person(position = "back_peek", display_transform = character_right(zoom = 2.5, yoffset = 0.30))
                            "You snap a quick photo of [the_person.possessive_title]."
                            $ add_insta_photo_to_history(the_person, "ass", _snap_outfit, "back_peek", reply="You convinced me to pose for this when no one was around... keep it between us.", source="favour")
                            $ the_person.outfit = _saved_outfit
                            $ the_person.draw_person()
                            $ the_person.change_slut(1)
                            if the_person.obedience < 150:
                                $ the_person.change_obedience(2)
                            $ _try_photo_opinion_increase(the_person, ["showing her ass"])
                        else:
                            the_person "Absolutely not. What kind of person do you think I am?"
                            "Ouch."
                    "Take a nude photo" if the_person.sluttiness >= (60 if not the_person.outfit.wearing_panties else 50):
                        mc.name "I know this is pushing it, but... could I take a quick photo of just your... lower half? Just for me, I promise."
                        if favour_success:
                            if the_person.opinion.showing_her_ass >= 1:
                                the_person "You want a photo of that? Ha, sure... nothing you haven't seen before."
                            else:
                                the_person "I can't believe I'm agreeing to this... okay, but this stays between us."
                            $ _saved_outfit = the_person.outfit
                            $ _snap_outfit = _saved_outfit.get_copy()
                            $ _snap_outfit.strip_to_tits()
                            $ _snap_outfit.remove_shirt()
                            $ _snap_outfit.strip_to_vagina(prefer_half_off = True)
                            $ the_person.outfit = _snap_outfit
                            $ the_person.draw_person(position = "stand3", display_transform = character_right(zoom = 2.5, yoffset = 0.65))
                            "You snap a quick photo of [the_person.possessive_title]."
                            $ add_insta_photo_to_history(the_person, "nude", _snap_outfit, "stand3", reply="I can't believe I let you take this... you owe me one.", source="favour")
                            $ the_person.outfit = _saved_outfit
                            $ the_person.draw_person()
                            $ the_person.change_slut(1)
                            if the_person.obedience < 150:
                                $ the_person.change_obedience(2)
                            $ _try_photo_opinion_increase(the_person, ["not wearing anything"])
                        else:
                            the_person "Absolutely not! Don't ever ask me something like that again."
                            "Ouch."
                    "Never mind":
                        $ mc.change_energy(15)
                        $ the_person.favour_count_moderate -= 1
                        mc.name "Never mind, it's okay."
                        return
            if favour_success:
                $ the_person.favour_count_moderate_success += 1
            $ the_person.set_event_day("obedience_med_favour")
        "Large Favour (tooltip)[large_fav_tooltip]" if the_person.favour_count_moderate_success >= 3 and mc.phone.has_number(the_person) and the_person.has_event_delay("obedience_large_favour", TIER_2_TIME_DELAY):
            $ mc.change_energy(-15)
            $ favour_success = renpy.random.random() < favour_success_chance(the_person.obedience, 20, the_person.love)
            $ the_person.favour_count_large += 1
            if the_person.is_family:
                if mc.is_home:
                    mc.name "Hey, can I ask for a huge favour?"
                    the_person "Umm, maybe. What do you need?"
                    if time_of_day < 2:
                        mc.name "I really need to get going, could you pack me a lunch? I don't think I have time today."
                    else:
                        mc.name "Can you get the trash and the dishes tonight? I know it's my turn, but I have work stuff I really need to get done."
                    if favour_success:
                        the_person "I... yeah I guess I can do that. Just this once?"
                        mc.name "Of course."

                        if the_person.obedience < 160:
                            $ the_person.change_obedience(3)
                    else:
                        the_person "Nope! The world doesn't revolve around you—find a way to get it done yourself!"
                else:
                    mc.name "Hey, can I ask for a favour?"
                    the_person "Umm, maybe?"
                    mc.name "I accidentally left my wallet at home, but I need to grab some food at the office today."
                    mc.name "Can you front me $20?"
                    if favour_success:
                        the_person "I... yeah I guess I can do that. Try not to make a habit out of this, okay?"
                        mc.name "Of course."
                        $ mc.business.change_funds(20)
                        if the_person.obedience < 160:
                            $ the_person.change_obedience(3)
                    else:
                        the_person "No way! If I give you money I'll never see it again!"
            else:
                menu:
                    "Get her address" if not the_person.mc_knows_address:
                        mc.name "Can I get your address? It would be handy to have."
                        if favour_success:
                            the_person "I guess. Just no unannounced 3 am booty calls, okay?"
                            mc.name "Of course."
                            $ the_person.learn_home()
                            if the_person.obedience < 160:
                                $ the_person.change_obedience(3)
                        else:
                            the_person "Yeah right! That is need to know information only, mister."
                            mc.name "Ah, okay..."
                    "Request more InstaPics" if the_person.has_role(instapic_role):
                        mc.name "Your InstaPics have been so hot lately. Could you take a few more today? I like to check it when I go to bed."
                        if favour_success:
                            the_person "Oh! I'm glad you like them. Yeah I could do that."
                            mc.name "Great! I appreciate it."
                            $ the_person.event_triggers_dict["insta_generate_pic"] = True
                            if the_person.obedience < 160:
                                $ the_person.change_obedience(3)
                        else:
                            the_person "Ummm, I just post when I get the chance. Sorry I'm not sure if I'll get around to it today or not."
                            mc.name "Ah, okay."
                    "Suggest InstaPic account" if not the_person.has_role(instapic_role):
                        mc.name "You look amazing today. Have you ever thought about starting an InstaPic account?"
                        mc.name "You really should. I know I would check it out!"
                        if favour_success:
                            the_person "You know, I had been considering doing that. I think you've convinced me, I'll do it later!"
                            mc.name "Great! I can't wait to see you post!"
                            $ the_person.learn_instapic()
                            if the_person.obedience < 160:
                                $ the_person.change_obedience(3)
                        else:
                            the_person "Sorry, I'm not really into social media."
                            mc.name "Okay, well if you ever change your mind, you would be great!"
                    "Quickie snapshot - cum on tits" if the_person.sluttiness >= (65 if not the_person.outfit.wearing_bra else 55):
                        mc.name "I've been thinking about you all day... I need you right now. Just a quick one, and I want to take a photo after."
                        if favour_success:
                            if the_person.opinion.giving_blowjobs >= 1:
                                the_person "Mmm, you're so bad... fine, but make it quick."
                            else:
                                the_person "I... okay, but this stays between us. I mean it."
                            $ the_person.draw_person(position = "blowjob")
                            "She drops to her knees and wraps her lips around your cock."
                            $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                            $ the_person.increase_blowjobs()
                            "You rest a hand on the back of her head as she bobs up and down on your shaft."
                            mc.name "Fuck, that feels amazing..."
                            "After a few minutes you feel your orgasm building."
                            mc.name "I'm about to cum..."
                            "She pulls back and you finish on her chest."
                            $ the_person.cum_on_tits()
                            $ ClimaxController.manual_clarity_release(climax_type = "tits", person = the_person)
                            $ _saved_outfit = the_person.outfit
                            $ _snap_outfit = _saved_outfit.get_copy()
                            $ _snap_outfit.strip_to_tits(prefer_half_off = True)
                            $ the_person.outfit = _snap_outfit
                            $ the_person.draw_person(position = "stand4", display_transform = character_right(zoom = 2.5, yoffset = 0.65))
                            "You grab your phone and snap a quick photo of her with your cum glistening on her chest."
                            $ add_insta_photo_to_history(the_person, "topless", _snap_outfit, "stand4", reply="I can't believe you took a photo of that... you better keep it safe.", source="favour")
                            $ the_person.outfit = _saved_outfit
                            $ the_person.draw_person()
                            $ the_person.change_slut(2)
                            if the_person.opinion.being_covered_in_cum < 0:
                                $ the_person.change_love(the_person.opinion.being_covered_in_cum)
                                if the_person.obedience < 160:
                                    $ the_person.change_obedience(6)
                            elif the_person.obedience < 160:
                                $ the_person.change_obedience(3)
                            $ _try_photo_opinion_increase(the_person, ["showing her tits", "being covered in cum"])
                        else:
                            the_person "Are you out of your mind? Absolutely not."
                            "Ouch."
                    "Quickie snapshot - cum on ass" if the_person.sluttiness >= (60 if not the_person.outfit.wearing_panties else 50):
                        mc.name "I've been thinking about you all day... I need you right now. Just a quick one, and I want to take a photo after."
                        if favour_success:
                            if the_person.opinion.giving_blowjobs >= 1:
                                the_person "Mmm, you're so bad... fine, but make it quick."
                            else:
                                the_person "I... okay, but this stays between us. I mean it."
                            $ the_person.draw_person(position = "blowjob")
                            "She drops to her knees and wraps her lips around your cock."
                            $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                            $ the_person.increase_blowjobs()
                            "You rest a hand on the back of her head as she bobs up and down on your shaft."
                            mc.name "Fuck, that feels amazing..."
                            "After a few minutes you feel your orgasm building."
                            mc.name "I'm about to cum... turn around."
                            "She turns around and you finish on her backside."
                            $ the_person.cum_on_ass()
                            $ ClimaxController.manual_clarity_release(climax_type = "ass", person = the_person)
                            $ _saved_outfit = the_person.outfit
                            $ _snap_outfit = _saved_outfit.get_copy()
                            $ _snap_outfit.strip_bottom_to_underwear()
                            $ the_person.outfit = _snap_outfit
                            $ the_person.draw_person(position = "back_peek", display_transform = character_right(zoom = 2.5, yoffset = 0.30))
                            "You grab your phone and snap a quick photo of her backside covered in your cum."
                            $ add_insta_photo_to_history(the_person, "ass", _snap_outfit, "back_peek", reply="I can't believe you took a photo of that... you better keep it safe.", source="favour")
                            $ the_person.outfit = _saved_outfit
                            $ the_person.draw_person()
                            $ the_person.change_slut(2)
                            if the_person.opinion.being_covered_in_cum < 0:
                                $ the_person.change_love(the_person.opinion.being_covered_in_cum)
                                if the_person.obedience < 160:
                                    $ the_person.change_obedience(6)
                            elif the_person.obedience < 160:
                                $ the_person.change_obedience(3)
                            $ _try_photo_opinion_increase(the_person, ["showing her ass", "being covered in cum"])
                        else:
                            the_person "Are you out of your mind? Absolutely not."
                            "Ouch."
                    "Quickie snapshot - cum on pussy" if the_person.sluttiness >= (80 if not the_person.outfit.wearing_panties else 70):
                        mc.name "I've been thinking about you all day... I need you right now. Just a quick one, and I want to take a photo after."
                        if favour_success:
                            if the_person.opinion.giving_blowjobs >= 1:
                                the_person "Mmm, you're so bad... fine, but make it quick."
                            else:
                                the_person "I... okay, but this stays between us. I mean it."
                            $ the_person.draw_person(position = "blowjob")
                            "She drops to her knees and wraps her lips around your cock."
                            $ the_person.draw_person(position = "blowjob", special_modifier = "blowjob")
                            $ the_person.increase_blowjobs()
                            "You rest a hand on the back of her head as she bobs up and down on your shaft."
                            mc.name "Fuck, that feels amazing..."
                            "After a few minutes you feel your orgasm building."
                            mc.name "I'm about to cum... spread your legs."
                            "She lies back and you pull out, finishing across her stomach and between her legs."
                            $ the_person.cum_on_stomach()
                            $ ClimaxController.manual_clarity_release(climax_type = "stomach", person = the_person)
                            $ _saved_outfit = the_person.outfit
                            $ _snap_outfit = _saved_outfit.get_copy()
                            $ _snap_outfit.strip_to_tits()
                            $ _snap_outfit.remove_shirt()
                            $ _snap_outfit.strip_to_vagina(prefer_half_off = True)
                            $ _snap_outfit.add_creampie_cum()
                            $ the_person.outfit = _snap_outfit
                            $ the_person.draw_person(position = "stand3", display_transform = character_right(zoom = 2.5, yoffset = 0.65))
                            "You grab your phone and snap a quick photo of her with your cum dripping down between her legs."
                            $ add_insta_photo_to_history(the_person, "nude", _snap_outfit, "stand3", reply="I can't believe you took a photo of that... you better keep it safe.", source="favour")
                            $ the_person.outfit = _saved_outfit
                            $ the_person.draw_person()
                            $ the_person.change_slut(2)
                            if the_person.opinion.being_covered_in_cum < 0:
                                $ the_person.change_love(the_person.opinion.being_covered_in_cum)
                                if the_person.obedience < 160:
                                    $ the_person.change_obedience(6)
                            elif the_person.obedience < 160:
                                $ the_person.change_obedience(3)
                            $ _try_photo_opinion_increase(the_person, ["not wearing anything", "being covered in cum"])
                        else:
                            the_person "Are you out of your mind? Absolutely not."
                            "Ouch."
                    "Never mind":
                        $ mc.change_energy(15)
                        $ the_person.favour_count_large -= 1
                        mc.name "Never mind, it's okay."
                        return
            $ the_person.set_event_day("obedience_large_favour")
        "Nevermind":
            mc.name "Nevermind, it's okay."
            return
    $ the_person.set_event_day("obedience_favour")
    return

label mc_move_to_private_location(the_person):
    $ old_mc_location = None
    if mc.location.person_count < 2:
        return False

    "You look around and see some people watching you, what do you want to do?"
    menu:
        "Go somewhere more private\n{menu_yellow}[mc.location.interruption_info_text]{/menu_yellow}":
            mc.name "Let's find somewhere a little more private."
            call mc_change_to_private_location(the_person) from _call_mc_change_to_private_location_move_to_private_location
            return True
        "Keep going\n{menu_yellow}[mc.location.watcher_info_text]{/menu_yellow}":
            return False

label mc_change_to_private_location(the_person):
    $ old_mc_location = mc.location

    # TODO: Add more appropriate private locations for hubs when needed
    if the_person.is_at_mc_house:
        $ ran_num = renpy.random.randint(0, 3)
        if ran_num == 0 and the_person.is_at(the_person.bedroom) and the_person.bedroom.person_count > 1:
            # bedroom is not private choose other location
            $ ran_num += renpy.random.randint(1, 3)
        if ran_num == 3 and kitchen.person_count > 0:
            # we can't go into the kitchen
            $ ran_num -= renpy.random.randint(1, 2)
        if ran_num == 0:
            $ mc.change_location(the_person.bedroom)
            "You take [the_person.possessive_title] to her bedroom."
        elif ran_num == 1:
            $ mc.change_location(home_shower)
            "You take [the_person.possessive_title] by the hand and lead her into the bathroom."
        elif ran_num == 2:
            $ mc.change_location(laundry_room)
            "You pull [the_person.possessive_title] into the laundry room."
        else:
            $ mc.change_location(kitchen)
            "You take [the_person.possessive_title] by the hand and lead her into the kitchen."
    elif the_person.is_at_job(prostitute_job):
        $ mc.change_location(downtown_hotel_room)
        "[the_person.possessive_title!c] takes you to a motel that rents rooms by the hour."
    elif mc.is_at(the_person.home):
        $ mc.change_location(the_person.bedroom)
        "You take [the_person.possessive_title] to her bedroom."
    elif mc.is_at(downtown_bar):
        $ mc.change_location(downtown_bar_bathroom)
        "You take [the_person.possessive_title] to the bathroom."
    elif mc.is_at(downtown_hotel):
        $ mc.change_location(downtown_hotel_room)
        "You take [the_person.possessive_title] to an empty hotel room."
    elif mc.is_at(hospital):
        $ mc.change_location(hospital_room)
        "You take [the_person.possessive_title] to an empty patient room."
    elif mc.is_at(gaming_cafe):
        $ mc.change_location(gaming_cafe_store_room)
        "You take [the_person.possessive_title] to the storage room."
    elif mc.is_at((mom_office_lobby, mom_offices)):
        $ mc.change_location(office_photocopy_room)
        "You take [the_person.possessive_title] to the photocopy room."
    elif mc.is_at_office:
        $ ran_num = renpy.random.randint(0, 2)
        if ran_num == 0:
            $ mc.change_location(work_bathroom)
            "You pull [the_person.possessive_title] into one of the bathrooms at your office."
        elif ran_num == 1:
            $ mc.change_location(storage_room)
            "You take [the_person.possessive_title]'s hand and lead her to an empty storage room and lock the door behind you."
        else:
            $ mc.change_location(ceo_office)
            "You take [the_person.possessive_title] by the arm and lead her to your office."
    elif mc.is_at(mall_hub):
        if mc.is_at(clothing_store):
            $ mc.change_location(changing_room)
            "You pull [the_person.possessive_title] into the dressing room."
        else:
            $ mc.change_location(mall_bathroom)
            "You take [the_person.possessive_title] to the mall bathroom."
    elif mc.is_at(sports_center_hub):
        $ mc.change_location(gym_shower)
        "You take [the_person.possessive_title] to the gym's shower area."
    elif mc.is_at(downtown_hub):
        $ mc.change_location(mall_bathroom)
        "You take [the_person.possessive_title] into a public bathroom nearby."
    elif mc.is_at(strip_club_hub):
        $ mc.change_location(strip_club_dressing_room)
        "You take [the_person.possessive_title] into the dressing room."
    elif mc.is_at(sex_shop_hub):
        $ mc.change_location(sex_store_storage)
        "You take [the_person.possessive_title] to the storage room."
    elif mc.is_at(university_hub):
        $ ran_num = renpy.random.randint(0, (3 if kaya.progress.love_step >=3 and (day % 7 in  (5,6) or time_of_day not in (1, 2)) else 2))
        if ran_num == 0:
            $ mc.change_location(university_bathroom)
            "You take [the_person.possessive_title] to one of the university's bathrooms."
        elif ran_num == 1:
            $ mc.change_location(university_study_room)
            "You take [the_person.possessive_title] to one of the university's empty study rooms."
        elif ran_num == 2:
            $ mc.change_location(university_library)
            "You take [the_person.possessive_title] to one an empty part of the university library."
        else: # rare occasions
            $ mc.change_location(university_lab)
            "You take [the_person.possessive_title] to [nora.fname]'s lab at the university that should be deserted by now."
    else:
        "You take [the_person.possessive_title] to a more private spot."
        $ old_mc_location = None
    return

label mc_restore_original_location(the_person):
    if "old_mc_location" in globals() and isinstance(old_mc_location, Room):
        if not old_mc_location.is_private:
            # we are moving to a non private location, she needs to get dressed properly
            if (not the_person.outfit.matches(the_person.current_planned_outfit) or
                    the_person.outfit.has_half_off_clothing):
                $ the_person.call_dialogue("clothing_review")
        if old_mc_location.is_public:
            "Afterwards you and [the_person.possessive_title] go back to the [old_mc_location.formal_name]."
        else:
            "Afterwards you and [the_person.possessive_title] go back to [old_mc_location.formal_name]."

        $ mc.change_location(old_mc_location)
        $ old_mc_location = None
        return True
    elif not the_person.location.is_private:
        if (not the_person.outfit.matches(the_person.current_planned_outfit) or
                the_person.outfit.has_half_off_clothing):
            $ the_person.call_dialogue("clothing_review")
    $ old_mc_location = None
    return False
