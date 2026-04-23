#Camila Teamups.

#planned teamups: Alexia is her main teamup. Starts with taking boudoir photos for her hubby, can end up taking them for MC
#If MC corrupts Camila AND Alexia, have the option to have them both leave their SOs for MC at the same time.
#Alexia explores hotwifey lifestyle during team up. MC and encourage or discourage it.

#Boudoir photo stages:
# 1 - Sexy photos of both girls, Camila talks a bit about hotwife lifestyle if alexia is dating
# 2 - Sexy photos. Ends with Camila taking deepthroat, alexia disbelief she would "cheat". Give MC option to encourage hotwifing or encourage alexia to keep it secret.
# 3 - transition to 3 is decision time. Alexia gets turned on and blows MC. MC can start exerting pressure on her (you're mine while you're here) or encourage sharing
# 4 - Full on threesome. If MC exerting, girls talk about enjoying their MC time. If hotwifing, girls talk about getting reclaimed.
# 5 - Exerting - Convince girls to dump their SOs, commit to you. If hotwifing, option to have SOs watch the photo shoot.


# camila_alexia_boudoir_final_setup
# camila_alexia_boudoir_intro
# camila_alexia_boudoir_recur

#Labels

label camila_alexia_boudoir_setup_reminder_label():
    "While working in your office, you start daydreaming about some of your recent sexual adventures."
    "Suddenly, you remember [camila.possessive_title], and your conversation about taking boudoir photos of her when you helped her pickup out some lingerie."
    "Recently, you purchased a camera and have started taking pictures with [alexia.title]. Maybe you could talk to her about doing them?"
    $ camila_alexia_boudoir_intro_setup()
    return

label camila_alexia_boudoir_setup_intro_label(the_person):
    mc.name "Hey [the_person.title]. Have a moment?"
    the_person "Uhh, sure [the_person.mc_title]."
    mc.name "You know how we take pictures of your for the ads to run, right?"
    the_person "Uhhh... yeah... hard to forget that..."
    mc.name "Well, I have a friend that I think would make a really good model. I was wondering if you would be willing to stay late one night and help me shoot some."
    the_person "Oh, like as the photographer?"
    mc.name "Exactly. I'd pay you overtime for it, of course."
    $ the_person.change_obedience(1)
    the_person "Oh man. I could really use the extra cash. What night were you thinking?"
    mc.name "I was thinking about Wednesday evenings, right after we close down."
    the_person "Okay. Are the pictures... are they going to be as risqué as the ones I did?"
    mc.name "Definitely. Actually, they are kind of a favour to her, too. She wants to get some boudoir style pictures for her husband."
    the_person "Oh! She's married? And she's okay with... and he's okay with it too?"
    mc.name "He is actually very supportive."
    the_person "Okay. I'll do it. Just let me know what day you want to start, okay?"
    mc.name "Perfect. I'll talk to her and get back to you."
    $ clear_scene()
    "You let [the_person.title] go. You should talk to [camila.title] and get the photoshoot finalized!"
    $ camila.add_unique_on_talk_event(camila_alexia_boudoir_final_setup)
    return

label camila_alexia_boudoir_final_setup_label(the_person):
    mc.name "Hey [the_person.title]. Guess what!"
    the_person "What?"
    if (day % 7 != 2):
        mc.name "I have a photoshoot scheduled for you on Wednesday night."
    else:
        mc.name "I have a photoshoot schedule for you tonight!"
    $ the_person.change_happiness(5)
    the_person "Oh wow! That's incredible!"
    mc.name "Let me get you the address. It'll be at my business, and one of my marketing people will be doing the pictures with me."
    the_person "Sounds great!"
    "You give [the_person.possessive_title] the information on your business location and the timing."
    the_person "Okay, I'll be there! And I've got just the outfit for it!"
    $ the_person.draw_person(position = "kissing")
    "[the_person.title] throws her arms around you and gives you a peck on the cheek."
    $ the_person.draw_person()
    the_person "See you there!"
    $ clear_scene()
    "Alright! You've got the time and place set for a sexy photoshoot!"
    $ camila.event_triggers_dict["boudoir_scheduled"] = True
    $ mc.business.add_mandatory_crisis(camila_alexia_boudoir_intro)
    return

