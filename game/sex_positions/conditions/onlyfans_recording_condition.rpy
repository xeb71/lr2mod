#Use this for recording a onlyfans session.

init -1 python:
    def condition_onlyfans_recording_reward_req(self, the_person, report_log):
        if report_log.get("guy orgasms", 0) > 0:   #She finished off MC
            return True
        return False

    def get_onlyfans_recording_income(the_person, report_log):
        income = 25 * (report_log.get("girl orgasms", 0) + 1)
        if the_person.is_pregnant:
            income *= 2
        if report_log.get("girl squirts", 0) > 0:
            income *= 2
        return income


    def make_condition_onlyfans_recording(room_choice = None):
        onlyfans_recording_blacklist = [anal_swing, missionary, breeding_missionary, doggy_anal_dildo_dp, piledriver_anal, piledriver_dp, spanking, standing_dildo, against_wall, kissing, piledriver, standing_grope]  #We should blacklist any position that would require both of MC's hands
        pre_label = "condition_onlyfans_recording_pre_label"
        post_label = "condition_onlyfans_recording_post_label"

        if room_choice:
            pre_label = "condition_onlyfans_recording_cheating_pre_label"
            post_label = f"condition_onlyfans_recording_cheating_post_{room_choice}"

        onlyfans_recording_condition = Condition_Type("OnlyFans Recording",
            pre_label = pre_label,
            post_label = post_label,
            position_blacklist = onlyfans_recording_blacklist,
            reward_cond = condition_onlyfans_recording_reward_req,
            reward_label = "condition_onlyfans_recording_reward_label")
        onlyfans_recording_condition.condition_vars.append(False) #Initialize this to false so in the first pre label we can mention getting the phone camera ready
        onlyfans_recording_condition.condition_vars.append(0)     #Female orgasms
        onlyfans_recording_condition.condition_vars.append(0)     #Male orgasms
        if room_choice:
            onlyfans_recording_condition.cheating_room_choice = room_choice
            onlyfans_recording_condition.condition_vars.append(False) # Partner has already interrupted once / bedroom discovery happened
            onlyfans_recording_condition.condition_vars.append(False) # Bathroom/kitchen: sex scene should end
            onlyfans_recording_condition.condition_vars.append(0)     # Bathroom/kitchen: orgasm count seen for cheating checks
        return onlyfans_recording_condition


label condition_onlyfans_recording_pre_label(the_person, the_position, the_object, report_log, the_condition):
    if the_condition.condition_vars[0]:
        "You check the phone, trying to make sure you are keeping the action in view while you [the_position.verb] [the_person.title]."
    else:
        mc.name "Here, let me see your phone. I'll take an OnlyFans video while I'm [the_position.verbing] you."
        the_person "Okay."
        "[the_person.title] gets out her phone, unlocks it, and loads up the OnlyFans app before handing it to you."
        mc.name "Alright, recording! Let's do this."
        $ the_condition.condition_vars[0] = True
    return

label condition_onlyfans_recording_post_label(the_person, the_position, the_object, report_log, the_condition):
    if report_log.get("girl orgasms", 0) > the_condition.condition_vars[1] and report_log.get("guy orgasms", 0) > the_condition.condition_vars[2]:  #you finished together
        "You aren't sure if you managed to keep the finale in focus, but you're sure the sounds of [the_person.title] cumming with you were hot."
        "You stop [the_position.verbing] her for a moment to make sure you capture the aftermath of your orgasm."
    elif report_log.get("girl orgasms", 0) > the_condition.condition_vars[1]: #she orgasmed
        "You keep [the_position.verbing] her, keeping her in frame as she cums for the video."
    elif report_log.get("guy orgasms", 0) > the_condition.condition_vars[2]:
        "You stop [the_position.verbing] her for a moment to make sure you capture the aftermath of your orgasm."
    $ the_condition.condition_vars[1] = report_log.get("girl orgasms", 0)
    $ the_condition.condition_vars[2] = report_log.get("guy orgasms", 0)
    return

label condition_onlyfans_recording_cheating_pre_label(the_person, the_position, the_object, report_log, the_condition):
    $ show_cheating_at_home_background(the_person, the_condition)
    if the_condition.condition_vars[0]:
        "You check the phone, trying to make sure you are keeping the action in view while you [the_position.verb] [the_person.title]."
    else:
        mc.name "Here, let me see your phone. I'll take an OnlyFans video while I'm [the_position.verbing] you."
        the_person "Okay."
        "[the_person.title] gets out her phone, unlocks it, and loads up the OnlyFans app before handing it to you."
        mc.name "Alright, recording! Let's do this."
        $ the_condition.condition_vars[0] = True
    return

