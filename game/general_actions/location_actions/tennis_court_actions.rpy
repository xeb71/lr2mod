init -2 python:
    tennis_session_cost = 25

init 3 python:
    def tennis_requirement():
        if not mc.business.has_funds(tennis_session_cost):
            return "Requires: $[tennis_session_cost]"
        if mc.energy < 30:
            return "Requires: 30 energy"
        return True

    def build_tennis_outfit(person):
        """Build a tennis outfit for *person*.

        Bottom: white skirt, or mini skirt if sluttiness > 40.
        Top: random choice of tank top, cropped t-shirt, sleeveless top.
        Feet: sneakers.
        """
        outfit = Outfit("Tennis Outfit")
        # --- bottom ---
        if person.sluttiness > 40:
            outfit.add_lower(mini_skirt.get_copy(), colour_white)
        else:
            outfit.add_lower(skirt.get_copy(), colour_white)
        # --- top ---
        top_choice = renpy.random.choice([tanktop, tshirt, sleeveless_top])
        outfit.add_upper(top_choice.get_copy(), colour_white)
        # --- feet ---
        outfit.add_feet(sneakers.get_copy(), colour_white)
        return outfit

    def tennis_initialization(self):
        sports_center_tennis_courts.add_action(self)

    tennis_solo_action = ActionMod("Hit the Courts {image=time_advance}", tennis_requirement, "tennis_solo_label",
        initialization = tennis_initialization, menu_tooltip = "Practise your tennis game on the courts.", category="Mall")

    invite_to_tennis_action = ActionMod("Invite to Tennis {image=time_advance}", tennis_requirement, "invite_to_tennis_label",
        initialization = tennis_initialization, menu_tooltip = "Challenge someone to a game of tennis.", category="Mall")

    def tennis_noticeboard_requirement():
        return mom.event_triggers_dict.get("tennis_sponsorship_done", False)

    tennis_noticeboard_action = ActionMod("Check Notice Board", tennis_noticeboard_requirement, "tennis_noticeboard_standalone_label",
        initialization = tennis_initialization, menu_tooltip = "View the tennis team notice board and rosters.", category="Mall")

    def challenge_captain_requirement():
        if not mom.event_triggers_dict.get("tennis_sponsorship_done", False):
            return "Requires: Tennis sponsorship"
        if not mc.business.has_funds(tennis_session_cost):
            return "Requires: $[tennis_session_cost]"
        if mc.energy < 40:
            return "Requires: 40 energy"
        captains = [renpy.store.perky_leader, renpy.store.showoff_leader, renpy.store.commando_leader]
        if not any(c is not None and c.event_triggers_dict.get("tennis_met", False) for c in captains):
            return "Check team roster to see if captain is available"
        # At least one met captain must be physically at the courts right now.
        if not any(c is not None and c.event_triggers_dict.get("tennis_met", False) and c in sports_center_tennis_courts.people for c in captains):
            return "No captains at the courts right now"
        return True

    challenge_captain_action = ActionMod("Challenge a Captain {image=time_advance}", challenge_captain_requirement, "challenge_captain_label",
        initialization = tennis_initialization, menu_tooltip = "Challenge a team captain to a match of tennis.", category="Mall")

    def meet_candidate_requirement():
        if renpy.store.mc_team_secretary_team is None:
            return "Requires: Team secretary appointment"
        if mc.energy < 10:
            return "Requires: 10 energy"
        return True

    meet_candidate_action = ActionMod("Meet a Candidate", meet_candidate_requirement, "tennis_meet_candidate_label",
        initialization = tennis_initialization, menu_tooltip = "A hopeful player wants to audition — as team secretary, you decide.", category="Mall")

    def challenge_member_requirement():
        if renpy.store.mc_team_secretary_team is None:
            return "Requires: Team secretary appointment"
        if not mc.business.has_funds(tennis_session_cost):
            return "Requires: $[tennis_session_cost]"
        if mc.energy < 30:
            return "Requires: 30 energy"
        _sec_team = renpy.store.mc_team_secretary_team
        _members = renpy.store.tennis_teams.get(_sec_team, [])
        _here = [p for p in _members if p in sports_center_tennis_courts.people]
        if not _here:
            return "No team members at the courts right now"
        return True

    challenge_member_action = ActionMod("Challenge a Team Member {image=time_advance}", challenge_member_requirement, "challenge_member_label",
        initialization = tennis_initialization, menu_tooltip = "Challenge one of your team members to a match with a wager.", category="Mall")

    def resolve_tennis_set(tactic, energy_before, focus_stat, cap_difficulty):
        """Return (won, energy_cost) for one set of the minigame.

        tactic:        "power" | "rally" | "finesse"
        energy_before: mc.energy at the start of this set
        focus_stat:    mc.focus
        cap_difficulty: float 0–1, higher = harder captain
        """
        if tactic == "power":
            energy_cost = 15
            energy_factor = energy_before / max(mc.max_energy, 1)
            win_chance = 0.40 + energy_factor * 0.45 - cap_difficulty
        elif tactic == "rally":
            energy_cost = 10
            energy_factor = energy_before / max(mc.max_energy, 1)
            focus_factor = min(focus_stat / 10.0, 1.0)
            win_chance = 0.35 + energy_factor * 0.25 + focus_factor * 0.20 - cap_difficulty
        else:  # finesse
            energy_cost = 8
            focus_factor = min(focus_stat / 10.0, 1.0)
            win_chance = 0.30 + focus_factor * 0.50 - cap_difficulty
        win_chance = max(0.15, min(0.90, win_chance))
        won = renpy.random.random() < win_chance
        return won, energy_cost

