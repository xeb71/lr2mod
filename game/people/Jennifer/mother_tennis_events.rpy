# Maximum number of non-captain members allowed per team.
# Each team can have 1 captain + TENNIS_TEAM_MAX_MEMBERS members = 6 players.
define TENNIS_TEAM_MAX_MEMBERS = 5

# These must use `default` (not `init python:`) so that Ren'Py saves and
# restores them correctly across saves and loads.
default perky_leader    = None
default showoff_leader  = None
default commando_leader = None

init python:
    def create_tennis_leaders():
        """Create the three tennis team captains and add them to the world.

        IMPORTANT: Captains must NOT start at purgatory.  ``is_available``
        returns False for anyone located in purgatory, which causes
        ``get_destination()`` to always return purgatory — trapping them
        there permanently.  Each captain gets a downtown apartment
        (generic_bedroom_1/2/3) as home and is scheduled at the tennis
        courts during early morning and morning on Tue–Sun.
        """
        # --- Perky Team leader: Zoe ---
        renpy.store.perky_leader = make_person(
            name="Zoe", last_name="Carter",
            age_range=[19, 20], body_type="standard_body",
            face_style="Face_2",
            tits="C", height=0.91,
            hair_colour=["blonde", [0.75, 0.65, 0.38, 0.95]], hair_style=ponytail,
            skin="white", eyes="blue",
            personality=wild_personality,
            name_color="#ff88cc", dial_color="#ff88cc",
            sluttiness=46, obedience=85, happiness=115, love=0,
            relationship="Single", kids=0,
            stat_array=[2, 3, 4], skill_array=[1, 2, 4, 2, 1], sex_skill_array=[2, 2, 2, 1],
            start_home=generic_bedroom_1,
            type="story",
        )
        renpy.store.perky_leader.like_women = 5
        renpy.store.perky_leader.event_triggers_dict["tennis_team"] = "perky"
        renpy.store.perky_leader.event_triggers_dict["tennis_captain"] = True
        renpy.store.perky_leader.set_opinion("taking control", 2)
        renpy.store.perky_leader.set_opinion("being submissive", -2)
        renpy.store.perky_leader.set_opinion("threesomes", 2)
        # day_slots [1-6] = Tuesday through Sunday (skip Monday=0); time_slots [0,1] = early morning, morning
        renpy.store.perky_leader.set_schedule(sports_center_tennis_courts, day_slots=[1, 2, 3, 4, 5, 6], time_slots=[0, 1])
        renpy.store.perky_leader.planned_outfit = build_tennis_outfit(renpy.store.perky_leader)
        generic_bedroom_1.add_person(renpy.store.perky_leader)
        write_log("[tennis] perky_leader (Zoe) created and scheduled at tennis courts Tue-Sun early morning/morning")

        # --- Showoff Team leader: Jade ---
        renpy.store.showoff_leader = make_person(
            name="Jade", last_name="Morrison",
            age_range=[24, 27], body_type="standard_body",
            face_style="Face_5",
            tits="D", height=0.93,
            hair_colour=["dark brown", [0.18, 0.12, 0.08, 0.95]], hair_style=messy_ponytail,
            skin="white", eyes="green",
            personality=wild_personality,
            name_color="#44aaff", dial_color="#44aaff",
            sluttiness=36, obedience=80, happiness=110, love=0,
            relationship="Single", kids=0,
            stat_array=[2, 4, 3], skill_array=[1, 3, 4, 2, 1], sex_skill_array=[3, 2, 2, 1],
            start_home=generic_bedroom_2,
            type="story",
        )
        renpy.store.showoff_leader.like_women = 5
        renpy.store.showoff_leader.event_triggers_dict["tennis_team"] = "showoff"
        renpy.store.showoff_leader.event_triggers_dict["tennis_captain"] = True
        renpy.store.showoff_leader.set_opinion("taking control", 2)
        renpy.store.showoff_leader.set_opinion("being submissive", -2)
        renpy.store.showoff_leader.set_opinion("threesomes", 2)
        # day_slots [1-6] = Tuesday through Sunday (skip Monday=0); time_slots [0,1] = early morning, morning
        renpy.store.showoff_leader.set_schedule(sports_center_tennis_courts, day_slots=[1, 2, 3, 4, 5, 6], time_slots=[0, 1])
        renpy.store.showoff_leader.planned_outfit = build_tennis_outfit(renpy.store.showoff_leader)
        generic_bedroom_2.add_person(renpy.store.showoff_leader)
        write_log("[tennis] showoff_leader (Jade) created and scheduled at tennis courts Tue-Sun early morning/morning")

        # --- Commando Team leader: Diana ---
        renpy.store.commando_leader = make_person(
            name="Diana", last_name="Novak",
            age_range=[33, 36], body_type="standard_body",
            face_style="Face_6",
            tits="DD", height=0.94,
            hair_colour=["black", [0.08, 0.06, 0.08, 0.95]], hair_style=short_hair,
            skin="white", eyes="brown",
            personality=reserved_personality,
            name_color="#aa55ff", dial_color="#aa55ff",
            sluttiness=46, obedience=75, happiness=108, love=0,
            relationship="Single", kids=0,
            stat_array=[3, 3, 3], skill_array=[2, 3, 3, 2, 1], sex_skill_array=[3, 3, 2, 1],
            start_home=generic_bedroom_3,
            type="story",
        )
        renpy.store.commando_leader.like_women = 5
        renpy.store.commando_leader.event_triggers_dict["tennis_team"] = "commando"
        renpy.store.commando_leader.event_triggers_dict["tennis_captain"] = True
        renpy.store.commando_leader.set_opinion("taking control", 2)
        renpy.store.commando_leader.set_opinion("being submissive", -2)
        renpy.store.commando_leader.set_opinion("threesomes", 2)
        # day_slots [1-6] = Tuesday through Sunday (skip Monday=0); time_slots [0,1] = early morning, morning
        renpy.store.commando_leader.set_schedule(sports_center_tennis_courts, day_slots=[1, 2, 3, 4, 5, 6], time_slots=[0, 1])
        renpy.store.commando_leader.planned_outfit = build_tennis_outfit(renpy.store.commando_leader)
        generic_bedroom_3.add_person(renpy.store.commando_leader)
        write_log("[tennis] commando_leader (Diana) created and scheduled at tennis courts Tue-Sun early morning/morning")

    def create_tennis_npc_members():
        """Pre-fill each team with 2 background NPC members."""
        teams = renpy.store.tennis_teams

        team_specs = {
            "perky":    {"age_range": [18, 20], "sluttiness_range": [40, 65]},
            "showoff":  {"age_range": [21, 29], "sluttiness_range": [30, 55]},
            "commando": {"age_range": [30, 45], "sluttiness_range": [40, 65]},
        }

        for team_key, specs in team_specs.items():
            if teams[team_key]:
                continue  # already populated
            for _ in range(2):
                npc = make_person(
                    age_range=specs["age_range"],
                    sluttiness_range=specs["sluttiness_range"],
                    start_home=purgatory,
                    type="random",
                )
                npc.like_women = renpy.random.randint(1, 5)
                npc.event_triggers_dict["tennis_team"] = team_key
                teams[team_key].append(npc)


