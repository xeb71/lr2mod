init -2 python:
    pool_session_cost = 20

default _pool_saved_outfit = None  # Ren'Py store default; ensures old saves loaded mid-session have a safe value

init 3 python:
    def pool_requirement():
        if not mc.business.has_funds(pool_session_cost):
            return "Requires: $[pool_session_cost]"
        if mc.energy < 30:
            return "Requires: 30 energy"
        return True

    def build_pool_outfit(person):
        """Build a pool / swimwear outfit for *person*.

        Bottom: panties or strappy panties.
        Top: bra or strappy bra.
        """
        outfit = Outfit("Pool Outfit")
        # --- bottom ---
        bottom_choice = renpy.random.choice([panties, strappy_panties])
        outfit.add_lower(bottom_choice.get_copy(), colour_white)
        # --- top ---
        top_choice = renpy.random.choice([bra, strappy_bra])
        outfit.add_upper(top_choice.get_copy(), colour_white)
        return person.personalize_outfit(outfit, allow_skimpy=False)

    def pool_initialization(self):
        sports_center_pool.add_action(self)

    swim_laps_action = ActionMod("Swim Laps {image=time_advance}", pool_requirement, "swim_laps_label",
        initialization = pool_initialization, menu_tooltip = "Do some laps in the pool to build up your stamina.", category="Mall")

    invite_to_pool_action = ActionMod("Invite to Pool {image=time_advance}", pool_requirement, "invite_to_pool_label",
        initialization = pool_initialization, menu_tooltip = "Invite someone to join you for a swim.", category="Mall")

label swim_laps_label():
    menu:
        "Casual swim" if mc.energy >= 30:
            "You spend some time doing a relaxed swim around the pool."
            $ mc.change_energy(-30)
            if mc.max_energy < 160:
                $ mc.change_max_energy(3)
                "The cool water feels refreshing and you can feel your stamina improving."
            elif mc.max_energy < mc.max_energy_cap:
                $ mc.change_max_energy(2)
                "You feel a slight improvement from the swim."
            else:
                "You have reached your peak fitness. Further laps won't add to your stamina."

        "Casual swim\n{menu_red}Requires: 30 energy{/menu_red} (disabled)" if mc.energy < 30:
            pass

        "Intensive laps" if mc.energy >= 50:
            "You push yourself through an intensive set of laps."
            $ mc.change_energy(-50)
            if mc.max_energy < 180:
                $ mc.change_max_energy(6)
                "Your arms burn and your lungs ache, but you can already feel the payoff."
            elif mc.max_energy < mc.max_energy_cap:
                $ mc.change_max_energy(3)
                "You feel a solid improvement from the intensive effort."
            else:
                "You have reached your peak fitness. Further laps won't add to your stamina."

        "Intensive laps\n{menu_red}Requires: 50 energy{/menu_red} (disabled)" if mc.energy < 50:
            pass

        "Nothing":
            return

    $ mc.business.change_funds(-pool_session_cost)
    "You pay for the pool session; $[pool_session_cost] has been deducted from the company's credit card."
    call advance_time() from _call_advance_time_swim_laps
    return


label invite_to_pool_label():
    call screen main_choice_display(build_menu_items(
        [get_sorted_people_list(known_people_in_the_game(), "Swim with", "Back")]
        ))
    if isinstance(_return, Person):
        $ the_person = _return
        "You send [the_person.possessive_title] a message about a swim at the sports centre."
        "After a short while, you receive a reply..."
        call invite_to_pool_response(the_person) from _call_invite_to_pool_response
        call advance_time() from _call_advance_time_invite_pool
    return


label invite_to_pool_response(the_person):
    if the_person.happiness < 100 or the_person.obedience < 80:
        $ the_person.draw_person(emotion = "sad")
        the_person "Sorry, I'm not really feeling up to a swim right now."
        $ the_person.change_obedience(-2)
        $ clear_scene()
        return

    if the_person.personality == bimbo_personality:
        the_person "A swim? Sounds fun! Be right there, [the_person.mc_title]!"
    elif the_person.obedience > 140:
        the_person "Of course, [the_person.mc_title]. I'll be there shortly."
    elif the_person.sluttiness > 30:
        the_person "Swimming with you? I might need help with my sunscreen, [the_person.mc_title]."
    else:
        the_person "Sure, that sounds like a nice way to spend some time."
        $ the_person.change_happiness(+5)

    call pool_session_with_person(the_person) from _call_pool_session_with_person
    return


