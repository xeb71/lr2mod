# Cheating at Home Condition
# When the girl has a significant other and the MC is at her home,
# sex is considered cheating unless it is a planned session (appointment/date).
# The player picks a room to have sex in, each with different trade-offs.

init -1 python:
    def is_cheating_at_home(the_person):
        """Return True when the girl has a significant other and MC is
        at her home, unless it is a planned session (scheduled appointment
        or date with this person)."""
        if not the_person.has_significant_other:
            return False
        if not the_person.is_home:
            return False
        # If the MC has a planned appointment/date with this person right
        # now it is not considered cheating (they arranged it).
        current_appt = mc.schedule.get_appointment()
        if current_appt is not None and current_appt.person == the_person:
            return False
        return True

    def is_cheating_at_home_condition(condition):
        return isinstance(condition, Condition_Type) and condition.name.startswith("cheating_at_home_")

    def get_cheating_at_home_room_choice(condition):
        if not is_cheating_at_home_condition(condition):
            return getattr(condition, "cheating_room_choice", None)
        if hasattr(condition, "cheating_room_choice"):
            return condition.cheating_room_choice
        return condition.name.removeprefix("cheating_at_home_")

    def show_cheating_at_home_background(the_person, the_condition):
        room_choice = get_cheating_at_home_room_choice(the_condition)
        if room_choice == "bathroom":
            background_name = "Home_Bathroom_Background"
        elif room_choice == "kitchen":
            background_name = "Kitchen_Background"
        elif room_choice == "bedroom":
            background_name = the_person.bedroom.background_name
        else:
            return

        background = bg_manager.background(background_name)
        if background is not None:
            renpy.show(name = mc.location.name, what = background, layer = "master")

    def _standing_position_blacklist():
        """Return a list of positions that require standing (Stand or Lean)."""
        return [p for p in list_of_positions
                if p.requires_location in ("Stand", "Lean")]

    def make_cheating_at_home_condition(room_choice):
        """Build a Condition_Type for the chosen room.

        room_choice – one of "bathroom", "kitchen", "bedroom"
        """
        post = "cheating_at_home_post_" + room_choice

        blacklist = None

        cond = Condition_Type(
            "cheating_at_home_" + room_choice,
            pre_label = "cheating_at_home_pre_label",
            post_label=post,
            position_blacklist=blacklist,
        )
        # condition_vars[0]: bool – has already knocked/called once (doubled risk on second occurrence)
        cond.condition_vars.append(False)
        # condition_vars[1]: bool – bathroom/kitchen: sex scene should end (partner discovered or player stopped)
        cond.condition_vars.append(False)
        # condition_vars[2]: int – bathroom/kitchen: orgasm count seen at end of previous round
        cond.condition_vars.append(0)
        return cond


label cheating_at_home_pre_label(the_person, the_position, the_object, report_log, the_condition):
    $ show_cheating_at_home_background(the_person, the_condition)
    return


# ── Location choice label ────────────────────────────────────────────────
label cheating_at_home_room_choice(the_person):
    $ so_title = the_person.so_title
    the_person "My [so_title] is home, we have to be careful..."
    menu:
        "Where should we go?"

        "Bathroom {size=-4}(private but you have to be quiet){/size}":
            $ _cheating_room = "bathroom"
            the_person "The bathroom... at least we can lock the door."

        "Kitchen {size=-4}(partner may hear you – riskier if standing up){/size}":
            $ _cheating_room = "kitchen"
            the_person "The kitchen... just stay low and don't make a sound."

        "Bedroom {size=-4}(have to be quiet – 30%% chance he will discover us){/size}":
            $ _cheating_room = "bedroom"
            the_person "The bedroom... it's risky, but let's try to be quiet."
    return _cheating_room