label mom_tennis_sponsorship_label():
    # Morning setup: force mom to kitchen so the player can find her there.
    $ write_log("[tennis mom] mom_tennis_sponsorship_label fired: day=%s time_of_day=%s mom_location=%s sponsorship_done=%s", day, time_of_day, mom.location.name if mom.location else "None", mom.event_triggers_dict.get("tennis_sponsorship_done", False))
    $ mom.change_location(kitchen)
    # Add the actual conversation as a talk event so the yellow ! appears on mom.
    $ mom.add_unique_on_talk_event(
        Action("Mom asks about tennis sponsorship", mom_tennis_sponsorship_talk_requirement, "mom_tennis_sponsorship_talk_label", priority=30)
    )
    # Re-queue this morning-setup label for the next qualifying work morning.
    $ mc.business.add_mandatory_morning_crisis(
        Action("Mom asks about tennis sponsorship", mom_tennis_sponsorship_requirement, "mom_tennis_sponsorship_label")
    )
    return


label mom_tennis_sponsorship_talk_label(the_person):
    $ mc.change_location(kitchen)
    $ the_person.change_location(kitchen)
    $ the_person.draw_person(emotion = "happy")
    "[the_person.possessive_title!c] is up early this morning, making herself a coffee in the kitchen."
    the_person "Oh! Good morning, [the_person.mc_title]. You're up early."
    mc.name "Morning, [the_person.title]. Everything okay?"
    the_person "Yes, actually — I wanted to catch you before the day gets away from us."
    the_person "I've been thinking... you know how I used to play tennis back in the day?"
    mc.name "A little. You were pretty good, weren't you?"
    the_person "I was! Anyway, the local club is running a tournament series and I would really love to enter."
    the_person "The problem is, there's a membership and entry fee to join. It's $500."
    the_person "I know it's a lot to ask, but... would you consider sponsoring me?"
    # Create the tennis captains and NPC roster members the first time the
    # event fires, regardless of which answer the player picks.
    python:
        if perky_leader is None:
            create_tennis_leaders()
        if not tennis_teams["perky"] and not tennis_teams["showoff"] and not tennis_teams["commando"]:
            create_tennis_npc_members()
    menu:
        "Sponsor her ($500)":
            if not mc.business.has_funds(500):
                mc.name "I would love to, but I don't have the funds right now. Ask me again later."
                the_person "Oh, no worries at all. Thank you for considering it."
                return
            $ mc.business.change_funds(-500, stat = "Sponsorship")
            mc.name "Of course. You should go for it."
            the_person "Really?! Oh, [the_person.mc_title], thank you so much!"
            "[the_person.possessive_title!c] throws her arms around you with a big smile."
            the_person "I'm going to start practising Tuesday and Thursday mornings at the sports centre. You should come watch sometime!"
            mc.name "I'll try."
            $ setup_mom_tennis_schedule()
            $ the_person.event_triggers_dict["tennis_sponsorship_done"] = True
            $ the_person.change_love(3)
            $ the_person.change_happiness(10)
        "Maybe another time":
            mc.name "It's a bit much right now, [the_person.title]. Maybe another time."
            the_person "Oh... of course. No pressure."
            "[the_person.possessive_title!c] looks a little deflated, but nods."
            $ the_person.event_triggers_dict["tennis_sponsorship_done"] = True
    return


