# Camila and Nora teamup scenes.

label camila_nora_goal_sync_setup_label(the_person):
    $ the_person = camila
    $ the_person.draw_person()
    mc.name "You've helped me rethink business goals and personal goals. Ever compare notes with anyone who does the same thing from a more academic angle?"
    the_person "Hmm... not really. Why?"
    mc.name "Because I know someone who is very good at turning big ambitions into concrete milestones."
    the_person "That does sound useful. Sometimes I can motivate people all day, but a really structured brain helps keep the plan from getting fuzzy."
    mc.name "Nora. She used to be one of my professors. Want me to set up coffee with her?"
    the_person "A professor and a coach at the same table? Ay, that could either be wonderful or exhausting."
    mc.name "With me there, probably both."
    $ the_person.change_happiness(3)
    the_person "Then yes. Set it up."
    "You text Nora and get a quick answer back. She is curious enough to agree to an afternoon coffee."
    $ camila.event_triggers_dict["nora_goal_teamup_scheduled"] = True
    $ add_camila_nora_goal_sync_intro_action()
    return

label camila_nora_goal_sync_intro_label():
    $ scene_manager = Scene()
    $ mc.change_location(coffee_shop)
    "That afternoon, you meet [camila.possessive_title] and [nora.title] at a coffee shop."
    $ scene_manager.add_actor(camila, position = "sitting")
    $ scene_manager.add_actor(nora, display_transform = character_center_flipped, position = "sitting")
    nora "So this is the lifestyle coach I've heard about."
    camila "And you are the professor who teaches him how to put everything in little boxes."
    mc.name "I feel very seen right now."
    "The two women share an amused look and settle in."
    camila "My whole thing is momentum. Get someone excited, get them moving, help them believe they can actually change."
    nora "Useful. My bias is toward systems. Motivation fades. Structure catches you when it does."
    camila "See? That's exactly why I wanted this."
    "For the next half hour they trade notes while you mostly listen."
    nora "Short-term goals should prove to the client that progress is real."
    camila "And the emotional win matters just as much as the checklist."
    nora "Agreed. If the plan feels punishing, people stop trusting it."
    $ camila.change_happiness(5)
    $ nora.change_happiness(3)
    "By the time the drinks are half-finished, the conversation has turned from theory to collaboration."
    camila "I should steal that milestone idea."
    nora "Borrow it. In exchange, you can teach me how you get people to stop psyching themselves out before they begin."
    mc.name "I was hoping you two would get along."
    camila "Oh, we do. She is intense, but in a fun way."
    nora "And she understands people better than most of the administrators I deal with."
    "It is not a flashy teamup, but it clicks immediately. Camila leaves with sharper tools for her coaching, and Nora leaves genuinely interested in how Camila reaches people."
    python:
        camila.event_triggers_dict["nora_goal_teamup_intro"] = True
        camila.event_triggers_dict["nora_goal_teamup_scheduled"] = False
        scene_manager.clear_scene()
        mc.change_location(downtown)
    return
