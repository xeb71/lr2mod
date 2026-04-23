

label nora_place_prog_scene_action_label():
    call progression_scene_label(nora_place_prog_scene, [nora]) from _call_progression_scene_nora_prog_action
    return

label nora_place_prog_scene_intro_scene(the_group):
    $ the_person = the_group[0]

    return

# Intro Scene
label nora_place_prog_scene_intro_0(the_group):
    $ the_person = the_group[0]
    mc.name "Hey, I was thinking about having some fun tonight. You interested?"
    the_person "[the_person.mc_title], lately, I'm ALWAYS interested."
    return

# Choice Scene
label nora_place_prog_scene_choice_label(the_group):
    $ the_person = the_group[0]
    if persistent.mc_noncon_pref == 2:
        the_person "I know just what to do."
    else:
        the_person "If you want to unwind, I can certainly help with that."
    menu:
        "Let's go {image=progress_token_small}" if nora_place_prog_scene.progression_available:
            "Something in her voice tells you she has been thinking about taking things a step farther."
        "Let's go" if not nora_place_prog_scene.progression_available:
            pass
        "Not tonight":
            mc.name "Maybe another night."
            the_person "Fine. Try not to keep me waiting too long."
            return False
    the_person "Tell you what, why don't you make me some coffee while I slip into something more... exciting."
    mc.name "Of course, [the_person.title]."
    $ clear_scene()
    "You head to her kitchen and put on a pot of coffee."
    "When it is done, you pour two cups. You look at [the_person.title]'s cup for a moment..."
    call give_serum(the_person) from _call_give_nora_her_prog_01
    "You mix the serum into [the_person.title]'s coffee and take it to the bedroom."
    "You sit down on the side of the bed and wait for her."
    if the_person.wardrobe.get_outfit_with_name("Nora Lingerie"):
        $ the_person.apply_outfit(the_person.wardrobe.get_outfit_with_name("Nora Lingerie"))
    else:
        $ the_person.apply_outfit(lingerie_wardrobe.pick_random_outfit(), update_taboo = True)
    "A minute later, she appears in her bedroom door."
    $ the_person.draw_person()
    the_person "Alright, ready to get started?"
    mc.name "Absolutely."
    "She walks up to you and takes her coffe from your hand and takes a sip."
    "She sets the coffe down and get's ready to begin."
    return True

label nora_place_prog_scene_multiple_choice_scene(the_group):
    $ the_person = the_group[0]
    if persistent.mc_noncon_pref == 2:
        $ nora_choice = nora_place_prog_scene_choose_action()
        if nora_choice == 0:
            the_person "Tonight, I want to sit back and let you take care of me with your mouth."
        elif nora_choice == 1:
            the_person "You've been keeping up lately, so tonight you are going to prove you can last for me."
        elif nora_choice == 2:
            the_person "Enough teasing. Lie back and let me ride you."
        return nora_choice

    the_person "Anything in particular you are in the mood for?"
    menu:
        "Oral Service" if 0 in nora_place_prog_scene.scene_unlock_list:
            $ show_popup_hint(nora_place_prog_scene_0_popup_text())
            mc.name "Why don't you sit on my face for a bit tonight?"
            the_person "Ah, can't get enough of my ass, can you? Alright."
            return 0
        "Endurance Test" if (1 in nora_place_prog_scene.scene_unlock_list) and (nora.sex_record.get("Last Sex Day", 0) >= day - 7):
            $ show_popup_hint(nora_place_prog_scene_1_popup_text())
            mc.name "I want to test my endurance tonight."
            the_person "Hmm, I suppose you HAVE been doing well at keeping me satisfied lately..."
            the_person "Alright, let's see if you have what it takes to make the night last."
            return 1
        "Endurance Test\n{menu_red}Too long since last sex session{/menu_red}(disabled)" if (1 in nora_place_prog_scene.scene_unlock_list) and (nora.sex_record.get("Last Sex Day", 0) < day - 7):
            pass
        "Cowgirl" if 2 in nora_place_prog_scene.scene_unlock_list:
            $ show_popup_hint(nora_place_prog_scene_2_popup_text())
            mc.name "Come here and show me those hips of yours."
            the_person "Mmm. I thought you'd pick that."
            return 2
        "Breeding Fetish Session" if 3 in nora_place_prog_scene.scene_unlock_list:
            return 3
        "Anal Fetish Session" if 4 in nora_place_prog_scene.scene_unlock_list:
            return 4
        "Cum Fetish Session" if 5 in nora_place_prog_scene.scene_unlock_list:
            return 5
        "Exhibitionist Session" if 6 in nora_place_prog_scene.scene_unlock_list:
            return 6
    return 0

#Exit scene. Nora might even get mad since he brought it up?
label nora_place_prog_scene_exit_scene(the_group):
    $ the_person = the_group[0]
    the_person "Another night then. I'll just have to work off this mood myself."
    return

#######################
#  Transition Scenes  #
#######################

label nora_place_prog_trans_scene_0(the_group):
    pass
    "This scene should never show. If you are seeing this, something went wrong."
    return