label camila_alexia_boudoir_intro_label():
    $ scene_manager = Scene()
    "It's Wednesday. The boudoir photoshoot with [camila.possessive_title] and [alexia.title] is tonight!"
    if mc.is_at_office:
        "You finish up quickly with the last of your daily tasks before going to your office."
    else:
        "You head back to work and to your office to get ready."
    $ mc.change_location(ceo_office)
    "Shortly after, you hear a knock on your door."
    $ scene_manager.add_actor(alexia)
    alexia "Knock knock! Hey [alexia.mc_title]."
    "In her hands she has the company camera."
    mc.name "Come in! Thanks for staying late for this."
    alexia "No problem. Honestly, I'm kind of curious about your mystery married model."
    "A second knock comes a minute later."
    $ scene_manager.add_actor(camila, display_transform = character_center_flipped, position = "stand4")
    camila "Hola... I hope I'm not late."
    mc.name "Perfect timing."
    "Camila steps fully into the office wearing a lingerie set under a light summer wrap. Alexia gives her a quick once-over, but the smile she offers is warm instead of competitive."
    alexia "You must be Camila. I'm Alexia. Don't worry, we've all had a first shoot."
    camila "That obvious, huh?"
    alexia "Only because you're doing the same thing I did. You're thinking about how you look instead of how the camera sees you."
    $ scene_manager.update_actor(alexia, position = "stand2")
    "[alexia.title] steps close and gently adjusts the drape of [camila.possessive_title]'s wrap, then tips her chin up."
    alexia "There. Long neck, shoulders back, let your hips do the work."
    $ scene_manager.update_actor(camila, position = "back_peek")
    "Camila follows the directions. The nervousness is still there, but now it mixes with excitement."
    mc.name "That's it. Hold that."
    "You take a run of pictures while Alexia keeps offering quiet pointers."
    alexia "Now give him a look like you know exactly what you're doing to him."
    $ scene_manager.update_actor(camila, position = "kissing")
    "Camila laughs, then surprises both of you by nailing the expression on the next try."
    camila "Like this?"
    mc.name "Exactly like that."
    $ mc.change_locked_clarity(30)
    "A few outfit adjustments later, Camila lets the wrap slide down enough to bare one breast, then eventually both."
    $ scene_manager.strip_to_tits(camila)
    camila "Okay... wow. This is a lot less terrifying with another woman here."
    alexia "Told you. You're not hiding from the camera. You're making it chase you."
    "The confidence in Camila's posture changes the whole room. By the end of the session she is arching for the lens on instinct, and Alexia is grinning like a coach watching a rookie finally trust her body."
    $ scene_manager.update_actor(camila, position = "stand4", emotion = "happy")
    camila "I actually had fun."
    alexia "You did more than have fun. You looked incredible."
    mc.name "The shots came out great too."
    camila "Then maybe we do this again sometime. Maybe with less panic next time."
    alexia "I'd be into that."
    "The two women share an easy smile. For the first time, Camila's modelling idea feels like something real instead of a secret fantasy."
    python:
        camila.event_triggers_dict["boudoir_stage"] = 1
        camila.event_triggers_dict["boudoir_scheduled"] = False
        scene_manager.clear_scene()
        mc.change_location(downtown)
    return



#This label is separated into three parts.
#In the intro portion, we basically talk about what we have done so far as a group.
#In the transition stage, we introduce what will be occurring during this session. If MC has unlocked the next tier of sluttiness stuff, we find out about it here.
#In the final stage, the sex act occurs.
label camila_alexia_boudoir_recur_label(the_person):
    "It's Wednesday. The boudoir photoshoot with [camila.possessive_title] and [alexia.title] is tonight!"
    if mc.is_at_office:
        "You finish up quickly with the last of your daily tasks before going to your office."
    else:
        "You head back to work and to your office to get ready."
    $ mc.change_location(ceo_office)


    return