# --- Tennis Team Roster Data ---
# Tracks which Person objects have joined each team (captains are shown separately).
# Populated at runtime when a girl passes an audition.
default tennis_teams = {"perky": [], "showoff": [], "commando": []}

# The team key (e.g. "perky") the MC has been appointed secretary of, or None.
default mc_team_secretary_team = None


screen tennis_team_rosters():
    modal True
    zorder 100

    frame:
        background "#1a45a1aa"
        xalign 0.5
        yalign 0.35
        xsize 820
        padding (16, 16)

        vbox:
            spacing 8
            text "Tennis Team Rosters" xalign 0.5 size 28 style "menu_text_title_style"
            null height 4

            hbox:
                spacing 12
                xalign 0.5

                for _nb_team_key, _nb_team_label, _nb_captain in [
                    ("perky",    "The Perky Team",    perky_leader),
                    ("showoff",  "The Showoff Team",  showoff_leader),
                    ("commando", "The Commando Team", commando_leader),
                ]:
                    frame:
                        background "#09296faa"
                        xsize 252
                        padding (10, 10)
                        vbox:
                            spacing 5
                            text "[_nb_team_label]" xalign 0.5 size 20 style "menu_text_title_style"
                            null height 2
                            # Captain is always first on the roster.
                            if _nb_captain is not None:
                                $ _nb_cap_met = _nb_captain.event_triggers_dict.get("tennis_met", False)
                                if _nb_cap_met:
                                    # Discovered: full name in captain's colour
                                    $ _nb_cap_color = _nb_captain.char.who_args.get('color', '#ffffff')
                                    $ _nb_cap_display = _nb_captain.name + " " + _nb_captain.last_name
                                    if _nb_captain in sports_center_tennis_courts.people:
                                        text "{color=[_nb_cap_color]}[_nb_cap_display]{/color} {color=#ffd700}★ Captain{/color} {color=#4caf50}● here{/color}" style "menu_text_style"
                                    else:
                                        text "{color=[_nb_cap_color]}[_nb_cap_display]{/color} {color=#ffd700}★ Captain{/color}" style "menu_text_style"
                                else:
                                    # Undiscovered: first name only in white
                                    if _nb_captain in sports_center_tennis_courts.people:
                                        text "{color=#ffffff}[_nb_captain.name]{/color} {color=#ffd700}★ Captain{/color} {color=#4caf50}● here{/color}" style "menu_text_style"
                                    else:
                                        text "{color=#ffffff}[_nb_captain.name]{/color} {color=#ffd700}★ Captain{/color}" style "menu_text_style"
                            else:
                                text "{color=#888888}(No captain yet){/color}" style "menu_text_style"
                            for _nb_p in tennis_teams[_nb_team_key]:
                                $ _nb_p_met = _nb_p.event_triggers_dict.get("tennis_met", False)
                                if _nb_p_met:
                                    $ _nb_p_color = _nb_p.char.who_args.get('color', '#ffffff')
                                    $ _nb_p_display = _nb_p.name + " " + _nb_p.last_name
                                    if _nb_p in sports_center_tennis_courts.people:
                                        text "{color=[_nb_p_color]}[_nb_p_display]{/color} {color=#4caf50}● here{/color}" style "menu_text_style"
                                    else:
                                        text "{color=[_nb_p_color]}[_nb_p_display]{/color}" style "menu_text_style"
                                else:
                                    if _nb_p in sports_center_tennis_courts.people:
                                        text "{color=#ffffff}[_nb_p.name]{/color} {color=#4caf50}● here{/color}" style "menu_text_style"
                                    else:
                                        text "{color=#ffffff}[_nb_p.name]{/color}" style "menu_text_style"

            null height 8
            textbutton "Close" action Return() xalign 0.5 style "textbutton_style" text_style "menu_text_style"

    key "game_menu" action Return()