label tennis_solo_label():
    menu:
        "Serve practice" if mc.energy >= 30:
            "You spend some time working on your serve at the back of the court."
            $ mc.change_energy(-30)
            if mc.max_energy < 160:
                $ mc.change_max_energy(3)
                "The repetitive motion pays off — you can feel your arm strengthening."
            elif mc.max_energy < mc.max_energy_cap:
                $ mc.change_max_energy(2)
                "You feel a modest improvement from the practice."
            else:
                "You have reached your peak fitness. Further practice won't add to your stamina."

        "Serve practice\n{menu_red}Requires: 30 energy{/menu_red} (disabled)" if mc.energy < 30:
            pass

        "Full match practice" if mc.energy >= 50:
            "You run drills the length of the court, pushing your footwork and endurance."
            $ mc.change_energy(-50)
            if mc.max_energy < 180:
                $ mc.change_max_energy(6)
                "Your legs ache but the effort has clearly done you good."
            elif mc.max_energy < mc.max_energy_cap:
                $ mc.change_max_energy(3)
                "You feel a solid improvement from the hard session."
            else:
                "You have reached your peak fitness. Further drills won't add to your stamina."

        "Full match practice\n{menu_red}Requires: 50 energy{/menu_red} (disabled)" if mc.energy < 50:
            pass

        "Nothing":
            return

    $ mc.business.change_funds(-tennis_session_cost)
    "You pay for the court hire; $[tennis_session_cost] has been deducted from the company's credit card."
    if mom.event_triggers_dict.get("tennis_sponsorship_done", False):
        call tennis_noticeboard_scene() from _call_tennis_noticeboard_scene_solo
    call advance_time() from _call_advance_time_tennis_solo
    return


label invite_to_tennis_label():
    call screen main_choice_display(build_menu_items(
        [get_sorted_people_list(known_people_in_the_game(), "Play tennis with", "Back")]
        ))
    if isinstance(_return, Person):
        $ the_person = _return
        "You message [the_person.possessive_title] about a game of tennis at the sports centre."
        "You wait for a reply..."
        call invite_to_tennis_response(the_person) from _call_invite_to_tennis_response
        call advance_time() from _call_advance_time_invite_tennis
    return


label invite_to_tennis_response(the_person):
    if the_person.happiness < 100 or the_person.obedience < 80:
        $ the_person.draw_person(emotion = "sad")
        the_person "I'm not really in the mood for tennis today, sorry."
        $ the_person.change_obedience(-2)
        $ clear_scene()
        return

    if the_person.personality == bimbo_personality:
        the_person "Tennis? Sure, I can wear that cute skirt! Be right there, [the_person.mc_title]!"
    elif the_person.obedience > 140:
        the_person "Of course, [the_person.mc_title]. I shall be right over."
    elif the_person.sluttiness > 30:
        the_person "A chance to show off my backhand — and my legs. I'm in, [the_person.mc_title]."
    else:
        the_person "Sounds great. See you on the court."
        $ the_person.change_happiness(+5)

    call tennis_session_with_person(the_person) from _call_tennis_session_with_person
    return