label pool_session_with_person(the_person):
    python:
        mc.change_location(sports_center_pool)
        if the_person not in sports_center_pool.people:
            the_person.change_location(sports_center_pool)
        _pool_saved_outfit = the_person.outfit.get_copy()
        _pool_outfit = build_pool_outfit(the_person)
        the_person.apply_outfit(_pool_outfit)
        ran_num = renpy.random.random() * 3
        the_person.draw_person(emotion = "happy")

    if ran_num < 1:
        "You take it easy with [the_person.possessive_title], drifting through the water side by side."
        if the_person.opinion.sports != 0:
            $ the_person.change_happiness(5 * the_person.opinion.sports)
            if the_person.opinion.sports > 0:
                "She seems completely at home in the water, gliding effortlessly from one end to the other."
            elif the_person.opinion.sports < 0:
                "She looks slightly uncomfortable, doing more floating than swimming."
            $ the_person.discover_opinion("sports")
        $ the_person.change_max_energy(5)
        "She seems to be getting a little fitter."
    elif ran_num < 2:
        "You do a few lengths together and then cool down by the poolside."
        if the_person.opinion.sports != 0:
            $ the_person.change_happiness(5 * the_person.opinion.sports)
            if the_person.opinion.sports > 0:
                "She keeps pace with you easily and seems to enjoy the exercise."
            elif the_person.opinion.sports < 0:
                "She keeps up but is clearly not in her element."
            $ the_person.discover_opinion("sports")
        $ the_person.change_max_energy(8)
        "The session seems to have done her some good."
    else:
        "You take [the_person.possessive_title] through a proper swim workout — intervals and all."
        if the_person.sluttiness > 20:
            $ the_person.draw_person(emotion = "happy")
            the_person "You have got me all hot and bothered just to cool me down again, [the_person.mc_title]."
        if the_person.opinion.sports != 0:
            $ the_person.change_happiness(5 * the_person.opinion.sports)
            if the_person.opinion.sports > 0:
                "She takes to the workout like a natural and finishes looking energised rather than exhausted."
            elif the_person.opinion.sports < 0:
                "She finishes looking winded and not particularly impressed."
            $ the_person.discover_opinion("sports")
        $ the_person.change_max_energy(10)
        "She is definitely building up her stamina."

    $ mc.change_energy(-30)

    if the_person.sluttiness > 50:
        $ the_person.draw_person()
        $ the_person.change_stats(arousal = renpy.random.randint(10, 25))
        if the_person.opinion.sports < 0:
            the_person "Well, I suppose the view made it worthwhile. Care to find somewhere private?"
        else:
            $ the_person.change_stats(happiness = 10, love = 2, max_love = 30)
            the_person "A swim always puts me in the mood for something more... interesting, [the_person.mc_title]."
        menu:
            "Have sex":
                mc.name "Follow me."
                the_person "Lead the way, [the_person.mc_title]."
                "You find a quiet corner of the changing rooms."
                $ the_person.break_taboo("kissing")
                $ old_outfit = the_person.outfit.get_copy()
                call fuck_person(the_person, start_position = kissing, start_object = mc.location.get_object_with_name("floor"), skip_intro = True) from _call_fuck_person_pool
                $ the_report = _return
                if the_report.get("girl orgasms", 0) > 0:
                    "[the_person.possessive_title!c] catches her breath and gives you a slow smile before reaching for her clothes."
                $ the_person.apply_outfit(old_outfit)
                $ the_person.draw_person(emotion = "happy")
                $ del old_outfit
            "Another time":
                mc.name "Maybe another time, [the_person.title]."
                $ the_person.change_happiness(-5)
    else:
        $ the_person.draw_person(emotion = "happy")
        if the_person.opinion.sports < 0:
            the_person "Well, at least it is over with."
        else:
            $ the_person.change_stats(happiness = 5, love = 1, max_love = 20)
            the_person "That was really enjoyable. We should do it again sometime."

    the_person "Thanks for the invite, [the_person.mc_title]."
    mc.name "Enjoy the rest of your day, [the_person.title]."
    $ the_person.apply_outfit(_pool_saved_outfit)
    $ the_person.draw_person(position="walking_away")

    $ mc.business.change_funds(-pool_session_cost)
    "You pay for the pool session; $[pool_session_cost] has been deducted from the company's credit card."

    $ mc.change_location(sports_center_pool)
    return