# --- Tennis Court Notice Board ---
# Fires during any tennis visit after the sponsorship event is complete.
# The scene shows the team roster noticeboard and (if playing with someone)
# offers an audition menu.

label tennis_noticeboard_scene(the_person=None):
    # the_person: Person object when called from a paired session (enables team auditions).
    # Pass None (default) when called from solo practice — the roster/notices are shown
    # but the audition menu is skipped because there is no NPC to audition.
    python:
        # Safety net: ensure captains and NPC members exist.
        if perky_leader is None:
            create_tennis_leaders()
        if not tennis_teams["perky"] and not tennis_teams["showoff"] and not tennis_teams["commando"]:
            create_tennis_npc_members()
        # Apply tennis outfits to everyone at the courts so they appear in
        # proper tennis attire rather than their daily planned outfit or gym clothes.
        for _nb_court_person in sports_center_tennis_courts.people:
            if _nb_court_person != mc:
                _nb_court_person.apply_outfit(build_tennis_outfit(_nb_court_person))
    "Near the entrance to the courts, a colourful notice board catches your eye."
    "Several flyers advertise women's social tennis teams looking for new members."
    menu:
        "Take a look":
            pass
        "View team rosters":
            call screen tennis_team_rosters()
        "Ignore it":
            return

    "You scan the notices. Three teams are advertising for players:"
    "The {b}Perky Team{/b} — 'Energetic young women wanted! We love the game and the social scene. Three courts reserved. Come say hi!'"
    "The {b}Showoff Team{/b} — 'Competitive women aged 21–29 who play to win and look good doing it. Three courts, big ambitions. New faces always welcome.'"
    "The {b}Commando Team{/b} — 'For serious, driven women aged 30 and over. Three dedicated courts, high intensity. Speak to the captain if you think you have what it takes.'"

    # Mark any captains currently at the courts as "discovered" by the MC.
    python:
        for _nb_disc_leader in [perky_leader, showoff_leader, commando_leader]:
            if _nb_disc_leader is not None and _nb_disc_leader in sports_center_tennis_courts.people:
                _nb_disc_leader.event_triggers_dict["tennis_met"] = True

    menu:
        "Check who has signed up":
            call screen tennis_team_rosters()
        "Continue":
            pass

    python:
        # Hidden qualification checks (like_women, age, sluttiness).
        # Perky: age ≤ 20, slut ≥ 40.  Showoff: 21-29, slut ≥ 30.  Commando: 30+, slut ≥ 40.
        if the_person is not None:
            _perky_ok    = (the_person.age <= 20       and the_person.like_women > 0 and the_person.sluttiness >= 40)
            _showoff_ok  = (21 <= the_person.age <= 29 and the_person.like_women > 0 and the_person.sluttiness >= 30)
            _commando_ok = (the_person.age >= 30       and the_person.like_women > 0 and the_person.sluttiness >= 40)
            _already_joined = the_person.event_triggers_dict.get("tennis_team") is not None

            # Special dress/equipment requirements for each team's audition.
            _perky_special_ok    = not the_person.wearing_bra
            _showoff_special_ok  = any(getattr(t, 'toy_type', None) == 'anal' for t in the_person.installed_toys)
            _commando_special_ok = not the_person.wearing_panties

            # Team capacity checks: each team is capped at TENNIS_TEAM_MAX_MEMBERS members.
            _perky_full    = len(tennis_teams["perky"])    >= TENNIS_TEAM_MAX_MEMBERS
            _showoff_full  = len(tennis_teams["showoff"])  >= TENNIS_TEAM_MAX_MEMBERS
            _commando_full = len(tennis_teams["commando"]) >= TENNIS_TEAM_MAX_MEMBERS
        else:
            _already_joined = True  # no NPC present — always skip the audition section

    if the_person is not None and not _already_joined:
        if _perky_ok or _showoff_ok or _commando_ok:
            "[the_person.possessive_title!c] lingers at the board, reading each notice carefully."
            the_person "These teams look interesting... I wonder how you get in?"
            mc.name "There is a notice about auditions — apparently you have to play a match against an existing member."
            the_person "An audition? That sounds like a challenge. I think I would like to try."

            menu:
                "Audition for the Perky Team" if _perky_ok and not _perky_full and _perky_special_ok:
                    call tennis_audition_scene(the_person, "perky") from _call_tennis_audition_perky
                "Audition for the Perky Team\n{menu_red}(Team is full — no open slots){/menu_red} (disabled)" if _perky_ok and _perky_full:
                    pass
                "Audition for the Perky Team\n{menu_red}(Not eligible right now){/menu_red} (disabled)" if _perky_ok and not _perky_full and not _perky_special_ok:
                    pass
                "Audition for the Showoff Team" if _showoff_ok and not _showoff_full and _showoff_special_ok:
                    call tennis_audition_scene(the_person, "showoff") from _call_tennis_audition_showoff
                "Audition for the Showoff Team\n{menu_red}(Team is full — no open slots){/menu_red} (disabled)" if _showoff_ok and _showoff_full:
                    pass
                "Audition for the Showoff Team\n{menu_red}(Not eligible right now){/menu_red} (disabled)" if _showoff_ok and not _showoff_full and not _showoff_special_ok:
                    pass
                "Audition for the Commando Team" if _commando_ok and not _commando_full and _commando_special_ok:
                    call tennis_audition_scene(the_person, "commando") from _call_tennis_audition_commando
                "Audition for the Commando Team\n{menu_red}(Team is full — no open slots){/menu_red} (disabled)" if _commando_ok and _commando_full:
                    pass
                "Audition for the Commando Team\n{menu_red}(Not eligible right now){/menu_red} (disabled)" if _commando_ok and not _commando_full and not _commando_special_ok:
                    pass
                "Not today":
                    "[the_person.possessive_title!c] pockets a contact slip, looking thoughtful."
    return