label nora_place_prog_trans_scene_1(the_group):
    $ the_person = the_group[0]
    $ show_popup_hint("New option unlocked:\n  Endurance Test")
    the_person "You have been doing a decent job keeping me satisfied lately."
    the_person "Let's see if you can keep up when I decide not to make this quick for you."
    return

label nora_place_prog_trans_scene_2(the_group):
    $ the_person = the_group[0]
    $ show_popup_hint("New option unlocked:\n  Cowgirl")
    the_person "I've spent enough nights teasing you."
    the_person "Tonight I'm taking what I want and you are going to lie back and enjoy it."
    return

label nora_place_prog_trans_scene_3(the_group):
    $ the_person = the_group[0]
    "In this scene, [the_person.possessive_title] rides MC to a creampie to fulfill her breeding fetish."
    return

label nora_place_prog_trans_scene_4(the_group):
    $ the_person = the_group[0]
    "In this scene, [the_person.possessive_title] rides MC anally to fulfill her anal fetish."
    return

label nora_place_prog_trans_scene_5(the_group):
    $ the_person = the_group[0]
    "In this scene, [the_person.possessive_title] tries to make MC cum multiple times to fulfill her cum fetish."
    return

label nora_place_prog_trans_scene_6(the_group):
    $ the_person = the_group[0]
    "In this scene, [the_person.possessive_title] ties up MC and livestreams a sex session for her exhibitionism fetish?."
    return


######################
#     End Scenes     #
######################


label nora_place_prog_scene_repeat_label(the_person, start_position, start_object, position_locked = True):
    $ keep_going = True
    while keep_going:
        call fuck_person(the_person, start_position = start_position, start_object = start_object, skip_intro = True, girl_in_charge = True, position_locked = position_locked) from _call_nora_place_prog_scene_repeat
        if _return.get("girl orgasms", 0) <= 0:
            return

        menu:
            "Keep going":
                if persistent.mc_noncon_pref == 2:
                    the_person "Good. Then stay right there. I'm not done with you yet."
                else:
                    the_person "Mmm... I could stop there, but where would be the fun in that?"
            "Leave":
                $ keep_going = False
    return


label nora_place_prog_scene_scene_0(the_group, scene_transition = False):
    $ the_person = the_group[0]
    if scene_transition:
        the_person "Relax. Just focus on making me feel good."
    else:
        the_person "On your back. I feel like being worshipped."
    if mc.sex_skills["Oral"] >= 6 and (mc.max_energy >= 160 or perk_system.has_ability_perk("Serum: Feat of Orgasm Control")) and the_person.effective_sluttiness() >= 60:
        call nora_place_prog_scene_repeat_label(the_person, sixty_nine, make_bed(), True) from _call_nora_place_prog_scene_0_full
    else:
        call nora_place_prog_scene_repeat_label(the_person, cunnilingus, make_bed(), True) from _call_nora_place_prog_scene_0_partial
    call nora_place_prog_post_scene(the_group) from _call_nora_place_prog_post_scene_0
    return

label nora_place_prog_scene_scene_1(the_group, scene_transition = False):
    $ the_person = the_group[0]
    if scene_transition:
        the_person "You wanted to make this last? Good. Then don't waste any of your energy."
    else:
        the_person "Tonight you don't get to rush to the finish."
    if mc.sex_skills["Oral"] >= 6 and mc.sex_skills["Foreplay"] >= 6 and mc.sex_skills["Vaginal"] >= 6 and (mc.max_energy >= 170 or perk_system.has_ability_perk("Serum: Feat of Orgasm Control")):
        call nora_place_prog_scene_repeat_label(the_person, sixty_nine, make_bed(), False) from _call_nora_place_prog_scene_1_full
    else:
        call nora_place_prog_scene_repeat_label(the_person, blowjob, make_bed(), True) from _call_nora_place_prog_scene_1_partial
    call nora_place_prog_post_scene(the_group) from _call_nora_place_prog_post_scene_1
    return

label nora_place_prog_scene_scene_2(the_group, scene_transition = False):
    $ the_person = the_group[0]
    if scene_transition:
        the_person "Hands off unless I tell you otherwise."
    else:
        the_person "Good. Then stay right there and let me work."
    call nora_place_prog_scene_repeat_label(the_person, cowgirl, make_bed(), True) from _call_nora_place_prog_scene_2
    call nora_place_prog_post_scene(the_group) from _call_nora_place_prog_post_scene_2
    return

label nora_place_prog_scene_scene_3(the_group, scene_transition = False):
    pass
    return

label nora_place_prog_scene_scene_4(the_group, scene_transition = False):
    pass
    return

label nora_place_prog_scene_scene_5(the_group, scene_transition = False):
    pass
    return

label nora_place_prog_scene_scene_6(the_group, scene_transition = False):
    pass
    return

label nora_place_prog_post_scene(the_group):
    $ the_person = the_group[0]
    call sex_review_trance(the_person) from _call_nora_place_prog_sex_review
    $ clear_scene()
    if the_person.wardrobe.get_outfit_with_name("Nora Lingerie"):
        $ the_person.apply_outfit(the_person.wardrobe.get_outfit_with_name("Nora Lingerie"))
    else:
        $ the_person.apply_planned_outfit()
    $ the_person.draw_person()
    the_person "That should keep me in a better mood for a while."
    mc.name "I can work with that."
    return