# ── Bathroom: private but you have to be quiet ──────────────────────────
label cheating_at_home_post_bathroom(the_person, the_position, the_object, report_log, the_condition):
    # condition_vars[0]: already knocked once (False = first knock, True = second+ knock → doubled risk)
    # condition_vars[1]: sex scene should end (partner discovered or player chose to stop)
    # condition_vars[2]: orgasm count seen at end of previous round

    if the_condition.condition_vars[1]:
        return

    python:
        current_orgasms = report_log.get("girl orgasms", 0)
        _new_orgasm = current_orgasms > the_condition.condition_vars[2]
        the_condition.condition_vars[2] = current_orgasms

    if not _new_orgasm:
        # No new orgasm – ambient quiet flavour text
        $ rand_choice = renpy.random.randint(0, 2)
        if rand_choice == 0:
            "[the_person.title] bites her lip, trying hard not to make any noise."
        elif rand_choice == 1:
            "[the_person.title] whispers urgently, reminding you to keep it down."
        return

    # She just orgasmed – 50 % base chance her partner knocks (80 % if she's in a trance)
    $ _do_knock = renpy.random.random() < (0.8 if the_person.is_in_trance else 0.5)
    if not _do_knock:
        # She came quietly – relief flavour text
        $ rand_choice = renpy.random.randint(0, 1)
        if rand_choice == 0:
            "[the_person.title] trembles, biting down hard on her lip to muffle the sound."
        else:
            "[the_person.title] buries her face against you, muffling herself as she comes."
        return

    # Partner knocks
    $ so_title = the_person.so_title
    "Three sharp knocks land on the bathroom door."
    "[the_person.possessive_title!c] [so_title]'s muffled voice bleeds through the wood: \"[the_person.fname]? You've been in there a while — everything okay?\""
    $ the_person.draw_person(emotion = "scared")
    "[the_person.title] freezes, eyes wide, a hand pressed over her mouth."

    menu:
        "Keep going – stay quiet {size=-4}(risky){/size}":
            the_person "Almost done, give me a few minutes!"
            python:
                _knocked_before = the_condition.condition_vars[0]
                _tag = the_position.skill_tag
                if _tag == "Foreplay":
                    _base = 0.40
                elif _tag == "Oral":
                    _base = 0.50
                elif _tag == "Vaginal":
                    _base = 0.60
                elif _tag == "Anal":
                    _base = 0.70
                else:
                    _base = 0.50
                _discover_chance = min(_base * 1.5, 1.0) if _knocked_before else _base
                the_condition.condition_vars[0] = True  # mark that at least one knock has occurred
            $ so_caught = renpy.random.random() < _discover_chance

            if so_caught:
                "A moment later the handle rattles — then the door swings open."
                $ the_person.draw_person(emotion = "scared")
                "[the_person.possessive_title!c] [so_title] stands in the doorway, face draining of colour."
                the_person "[the_person.mc_title]—!"
                "Before anything else can happen, [the_person.possessive_title]'s [so_title] slams the door shut and you can hear heavy footsteps walking away."
                $ the_person.change_happiness(-5)
                $ the_person.change_love(-3)
                $ the_person.change_obedience(5, 200)
                $ the_condition.condition_vars[1] = True
                $ finished = True
            else:
                "[the_person.title] manages to hold completely still until the footsteps outside finally recede."
                if the_condition.condition_vars[0] and _knocked_before:
                    "[the_person.title] exhales shakily. \"That was the second time... we're pushing our luck.\""
                else:
                    "[the_person.title] lets out a shaky breath once she is sure [the_person.possessive_title] [so_title] has walked away."

        "Stop – play it safe":
            the_person "I'm coming now!"
            "[the_person.title] presses a finger to her lips and the two of you go completely still."
            "You can hear [the_person.possessive_title] [so_title] linger outside for a long moment before his footsteps finally move away."
            "[the_person.title] gives you a look that says everything — it's over for today."
            $ the_condition.condition_vars[1] = True
            $ finished = True
    return