label condition_onlyfans_recording_cheating_post_bathroom(the_person, the_position, the_object, report_log, the_condition):
    if report_log.get("girl orgasms", 0) > the_condition.condition_vars[1] and report_log.get("guy orgasms", 0) > the_condition.condition_vars[2]:
        "You aren't sure if you managed to keep the finale in focus, but you're sure the sounds of [the_person.title] cumming with you were hot."
        "You stop [the_position.verbing] her for a moment to make sure you capture the aftermath of your orgasm."
    elif report_log.get("girl orgasms", 0) > the_condition.condition_vars[1]:
        "You keep [the_position.verbing] her, keeping her in frame as she cums for the video."
    elif report_log.get("guy orgasms", 0) > the_condition.condition_vars[2]:
        "You stop [the_position.verbing] her for a moment to make sure you capture the aftermath of your orgasm."
    $ the_condition.condition_vars[1] = report_log.get("girl orgasms", 0)
    $ the_condition.condition_vars[2] = report_log.get("guy orgasms", 0)

    if the_condition.condition_vars[4]:
        return

    python:
        current_orgasms = report_log.get("girl orgasms", 0)
        _new_orgasm = current_orgasms > the_condition.condition_vars[5]
        the_condition.condition_vars[5] = current_orgasms

    if not _new_orgasm:
        $ rand_choice = renpy.random.randint(0, 2)
        if rand_choice == 0:
            "[the_person.title] bites her lip, trying hard not to make any noise."
        elif rand_choice == 1:
            "[the_person.title] whispers urgently, reminding you to keep it down."
        return

    $ _do_knock = renpy.random.random() < (0.8 if the_person.is_in_trance else 0.5)
    if not _do_knock:
        $ rand_choice = renpy.random.randint(0, 1)
        if rand_choice == 0:
            "[the_person.title] trembles, biting down hard on her lip to muffle the sound."
        else:
            "[the_person.title] buries her face against you, muffling herself as she comes."
        return

    $ so_title = the_person.so_title
    "Three sharp knocks land on the bathroom door."
    "[the_person.possessive_title!c] [so_title]'s muffled voice bleeds through the wood: \"[the_person.fname]? You've been in there a while — everything okay?\""
    $ the_person.draw_person(emotion = "scared")
    "[the_person.title] freezes, eyes wide, a hand pressed over her mouth."

    menu:
        "Keep going – stay quiet {size=-4}(risky){/size}":
            the_person "Almost done, give me a few minutes!"
            python:
                _knocked_before = the_condition.condition_vars[3]
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
                the_condition.condition_vars[3] = True
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
                $ the_condition.condition_vars[4] = True
                $ finished = True
            else:
                "[the_person.title] manages to hold completely still until the footsteps outside finally recede."
                if _knocked_before:
                    "[the_person.title] exhales shakily. \"That was the second time... we're pushing our luck.\""
                else:
                    "[the_person.title] lets out a shaky breath once she is sure [the_person.possessive_title] [so_title] has walked away."

        "Stop – play it safe":
            the_person "I'm coming now!"
            "[the_person.title] presses a finger to her lips and the two of you go completely still."
            "You can hear [the_person.possessive_title] [so_title] linger outside for a long moment before his footsteps finally move away."
            "[the_person.title] gives you a look that says everything — it's over for today."
            $ the_condition.condition_vars[4] = True
            $ finished = True
    return