# Audition match. the_person tries to earn a spot on the chosen team.
# team_key is one of "perky", "showoff", "commando".
label tennis_audition_scene(the_person, team_key):
    # Safety guard: bail out silently if the team filled up since the menu was shown.
    if len(tennis_teams[team_key]) >= TENNIS_TEAM_MAX_MEMBERS:
        "[the_person.possessive_title!c] checks the notice board again — all slots for that team appear to have been filled."
        return
    python:
        _team_labels = {"perky": "the Perky Team", "showoff": "the Showoff Team", "commando": "the Commando Team"}
        _team_slut_gain = {"perky": 2, "showoff": 3, "commando": 4}
        _team_captain   = {"perky": perky_leader, "showoff": showoff_leader, "commando": commando_leader}

        _tl = _team_labels[team_key]
        _gain = _team_slut_gain[team_key]
        _captain = _team_captain[team_key]

        # Find an opponent: prefer a team member already at the courts, fall back to captain.
        _members_here = [p for p in tennis_teams[team_key] if p in sports_center_tennis_courts.people]
        _opponent = renpy.random.choice(_members_here) if _members_here else _captain

        # Make sure the captain is present (captains are scheduled Tue–Sun).
        if _opponent not in sports_center_tennis_courts.people:
            _opponent.change_location(sports_center_tennis_courts)

        # Apply tennis outfit to opponent so she appears in proper tennis attire.
        _opponent.apply_outfit(build_tennis_outfit(_opponent))
        _opponent.draw_person(emotion="happy")

    "[the_person.possessive_title!c] walks over to [_opponent.display_name], who is warming up on one of the three reserved courts."

    if _opponent is _captain:
        _opponent "[the_person.display_name]? I'm [_opponent.display_name] — I captain [_tl]. So you want to audition, do you?"
    else:
        _opponent "Oh, a new face! [_opponent.display_name]. Looking to audition? You've come to the right place."

    the_person "I would love a shot at joining. I'm ready when you are."
    _opponent "Then let's see what you've got. Three courts, plenty of room. Let's use court one."

    "You watch from the side as the two of them take up positions on opposite sides of the net."
    "The rally is fast and measured — [_opponent.display_name] testing [the_person.possessive_title] footwork, her timing, her composure."

    python:
        # Audition result: weighted by slut (higher slut → more comfortable → better chance).
        _slut_bonus = the_person.sluttiness / 100.0
        _pass_chance = 0.45 + (_slut_bonus * 0.35)   # ranges from 0.45 (slut=0) to 0.80 (slut=100)
        _audition_passed = renpy.random.random() < _pass_chance

    if _audition_passed:
        "[_opponent.display_name] lowers her racket and nods slowly, a smile playing at the corner of her mouth."
        _opponent "Good footwork. Good composure. I like what I see."
        the_person "Does that mean...?"
        _opponent "Welcome to [_tl]."
        "[the_person.possessive_title!c] breaks into a wide grin."
        $ the_person.event_triggers_dict["tennis_team"] = team_key
        $ tennis_teams[team_key].append(the_person)
        $ the_person.change_slut(_gain)
        call tennis_locker_room_scene(the_person, team_key, _opponent) from _call_tennis_locker_room
    else:
        "[_opponent.display_name] walks to the net, expression neutral but not unkind."
        _opponent "Not quite there yet. Your positioning needs work. Come back and try again any time."
        the_person "I'll keep practising."
        "[the_person.possessive_title!c] collects the ball and gives a determined nod."
    return