label tennis_session_with_person(the_person):
    python:
        mc.change_location(sports_center_tennis_courts)
        if the_person not in sports_center_tennis_courts.people:
            the_person.change_location(sports_center_tennis_courts)
        _tennis_outfit = build_tennis_outfit(the_person)
        the_person.apply_outfit(_tennis_outfit)
        ran_num = renpy.random.random() * 3
        the_person.draw_person(emotion = "happy")

    if ran_num < 1:
        "You and [the_person.possessive_title] hit the ball back and forth, keeping it casual."
        if the_person.opinion.sports != 0:
            $ the_person.change_happiness(5 * the_person.opinion.sports)
            if the_person.opinion.sports > 0:
                "She has a natural sense of timing and seems to genuinely enjoy herself."
            elif the_person.opinion.sports < 0:
                "She does her best but it is clear the sport is not really her thing."
            $ the_person.discover_opinion("sports")
        $ the_person.change_max_energy(5)
        "She seems to be getting a little fitter."
    elif ran_num < 2:
        "You play a proper set — some good rallies, a few winners, and plenty of laughter."
        if the_person.opinion.sports != 0:
            $ the_person.change_happiness(5 * the_person.opinion.sports)
            if the_person.opinion.sports > 0:
                "She is competitive and clearly enjoying every point."
            elif the_person.opinion.sports < 0:
                "She goes through the motions but is relieved when the set is over."
            $ the_person.discover_opinion("sports")
        $ the_person.change_max_energy(8)
        "The match was a good workout for both of you."
    else:
        "You push [the_person.possessive_title] hard — running her from corner to corner until she is breathing heavily."
        if the_person.sluttiness > 20:
            $ the_person.draw_person(emotion = "happy")
            the_person "You certainly know how to get a girl out of breath, [the_person.mc_title]."
        if the_person.opinion.sports != 0:
            $ the_person.change_happiness(5 * the_person.opinion.sports)
            if the_person.opinion.sports > 0:
                "Despite the hard work, she finishes with a broad smile and rosy cheeks."
            elif the_person.opinion.sports < 0:
                "She finishes the session looking exhausted and less than thrilled."
            $ the_person.discover_opinion("sports")
        $ the_person.change_max_energy(10)
        "She is definitely building up her stamina."

    $ mc.change_energy(-30)

    if the_person.sluttiness > 50:
        $ the_person.draw_person()
        $ the_person.change_stats(arousal = renpy.random.randint(10, 25))
        if the_person.opinion.sports < 0:
            the_person "At least the view was worth it. Perhaps we could find a better use for all this energy, [the_person.mc_title]?"
        else:
            $ the_person.change_stats(happiness = 10, love = 2, max_love = 30)
            the_person "There is something about working up a sweat with you that puts other things on my mind, [the_person.mc_title]."
        menu:
            "Have sex":
                mc.name "Let's find somewhere quiet."
                the_person "I know just the place."
                "You slip away to a secluded corner of the changing rooms."
                $ the_person.break_taboo("kissing")
                $ old_outfit = the_person.outfit.get_copy()
                call fuck_person(the_person, start_position = kissing, start_object = mc.location.get_object_with_name("floor"), skip_intro = True) from _call_fuck_person_tennis
                $ the_report = _return
                if the_report.get("girl orgasms", 0) > 0:
                    "[the_person.possessive_title!c] leans against the wall for a moment, catching her breath, then starts getting dressed with a contented smile."
                $ the_person.apply_outfit(old_outfit)
                $ the_person.draw_person(emotion = "happy")
                $ del old_outfit
            "Another time":
                mc.name "Maybe next time, [the_person.title]."
                $ the_person.change_happiness(-5)
    else:
        $ the_person.draw_person(emotion = "happy")
        if the_person.opinion.sports < 0:
            the_person "Well... I suppose it was good for me, even if I did not enjoy it much."
        else:
            $ the_person.change_stats(happiness = 5, love = 1, max_love = 20)
            the_person "That was a great game. We should play again soon."

    the_person "Thanks for the game, [the_person.mc_title]."
    mc.name "Good match, [the_person.title]. See you next time."
    $ the_person.draw_person(position="walking_away")

    $ mc.business.change_funds(-tennis_session_cost)
    "You pay for the court hire; $[tennis_session_cost] has been deducted from the company's credit card."

    # If mom is at the courts on one of her practice days, a notice board is visible near the entrance.
    if mom.event_triggers_dict.get("tennis_sponsorship_done", False):
        call tennis_noticeboard_scene(the_person) from _call_tennis_noticeboard_scene

    $ mc.change_location(sports_center_tennis_courts)
    return


label tennis_noticeboard_standalone_label():
    call tennis_noticeboard_scene() from _call_tennis_noticeboard_scene_standalone
    return


# --- Challenge a Captain ---

label challenge_captain_label():
    python:
        _perky_met    = perky_leader    is not None and perky_leader.event_triggers_dict.get("tennis_met", False) and perky_leader in sports_center_tennis_courts.people
        _showoff_met  = showoff_leader  is not None and showoff_leader.event_triggers_dict.get("tennis_met", False) and showoff_leader in sports_center_tennis_courts.people
        _commando_met = commando_leader is not None and commando_leader.event_triggers_dict.get("tennis_met", False) and commando_leader in sports_center_tennis_courts.people
        _perky_name    = perky_leader.display_name    if perky_leader    is not None else ""
        _showoff_name  = showoff_leader.display_name  if showoff_leader  is not None else ""
        _commando_name = commando_leader.display_name if commando_leader is not None else ""
        _challenge_target = None

    if not (_perky_met or _showoff_met or _commando_met):
        "None of the team captains you've met are at the courts right now. Try visiting during early morning or morning."
        return

    "You look around the courts for a captain to challenge to a proper match."

    menu:
        "Challenge [_perky_name] — Perky Team captain" if _perky_met:
            $ _challenge_target = perky_leader
        "Challenge [_showoff_name] — Showoff Team captain" if _showoff_met:
            $ _challenge_target = showoff_leader
        "Challenge [_commando_name] — Commando Team captain" if _commando_met:
            $ _challenge_target = commando_leader
        "Maybe another time":
            return

    call tennis_captain_match(_challenge_target) from _call_tennis_captain_match_outer
    $ mc.business.change_funds(-tennis_session_cost)
    "You pay for the court hire; $[tennis_session_cost] has been deducted from the company's credit card."
    call advance_time() from _call_advance_time_captain_challenge
    return