label condition_onlyfans_recording_cheating_post_kitchen(the_person, the_position, the_object, report_log, the_condition):
    if report_log.get("girl orgasms", 0) > the_condition.condition_vars[1] and report_log.get("guy orgasms", 0) > the_condition.condition_vars[2]:
        "You aren't sure if you managed to keep the finale in focus, but you're sure the sounds of [the_person.title] cumming with you were hot."
        "You stop [the_position.verbing] her for a moment to make sure you capture the aftermath of your orgasm."
    elif report_log.get("girl orgasms", 0) > the_condition.condition_vars[1]:
        "You keep [the_position.verbing] her, keeping her in frame as she cums for the video."
    elif report_log.get("guy orgasms", 0) > the_condition.condition_vars[2]:
        "You stop [the_position.verbing] her for a moment to make sure you capture the aftermath of your orgasm."
    $ the_condition.condition_vars[1] = report_log.get("girl orgasms", 0)
    $ the_condition.condition_vars[2] = report_log.get("guy orgasms", 0)

    if the_condition.condition_vars[4]:
        return

    python:
        current_orgasms = report_log.get("girl orgasms", 0)
        _new_orgasm = current_orgasms > the_condition.condition_vars[5]
        the_condition.condition_vars[5] = current_orgasms

    if not _new_orgasm:
        $ rand_choice = renpy.random.randint(0, 2)
        if rand_choice == 0:
            "[the_person.title] tugs you lower, making sure neither of you can be seen above the counter."
        elif rand_choice == 1:
            "[the_person.title] freezes for a moment, listening for footsteps, before pulling you close again."
        return

    $ _do_call = renpy.random.random() < (0.8 if the_person.is_in_trance else 0.5)
    if not _do_call:
        $ rand_choice = renpy.random.randint(0, 1)
        if rand_choice == 0:
            "[the_person.title] buries her head against your chest, muffling herself as she comes."
        else:
            "[the_person.title] digs her nails into your arm, trembling silently through the wave."
        return

    $ so_title = the_person.so_title
    "[the_person.possessive_title!c] [so_title]'s voice drifts in from the living room: \"[the_person.fname]? You okay in there?\""
    $ the_person.draw_person(emotion = "scared")
    "[the_person.title] goes rigid, eyes darting toward the doorway."

    menu:
        "Keep going – stay low and quiet {size=-4}(risky){/size}":
            the_person "Almost done, give me a few minutes!"
            python:
                _called_before = the_condition.condition_vars[3]
                _loc = the_position.requires_location
                if _loc in ("Stand", "Lean"):
                    _base = 0.65
                elif _loc in ("Low",):
                    _base = 0.40
                else:
                    _base = 0.25
                _discover_chance = min(_base * 1.5, 1.0) if _called_before else _base
                the_condition.condition_vars[3] = True
            $ so_caught = renpy.random.random() < _discover_chance

            if so_caught:
                "[the_person.possessive_title!c] [so_title]'s footsteps grow louder as he steps into the kitchen doorway."
                $ the_person.draw_person(emotion = "scared")
                the_person "[the_person.mc_title]—!"
                "[the_person.possessive_title!c] [so_title] sees you both and goes pale. He turns and walks back out without a word."
                $ the_person.change_happiness(-5)
                $ the_person.change_love(-3)
                $ the_person.change_obedience(5, 200)
                $ the_condition.condition_vars[4] = True
                $ finished = True
            else:
                if the_position.requires_location in ("Stand", "Lean"):
                    "[the_person.title] yanks you both down behind the counter just in time as [the_person.possessive_title] [so_title]'s voice falls silent."
                else:
                    "[the_person.title] holds her breath, pressed low, until [the_person.possessive_title] [so_title] gives up and goes quiet."
                if _called_before:
                    "[the_person.title] exhales shakily. \"That was the second time... we're really pushing our luck.\""
                else:
                    "[the_person.title] lets out a silent breath of relief once the living room falls quiet again."

        "Stop – play it safe":
            the_person "I'm coming now!"
            "[the_person.title] grabs your arm and shakes her head, mouthing 'stop'."
            "You both freeze until [the_person.possessive_title] [so_title]'s voice fades back into the living room."
            "[the_person.title] gives you an apologetic look. It's over for today."
            $ the_condition.condition_vars[4] = True
            $ finished = True
    return

label condition_onlyfans_recording_cheating_post_bedroom(the_person, the_position, the_object, report_log, the_condition):
    if report_log.get("girl orgasms", 0) > the_condition.condition_vars[1] and report_log.get("guy orgasms", 0) > the_condition.condition_vars[2]:
        "You aren't sure if you managed to keep the finale in focus, but you're sure the sounds of [the_person.title] cumming with you were hot."
        "You stop [the_position.verbing] her for a moment to make sure you capture the aftermath of your orgasm."
    elif report_log.get("girl orgasms", 0) > the_condition.condition_vars[1]:
        "You keep [the_position.verbing] her, keeping her in frame as she cums for the video."
    elif report_log.get("guy orgasms", 0) > the_condition.condition_vars[2]:
        "You stop [the_position.verbing] her for a moment to make sure you capture the aftermath of your orgasm."
    $ the_condition.condition_vars[1] = report_log.get("girl orgasms", 0)
    $ the_condition.condition_vars[2] = report_log.get("guy orgasms", 0)

    if the_condition.condition_vars[3]:
        return
    $ rand_choice = renpy.random.randint(0, 2)
    if rand_choice == 0:
        "[the_person.title] moans softly into the pillow, trying to stay quiet."
    elif rand_choice == 1:
        "[the_person.title] grips the sheets tightly, stifling a gasp."

    if renpy.random.random() < 0.30:
        $ the_condition.condition_vars[3] = True
        $ so_title = the_person.so_title
        "Suddenly the bedroom door swings open."
        "[the_person.title]'s [so_title] stands in the doorway, eyes wide."
        the_person "[the_person.mc_title]! He's here!"
        "Before either of you can react, [the_person.possessive_title]'s [so_title] storms out of the room."
        $ the_person.change_happiness(-5)
        $ the_person.change_love(-3)
        $ the_person.change_obedience(5, 200)
    return

label condition_onlyfans_recording_reward_label(the_person, report_log, the_condition):
    $ video_income = get_onlyfans_recording_income(the_person, report_log)
    $ mc_video_income = video_income // 2
    $ girl_video_income = video_income - mc_video_income
    $ mc.business.change_funds(mc_video_income, stat = "OnlyFanatics")
    $ the_person.change_stats(slut = 2, max_slut = 80, obedience = 3)
    "[the_person.possessive_title!c] seems pleased she managed to get you off during the video."
    "The video should pull in about $[video_income:,.0f] from her OnlyFanatics subscribers."
    "She keeps $[girl_video_income:,.0f], and your cut is $[mc_video_income:,.0f]."
    if report_log.get("girl orgasms", 0) > 5:
        mc.name "You earned every dollar of that. A performance like that is going to keep your subscribers very happy."
    return