# ── Kitchen: partner calls from the living room on orgasm ─────────────────
label cheating_at_home_post_kitchen(the_person, the_position, the_object, report_log, the_condition):
    # condition_vars[0]: partner has already called once (doubled risk on next call)
    # condition_vars[1]: sex scene should end (partner discovered or player stopped)
    # condition_vars[2]: orgasm count seen at end of previous round

    if the_condition.condition_vars[1]:
        return

    python:
        current_orgasms = report_log.get("girl orgasms", 0)
        _new_orgasm = current_orgasms > the_condition.condition_vars[2]
        the_condition.condition_vars[2] = current_orgasms

    if not _new_orgasm:
        # No new orgasm – ambient quiet flavour text
        $ rand_choice = renpy.random.randint(0, 2)
        if rand_choice == 0:
            "[the_person.title] tugs you lower, making sure neither of you can be seen above the counter."
        elif rand_choice == 1:
            "[the_person.title] freezes for a moment, listening for footsteps, before pulling you close again."
        return

    # She just orgasmed – 50 % base chance her partner calls (80 % if she's in a trance)
    $ _do_call = renpy.random.random() < (0.8 if the_person.is_in_trance else 0.5)
    if not _do_call:
        # She came quietly – relief flavour text
        $ rand_choice = renpy.random.randint(0, 1)
        if rand_choice == 0:
            "[the_person.title] buries her head against your chest, muffling herself as she comes."
        else:
            "[the_person.title] digs her nails into your arm, trembling silently through the wave."
        return

    # Partner calls from the living room
    $ so_title = the_person.so_title
    "[the_person.possessive_title!c] [so_title]'s voice drifts in from the living room: \"[the_person.fname]? You okay in there?\""
    $ the_person.draw_person(emotion = "scared")
    "[the_person.title] goes rigid, eyes darting toward the doorway."

    menu:
        "Keep going – stay low and quiet {size=-4}(risky){/size}":
            the_person "Almost done, give me a few minutes!"
            python:
                _called_before = the_condition.condition_vars[0]
                _loc = the_position.requires_location
                # Position-based discovery chance: standing is most visible
                if _loc in ("Stand", "Lean"):
                    _base = 0.65
                elif _loc in ("Low",):
                    _base = 0.40
                else:  # Kneel, Sit, Lay, Swing – well below counter level
                    _base = 0.25
                _discover_chance = min(_base * 1.5, 1.0) if _called_before else _base
                the_condition.condition_vars[0] = True  # mark at least one call has occurred
            $ so_caught = renpy.random.random() < _discover_chance

            if so_caught:
                "[the_person.possessive_title!c] [so_title]'s footsteps grow louder as he steps into the kitchen doorway."
                $ the_person.draw_person(emotion = "scared")
                the_person "[the_person.mc_title]—!"
                "[the_person.possessive_title!c] [so_title] sees you both and goes pale. He turns and walks back out without a word."
                $ the_person.change_happiness(-5)
                $ the_person.change_love(-3)
                $ the_person.change_obedience(5, 200)
                $ the_condition.condition_vars[1] = True
                $ finished = True
            else:
                if the_position.requires_location in ("Stand", "Lean"):
                    "[the_person.title] yanks you both down behind the counter just in time as [the_person.possessive_title] [so_title]'s voice falls silent."
                else:
                    "[the_person.title] holds her breath, pressed low, until [the_person.possessive_title] [so_title] gives up and goes quiet."
                if the_condition.condition_vars[0] and _called_before:
                    "[the_person.title] exhales shakily. \"That was the second time... we're really pushing our luck.\""
                else:
                    "[the_person.title] lets out a silent breath of relief once the living room falls quiet again."

        "Stop – play it safe":
            the_person "I'm coming now!"
            "[the_person.title] grabs your arm and shakes her head, mouthing 'stop'."
            "You both freeze until [the_person.possessive_title] [so_title]'s voice fades back into the living room."
            "[the_person.title] gives you an apologetic look. It's over for today."
            $ the_condition.condition_vars[1] = True
            $ finished = True
    return


# ── Bedroom: quiet, 30 % discovery each round ───────────────────────────
label cheating_at_home_post_bedroom(the_person, the_position, the_object, report_log, the_condition):
    if the_condition.condition_vars[0]:
        return
    $ rand_choice = renpy.random.randint(0, 2)
    if rand_choice == 0:
        "[the_person.title] moans softly into the pillow, trying to stay quiet."
    elif rand_choice == 1:
        "[the_person.title] grips the sheets tightly, stifling a gasp."

    # 30 % chance per round the partner discovers them
    if renpy.random.random() < 0.30:
        $ the_condition.condition_vars[0] = True
        $ so_title = the_person.so_title
        "Suddenly the bedroom door swings open."
        "[the_person.title]'s [so_title] stands in the doorway, eyes wide."
        the_person "[the_person.mc_title]! He's here!"
        "Before either of you can react, [the_person.possessive_title]'s [so_title] storms out of the room."
        $ the_person.change_happiness(-5)
        $ the_person.change_love(-3)
        $ the_person.change_obedience(5, 200)
    return