# Best-of-three minigame against a team captain.
# Energy and focus are the main attributes that decide each set.
# Winning the match increases the captain's obedience by 10.
label tennis_captain_match(captain):
    python:
        mc.change_location(sports_center_tennis_courts)
        _cap_team = captain.event_triggers_dict.get("tennis_team", "perky")
        _base_diff = {"perky": 0.35, "showoff": 0.50, "commando": 0.60}[_cap_team]
        # More obedient captain is marginally less aggressive.
        _cap_difficulty = _base_diff - max(0, captain.obedience - 80) * 0.002
        _cap_difficulty = max(0.20, min(0.75, _cap_difficulty))
        _sets_won  = 0
        _sets_lost = 0

        # Make captain visible on court in tennis attire.
        if captain not in sports_center_tennis_courts.people:
            captain.change_location(sports_center_tennis_courts)
        captain.apply_outfit(build_tennis_outfit(captain))
        captain.draw_person(emotion="default")

    mc.name "I'd like to challenge you to a proper match."
    captain "A challenge? I never turn those down. Best of three sets."
    mc.name "Then let's get started."
    "You warm up on opposite sides of the net. [captain.display_name] looks relaxed and unhurried."

    # --- Set 1 ---
    "The first set begins. You weigh up your options."

    menu:
        "Power serves — put your energy behind every shot" if mc.energy >= 15:
            python:
                _set1_won, _cost1 = resolve_tennis_set("power", mc.energy, mc.focus, _cap_difficulty)
                mc.change_energy(-_cost1)
            if _set1_won:
                "Your serve fires off the racket like a shot. [captain.display_name] scrambles but can't find a reply. You take the first set."
                $ _sets_won += 1
            else:
                "[captain.display_name] reads your delivery early and steps around it, punishing every second ball. She takes the first set."
                $ _sets_lost += 1
        "Power serves — {menu_red}Requires: 15 energy{/menu_red} (disabled)" if mc.energy < 15:
            pass
        "Steady baseline rally — wear her down with consistency":
            python:
                _set1_won, _cost1 = resolve_tennis_set("rally", mc.energy, mc.focus, _cap_difficulty)
                mc.change_energy(-_cost1)
            if _set1_won:
                "You trade groundstrokes patiently, waiting for your moment. [captain.display_name] starts forcing shots and gives the set away."
                $ _sets_won += 1
            else:
                "[captain.display_name]'s baseline game is tight and consistent. She outlasts you through the key games. She takes the first set."
                $ _sets_lost += 1
        "Touch and angles — outthink her with your focus":
            python:
                _set1_won, _cost1 = resolve_tennis_set("finesse", mc.energy, mc.focus, _cap_difficulty)
                mc.change_energy(-_cost1)
            if _set1_won:
                "Your angle play leaves [captain.display_name] wrong-footed at every turn. She shakes her head as you close out the set."
                $ _sets_won += 1
            else:
                "[captain.display_name] anticipates every trick, covering the net and driving through you. She takes the first set."
                $ _sets_lost += 1

    # --- Set 2 ---
    python:
        if _sets_won == 1:
            _set2_intro = f"One set up. {captain.display_name} narrows her eyes. She is not ready to give in."
        else:
            _set2_intro = "A set down — but there is still everything to play for."

    "[_set2_intro]"

    menu:
        "Power serves — unleash everything you have" if mc.energy >= 15:
            python:
                _set2_won, _cost2 = resolve_tennis_set("power", mc.energy, mc.focus, _cap_difficulty)
                mc.change_energy(-_cost2)
            if _set2_won:
                "Your power game stays at the same ferocious level. [captain.display_name] fights hard but you close out the second set."
                $ _sets_won += 1
            else:
                "She has adjusted to your serve now, stepping inside the baseline and drilling cross-court winners. She takes the second set."
                $ _sets_lost += 1
        "Power serves — {menu_red}Requires: 15 energy{/menu_red} (disabled)" if mc.energy < 15:
            pass
        "Steady baseline rally — keep the pressure up":
            python:
                _set2_won, _cost2 = resolve_tennis_set("rally", mc.energy, mc.focus, _cap_difficulty)
                mc.change_energy(-_cost2)
            if _set2_won:
                "Patience wins the day. You outrun [captain.display_name] through the second set and take it."
                $ _sets_won += 1
            else:
                "[captain.display_name] finds her rhythm in the long rallies and pulls the second set back."
                $ _sets_lost += 1
        "Touch and angles — keep her guessing":
            python:
                _set2_won, _cost2 = resolve_tennis_set("finesse", mc.energy, mc.focus, _cap_difficulty)
                mc.change_energy(-_cost2)
            if _set2_won:
                "Your placement keeps [captain.display_name] constantly off balance. A perfectly placed winner closes out the second set."
                $ _sets_won += 1
            else:
                "[captain.display_name] reads the pattern and kills your finesse game dead. She levels the match."
                $ _sets_lost += 1

    # --- Set 3 (if needed) ---
    if _sets_won < 2 and _sets_lost < 2:
        "[captain.display_name] bounces on her toes at the baseline. One set each — it all comes down to this."
        mc.name "Deciding set. No excuses."
        captain "Show me what you have got."

        menu:
            "Power serves — give absolutely everything" if mc.energy >= 15:
                python:
                    _set3_won, _cost3 = resolve_tennis_set("power", mc.energy, mc.focus, _cap_difficulty)
                    mc.change_energy(-_cost3)
                if _set3_won:
                    "You leave nothing in reserve. Your serve is unstoppable in the final set and you battle through to take it."
                    $ _sets_won += 1
                else:
                    "The tank runs dry at the worst moment. [captain.display_name] breaks through and closes out the match."
                    $ _sets_lost += 1
            "Power serves — {menu_red}Requires: 15 energy{/menu_red} (disabled)" if mc.energy < 15:
                pass
            "Steady baseline — stay calm and grind it out":
                python:
                    _set3_won, _cost3 = resolve_tennis_set("rally", mc.energy, mc.focus, _cap_difficulty)
                    mc.change_energy(-_cost3)
                if _set3_won:
                    "You grind every single point out. [captain.display_name] gives it everything but your consistency sees you through to the end."
                    $ _sets_won += 1
                else:
                    "[captain.display_name]'s experience shows when it matters most. She wins the deciding set."
                    $ _sets_lost += 1
            "Touch and angles — win it with your head":
                python:
                    _set3_won, _cost3 = resolve_tennis_set("finesse", mc.energy, mc.focus, _cap_difficulty)
                    mc.change_energy(-_cost3)
                if _set3_won:
                    "One perfectly placed drop shot seals it. [captain.display_name] watches the ball die and nods slowly."
                    $ _sets_won += 1
                else:
                    "[captain.display_name] stops falling for the angles. She outmuscles you through the third set and takes the match."
                    $ _sets_lost += 1

    # --- Match result ---
    if _sets_won > _sets_lost:
        $ captain.draw_person(emotion="sad")
        "[captain.display_name] walks to the net, breathing harder than usual, and extends her hand."
        captain "You beat me. I didn't expect that. Well played."
        mc.name "Good match, [captain.name]. You made me work for every point."
        "[captain.display_name] stands a little straighter, something shifting behind her eyes."
        $ captain.change_obedience(10)
        $ captain.change_happiness(-5)
        python:
            _prev_wins = captain.event_triggers_dict.get("mc_captain_wins", 0)
            captain.event_triggers_dict["mc_captain_wins"] = _prev_wins + 1
        if captain.event_triggers_dict["mc_captain_wins"] >= 3 and not captain.event_triggers_dict.get("captain_secretary_offered", False):
            call tennis_captain_secretary_offer(captain) from _call_tennis_captain_secretary_offer
    else:
        $ captain.draw_person(emotion="happy")
        "[captain.display_name] shakes your hand with a firm, satisfied grip."
        captain "Good effort. You have real potential — come back when you are sharper."
        mc.name "Next time, [captain.name]."
        $ mc.change_max_energy(2)
        "The hard match has pushed your limits slightly. You can feel your stamina improving."

    $ captain.draw_person(position="walking_away")
    return