# Post-audition scene. The newly accepted member joins the team in the locker room.
label tennis_locker_room_scene(the_person, team_key, opponent):
    python:
        _team_labels = {"perky": "the Perky Team", "showoff": "the Showoff Team", "commando": "the Commando Team"}
        _tl = _team_labels[team_key]
        _members_here = [p for p in tennis_teams[team_key]
                         if p in sports_center_tennis_courts.people and p is not the_person and p is not opponent]

    $ mc.change_location(changing_room)
    $ the_person.change_location(changing_room)
    $ opponent.change_location(changing_room)

    "After the courts have been packed away, the team filters into the locker room."
    "Steam drifts from the showers. The air smells of sport and something warmer."

    opponent "Ladies — we have a new member. Everyone say hello to [the_person.display_name]."

    if _members_here:
        "The room offers a round of smiles and a few murmured hellos."
    else:
        opponent "It's just the two of us for now, but [_tl] is growing."
        the_person "I'm glad to be here."

    opponent "We meet here after every session. Rule one: what happens in the locker room stays in the locker room."
    the_person "Understood."

    if the_person.sluttiness > 50:
        opponent "I have a feeling you'll fit in just fine."
        "[the_person.possessive_title!c] glances around the steamy room with a small, knowing smile."
        $ the_person.change_stats(arousal = renpy.random.randint(5, 15))
    else:
        opponent "Get changed and I'll see you next session."

    $ mc.change_location(sports_center_tennis_courts)
    return