# Triggered when MC has beaten the captain three times.
# The captain offers the MC the role of team secretary — gatekeeper for auditions.
label tennis_captain_secretary_offer(captain):
    $ captain.event_triggers_dict["captain_secretary_offered"] = True
    python:
        _cap_team = captain.event_triggers_dict.get("tennis_team", "perky")
        _team_labels = {"perky": "the Perky Team", "showoff": "the Showoff Team", "commando": "the Commando Team"}
        _tl = _team_labels[_cap_team]
    $ captain.draw_person(emotion="sad")
    "[captain.display_name] holds the handshake a beat longer than usual, studying your face."
    captain "Three times. I keep telling myself the next match will be different, and you keep proving me wrong."
    mc.name "You push me every time. It's a good match."
    captain "You're the best opponent I've faced on these courts. And you run a company on top of it all."
    "[captain.display_name] looks thoughtful for a moment."
    captain "I have a proposal for you. [_tl!c] needs a secretary — someone to handle administration, keep things running."
    captain "I'd like to offer you the position."

    menu:
        "What does the job involve?":
            $ captain.draw_person(emotion="happy")
            captain "As team secretary you're the gatekeeper. Anyone who wants to audition for a spot on the team has to go through you first."
            captain "You decide who gets to try out — and who doesn't."
            captain "It means every hopeful candidate needs your approval before they can step onto the court."
            "[captain.display_name] gives you a knowing look."
            captain "People will do a lot to get your attention when you hold that kind of power."
            menu:
                "Accept the position":
                    $ mc_team_secretary_team = _cap_team
                    $ captain.draw_person(emotion="happy")
                    mc.name "I like the sound of that. Count me in."
                    captain "Excellent. Welcome aboard. You'll meet candidates every time you're down at the courts."
                    captain "They'll come to you. Just decide who deserves a shot."
                    $ captain.change_happiness(10)
                    $ captain.change_obedience(5)
                "Decline":
                    mc.name "Interesting, but not for me right now."
                    captain "Fair enough. The offer's there if you change your mind."
                    "[captain.display_name] steps back, her expression carefully neutral."
        "Accept — sounds like a good fit." if mc_team_secretary_team is None:
            $ mc_team_secretary_team = _cap_team
            $ captain.draw_person(emotion="happy")
            mc.name "I'll take it. I could use a change of pace."
            captain "Great decision. You'll meet candidates whenever you're at the courts."
            $ captain.change_happiness(10)
            $ captain.change_obedience(5)
        "Not right now — I'll think about it.":
            mc.name "I'm not looking for extra commitments right now, but I'll keep it in mind."
            captain "Fair enough. You know where to find me."
            "[captain.display_name] steps back, her expression carefully neutral."
    return


# --- Meet Candidates (Team Secretary) ---
# When MC is team secretary, candidates approach at the courts wanting to audition.
# MC can approve, deny, or ask for a favour before granting approval.

label tennis_meet_candidate_label():
    python:
        _sec_team = mc_team_secretary_team
        _team_labels = {"perky": "the Perky Team", "showoff": "the Showoff Team", "commando": "the Commando Team"}
        _tl = _team_labels.get(_sec_team, "the team")

        _team_full = len(tennis_teams.get(_sec_team, [])) >= TENNIS_TEAM_MAX_MEMBERS

        # Generate a random candidate who fits the team profile.
        _team_specs = {
            "perky":    {"age_range": [18, 20], "sluttiness_range": [30, 55]},
            "showoff":  {"age_range": [21, 29], "sluttiness_range": [20, 45]},
            "commando": {"age_range": [30, 45], "sluttiness_range": [30, 55]},
        }
        _spec = _team_specs.get(_sec_team, {"age_range": [18, 30], "sluttiness_range": [20, 40]})
        _candidate = make_person(
            age_range=_spec["age_range"],
            sluttiness_range=_spec["sluttiness_range"],
            start_home=purgatory,
            type="random",
        )
        _candidate.like_women = renpy.random.randint(1, 5)
        _candidate.change_location(sports_center_tennis_courts)
        _candidate.apply_outfit(build_tennis_outfit(_candidate))
        _candidate.draw_person(emotion="happy")

    "While you're at the courts, a young woman in tennis gear approaches you."
    _candidate "Excuse me — are you the secretary for [_tl]?"
    mc.name "That's right. What can I do for you?"
    _candidate "I'm [_candidate.name]. I've been practising for months and I'd love a chance to audition for a spot on the team."
    _candidate "I heard you're the one who decides who gets to try out."

    if _team_full:
        mc.name "I'm afraid [_tl] is full right now. There are no open slots."
        _candidate "Oh... that's a shame. Could you let me know if anything opens up?"
        mc.name "I'll keep you in mind."
        "[_candidate.display_name] looks disappointed but nods politely and walks away."
        $ _candidate.draw_person(position="walking_away")
        return

    menu:
        "Approve her audition":
            mc.name "You look like you've put in the work. I'll approve your audition."
            $ _candidate.draw_person(emotion="happy")
            _candidate "Really? Thank you so much! I won't let you down."
            "You sign off on [_candidate.display_name]'s application."
            call tennis_audition_scene(_candidate, _sec_team) from _call_tennis_audition_secretary_approve
        "Deny her":
            mc.name "I don't think you're ready. Come back when you've improved."
            $ _candidate.draw_person(emotion="sad")
            _candidate "Oh... I understand. I'll keep working at it."
            "[_candidate.display_name] shoulders her bag and heads for the exit, clearly deflated."
            $ _candidate.change_happiness(-10)
            $ _candidate.draw_person(position="walking_away")
        "Persuade her to do you a favour first":
            mc.name "I have a lot of candidates to consider. You'd need to show me you're... committed."
            _candidate "Committed? What do you mean?"
            mc.name "Let's just say the secretary position comes with a lot of requests. If you can help me with something, I'll move your application to the top of the pile."
            if _candidate.sluttiness >= 30:
                $ _candidate.draw_person(emotion="happy")
                _candidate "I... suppose I can be flexible. What did you have in mind?"
                menu:
                    "Ask for a kiss":
                        mc.name "A kiss. Just to show me you're serious."
                        _candidate "That's... okay. I can do that."
                        $ _candidate.break_taboo("kissing")
                        $ _candidate.change_love(5)
                        $ _candidate.change_obedience(5)
                        "[_candidate.display_name] steps closer and presses her lips to yours. It lingers a beat longer than it needs to."
                        mc.name "Good. Your audition is approved."
                        call tennis_audition_scene(_candidate, _sec_team) from _call_tennis_audition_secretary_kiss
                    "Ask her to flash you":
                        mc.name "Show me what you've got under that tennis top. Quick — nobody's looking."
                        if _candidate.sluttiness >= 40:
                            _candidate "Fine... but only because I really want this."
                            "[_candidate.display_name] glances around, then lifts her top briefly."
                            $ _candidate.change_slut(3, 60)
                            $ _candidate.change_obedience(5)
                            $ mc.change_locked_clarity(5)
                            mc.name "That's the kind of dedication I like to see. You're approved."
                            call tennis_audition_scene(_candidate, _sec_team) from _call_tennis_audition_secretary_flash
                        else:
                            $ _candidate.draw_person(emotion="sad")
                            _candidate "I... no. That's too much. Sorry."
                            mc.name "Then I'm afraid I can't help you right now."
                            "[_candidate.display_name] looks away, embarrassed, and leaves."
                            $ _candidate.draw_person(position="walking_away")
                    "Never mind — just approve her":
                        mc.name "Actually, forget it. You seem dedicated enough. Go ahead."
                        _candidate "Thank you!"
                        call tennis_audition_scene(_candidate, _sec_team) from _call_tennis_audition_secretary_nevermind
            else:
                $ _candidate.draw_person(emotion="sad")
                _candidate "I'm not sure what you mean, but I just want to play tennis."
                mc.name "Then come back when you're ready to be more flexible."
                "[_candidate.display_name] shakes her head and walks off."
                $ _candidate.draw_person(position="walking_away")
    return


# --- Challenge a Team Member ---
# As team secretary the MC can challenge any member of their team to a best-of-one set.
# If the MC wins, they pick one of four rewards.
# If the member wins, she picks a random reward from the MC.

label challenge_member_label():
    python:
        _sec_team = mc_team_secretary_team
        _team_labels = {"perky": "the Perky Team", "showoff": "the Showoff Team", "commando": "the Commando Team"}
        _tl = _team_labels.get(_sec_team, "the team")
        _members = tennis_teams.get(_sec_team, [])
        _here = [p for p in _members if p in sports_center_tennis_courts.people]

    if not _here:
        "None of your team members are at the courts right now."
        return

    "You look around the courts for one of [_tl]'s members to challenge."

    call screen main_choice_display(build_menu_items(
        [get_sorted_people_list(_here, "Challenge a team member:", "Never mind")]))
    if not isinstance(_return, Person):
        return

    $ the_person = _return

    call tennis_member_match(the_person) from _call_tennis_member_match_outer
    $ mc.business.change_funds(-tennis_session_cost)
    "You pay for the court hire; $[tennis_session_cost] has been deducted from the company's credit card."
    call advance_time() from _call_advance_time_member_challenge
    return


# Single-set match against a team member with reward wagers.
label tennis_member_match(the_person):
    python:
        mc.change_location(sports_center_tennis_courts)
        if the_person not in sports_center_tennis_courts.people:
            the_person.change_location(sports_center_tennis_courts)
        the_person.apply_outfit(build_tennis_outfit(the_person))
        the_person.draw_person(emotion="happy")

        # Member difficulty is lower than captains — based on team tier.
        _mem_team = the_person.event_triggers_dict.get("tennis_team", mc_team_secretary_team)
        _mem_diff = {"perky": 0.20, "showoff": 0.30, "commando": 0.40}.get(_mem_team, 0.25)
        _mem_diff = max(0.10, min(0.60, _mem_diff))

    mc.name "Hey [the_person.name] — how about a friendly match? One set, but let's make it interesting."
    the_person "Interesting how?"
    mc.name "Loser has to do something for the winner. A little wager."

    if the_person.obedience >= 100 or the_person.sluttiness >= 30:
        $ the_person.draw_person(emotion="happy")
        the_person "You're on. I hope you're ready to pay up."
    else:
        the_person "Fine, but nothing too crazy."

    "You take your positions on opposite sides of the net."

    menu:
        "Power serves — overpower her" if mc.energy >= 15:
            python:
                _set_won, _cost = resolve_tennis_set("power", mc.energy, mc.focus, _mem_diff)
                mc.change_energy(-_cost)
            if _set_won:
                "Your serve is untouchable. [the_person.display_name] does her best but cannot return a single one."
            else:
                "[the_person.display_name] steps inside your delivery and punches it back with interest. She takes the set."
        "Power serves — {menu_red}Requires: 15 energy{/menu_red} (disabled)" if mc.energy < 15:
            $ _set_won = False
        "Steady baseline rally — grind her down":
            python:
                _set_won, _cost = resolve_tennis_set("rally", mc.energy, mc.focus, _mem_diff)
                mc.change_energy(-_cost)
            if _set_won:
                "You trade groundstrokes until [the_person.display_name] starts making mistakes. You close out the set."
            else:
                "[the_person.display_name]'s consistency outlasts yours. She takes the set with a smile."
        "Touch and angles — outthink her":
            python:
                _set_won, _cost = resolve_tennis_set("finesse", mc.energy, mc.focus, _mem_diff)
                mc.change_energy(-_cost)
            if _set_won:
                "Your placement keeps [the_person.display_name] wrong-footed at every turn. She can only shake her head."
            else:
                "[the_person.display_name] reads your angles and turns them against you. She wins the set convincingly."

    # --- Reward phase ---
    if _set_won:
        $ the_person.draw_person(emotion="sad")
        "[the_person.display_name] walks to the net, slightly out of breath."
        the_person "Okay, you won fair and square. What's my forfeit?"
        mc.name "Let me think..."

        menu:
            "A kiss":
                mc.name "A kiss. Right here on the court."
                if the_person.sluttiness >= 20 or the_person.obedience >= 100:
                    $ the_person.draw_person(emotion="happy")
                    the_person "A bet's a bet."
                    "[the_person.display_name] steps up and presses her lips to yours. It lasts a beat longer than it needs to."
                    $ the_person.break_taboo("kissing")
                    $ the_person.change_love(3)
                    $ the_person.change_obedience(3)
                else:
                    $ the_person.draw_person(emotion="sad")
                    the_person "That's... a bit much. But fine, a quick one."
                    "[the_person.display_name] gives you a brief, awkward kiss on the cheek."
                    $ the_person.change_obedience(2)

            "Her panties" if the_person.outfit.wearing_panties:
                mc.name "Your panties. Hand them over."
                if the_person.sluttiness >= 40 or the_person.obedience >= 120:
                    $ the_person.draw_person(emotion="happy")
                    the_person "Seriously? Fine... a deal's a deal."
                    "[the_person.display_name] glances around, then discretely slips off her panties and hands them to you."
                    $ the_person.outfit.remove_panties()
                    $ the_person.draw_person(emotion="happy")
                    $ the_person.change_slut(3, 60)
                    $ the_person.change_obedience(5)
                    $ mc.change_locked_clarity(5)
                else:
                    $ the_person.draw_person(emotion="sad")
                    the_person "No way! That's way too far."
                    mc.name "A bet's a bet, [the_person.name]."
                    the_person "Ugh... fine."
                    "[the_person.display_name] reluctantly hands over her panties, blushing furiously."
                    $ the_person.outfit.remove_panties()
                    $ the_person.draw_person(emotion="sad")
                    $ the_person.change_obedience(3)
                    $ mc.change_locked_clarity(3)

            "Her bra" if the_person.outfit.wearing_bra:
                mc.name "Your bra. Let's see you play the rest of practice without it."
                if the_person.sluttiness >= 50 or the_person.obedience >= 130:
                    $ the_person.draw_person(emotion="happy")
                    the_person "You're enjoying this, aren't you?"
                    "[the_person.display_name] reaches behind her back and pulls her bra out through her sleeve."
                    $ the_person.outfit.remove_bra()
                    $ the_person.draw_person(emotion="happy")
                    $ the_person.change_slut(5, 70)
                    $ the_person.change_obedience(5)
                    $ mc.change_locked_clarity(8)
                else:
                    $ the_person.draw_person(emotion="sad")
                    the_person "That is so not fair!"
                    mc.name "You agreed to the wager."
                    "[the_person.display_name] reluctantly removes her bra, arms crossed over her chest."
                    $ the_person.outfit.remove_bra()
                    $ the_person.draw_person(emotion="sad")
                    $ the_person.change_obedience(3)
                    $ mc.change_locked_clarity(5)

            "An upskirt photo":
                mc.name "I want a photo. A quick upskirt shot — just for me."
                if the_person.sluttiness >= 45 or the_person.obedience >= 125:
                    $ the_person.draw_person(emotion="happy")
                    the_person "You perv... okay, but just one."
                    "[the_person.display_name] lifts the hem of her tennis skirt just enough for you to snap a photo."
                    $ the_person.change_slut(4, 65)
                    $ the_person.change_obedience(5)
                    $ mc.change_locked_clarity(10)
                else:
                    $ the_person.draw_person(emotion="sad")
                    the_person "A photo?! That's really pushing it..."
                    mc.name "A bet's a bet."
                    "After a long pause, [the_person.display_name] reluctantly lifts her skirt just enough for a quick photo."
                    $ the_person.change_obedience(3)
                    $ mc.change_locked_clarity(6)
    else:
        # Member wins — she picks a random reward from the MC.
        $ the_person.draw_person(emotion="happy")
        "[the_person.display_name] beams as she walks to the net."
        the_person "I win! Time to pay up."

        python:
            _member_rewards = ["energy_drink", "massage", "kiss", "grope"]
            _reward = renpy.random.choice(_member_rewards)

        if _reward == "energy_drink":
            the_person "You owe me an energy drink. The good kind."
            mc.name "Fair enough. One sports drink, coming up."
            $ mc.business.change_funds(-5)
            $ the_person.change_happiness(5)
            "You buy [the_person.display_name] a drink from the vending machine."
        elif _reward == "massage":
            the_person "My shoulders are killing me. You owe me a quick massage."
            mc.name "I suppose I did agree to this."
            "You spend a few minutes rubbing [the_person.display_name]'s shoulders. She sighs happily."
            $ the_person.change_happiness(8)
            $ the_person.change_love(2)
        elif _reward == "kiss":
            the_person "I want a kiss. Right here, right now."
            mc.name "A bet's a bet..."
            "[the_person.display_name] steps close and presses her lips to yours. She pulls back with a satisfied grin."
            $ the_person.break_taboo("kissing")
            $ the_person.change_love(5)
            $ the_person.change_happiness(5)
            $ mc.change_locked_clarity(3)
        else:
            the_person "I get to cop a feel. Fair's fair."
            mc.name "I... didn't expect that."
            "[the_person.display_name] steps in and runs her hand across your chest, giving you a firm squeeze."
            the_person "Not bad. Maybe I should win more often."
            $ the_person.change_slut(2, 60)
            $ the_person.change_love(3)
            $ the_person.change_happiness(5)

    $ the_person.draw_person(position="walking_away")
    return
