# Contains all of the information/events for girls who are on instapic.
# Girls are given this role if they have an account.

define INSTA_PHOTO_ALBUM_BOX_XALIGN = 0.42

label check_insta():
    # TODO: Check if anyone you know has posted pictures on InstaPic
    # TODO: Ability to find new Insta girls who are posting revealing pics.
    call screen main_choice_display(build_menu_items(build_insta_menu(), draw_hearts_for_people = False, draw_person_previews = False, draw_insta = True))
    if isinstance(_return, Person):
        call view_insta(_return) from _call_view_insta
        jump check_insta
    return

label view_insta(the_person):
    # TODO: If she has a dikdok or onlyfan she may plug that along with a slutty pic.
    # TODO: Add support for girls doing colab posts or bringing their friends in. ie. Mom and Lily should appear in some shoots together.
    $ the_person.event_triggers_dict["insta_awaiting_mc_response"] = False
    $ _dm_responded = the_person.event_triggers_dict.get("insta_special_request_responded", False)
    if _dm_responded and not the_person.event_triggers_dict.get("insta_dm_photo_available", False):
        # For non-photo responses (e.g. outfit requests), clear the responded flag immediately
        # since the outfit will surface through the public-post branch when insta_generate_pic fires.
        # For DM photo responses, defer clearing until the notification branch fires to avoid
        # permanently losing the notification when a public post also shows on the same visit.
        $ the_person.event_triggers_dict["insta_special_request_responded"] = False
        $ the_person.event_triggers_dict["insta_special_request_type"] = None
    $ posted_today = False
    if _dm_responded and the_person.event_triggers_dict.get("insta_dm_photo_available", False):
        $ the_person.event_triggers_dict["insta_special_request_responded"] = False
        $ the_person.event_triggers_dict["insta_special_request_type"] = None
        $ the_person.event_triggers_dict["insta_dm_photo_available"] = False
        "You open InstaPic and see that [the_person.title] has shared some private photos with you!"
        $ posted_today = True
        $ _latest_dm_photo = the_person.event_triggers_dict["insta_photo_history"][-1]
        call dm_replay_photo(the_person, _latest_dm_photo, is_new = True) from _call_dm_replay_photo_new_post
        $ the_person.event_triggers_dict["insta_awaiting_mc_response"] = True

    if the_person.event_triggers_dict.get("insta_generate_pic", False):
        "It looks like [the_person.title] has posted a new picture today, along with a comment overlaid at the bottom."
        $ posted_today = True
        if the_person.event_triggers_dict.get("insta_new_boobs_brag", None) is not None:
            $ the_person.event_triggers_dict["insta_new_boobs_brag"] = None
            $ skimpy_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ the_person.apply_outfit(skimpy_outfit)
            $ ran_num = renpy.random.randint(0,1)
            if ran_num == 0:
                $ the_person.draw_person()
            else:
                $ the_person.draw_person(position = "kneeling1")
            $ mc.change_locked_clarity(15)
            the_person "Went to the doc and got some upgrades! Don't they look great?!"
            $ the_person.event_triggers_dict["insta_last_public_post"] = {"type": "public", "outfit": skimpy_outfit, "position": {0: "default", 1: "kneeling1"}.get(ran_num, "default"), "reply": "Went to the doc and got some upgrades! Don't they look great?!"}
            $ the_person.apply_planned_outfit() # Reset them to their normal daily wear.
            $ del skimpy_outfit

        elif the_person.event_triggers_dict.get("insta_special_request_outfit", None):
            $ _request_outfit = the_person.event_triggers_dict.get("insta_special_request_outfit")
            $ the_person.apply_outfit(_request_outfit)
            $ ran_num = renpy.random.randint(0,2)
            $ _outfit_position = "default"
            if ran_num == 0:
                $ the_person.draw_person()
            elif ran_num == 1:
                $ _outfit_position = "kneeling1"
                $ the_person.draw_person(position = "kneeling1")
            else:
                $ _outfit_position = "back_peek"
                $ the_person.draw_person(position = "back_peek")
            $ mc.change_locked_clarity(10)
            the_person "Wearing something special today: a design sent in by a fan!"
            $ add_insta_photo_to_history(the_person, "outfit", outfit=_request_outfit, position=_outfit_position, reply="Wearing something special today: a design sent in by a fan!")
            $ the_person.event_triggers_dict["insta_special_request_outfit"] = None

        elif the_person.effective_sluttiness() + (5 * the_person.opinion(("showing her ass", "showing her tits"))) > 20: #TODO: Decide what slut_requirement should be.
            $ skimpy_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ the_person.apply_outfit(skimpy_outfit)
            $ ran_num = renpy.random.randint(0,3)
            if ran_num == 0:
                $ the_person.draw_person(position = "stand3")
                $ mc.change_locked_clarity(5)
                the_person "Thought this outfit looked sexy. What do you think?"
            elif ran_num == 1:
                $ the_person.draw_person(position = "kneeling1")
                $ mc.change_locked_clarity(10)
                the_person "Hey everyone, what do you think of this pose? I think it makes my tits look great!"
            elif ran_num == 2:
                $ the_person.draw_person(position = "back_peek")
                $ mc.change_locked_clarity(5)
                the_person "Ass was looking great, just had to take a pic!"
            elif ran_num == 3:
                $ the_person.draw_person(position = "kneeling1")
                $ mc.change_locked_clarity(10)
                the_person "Do I look good down on my knees?"

            if the_person.has_role(dikdok_role) and the_person.event_triggers_dict.get("dikdok_generate_video", False):
                the_person "If you liked that, come see me getting into trouble on DikDok! Hurry, I might get banned soon!"
                $ the_person.learn_dikdok()

            elif the_person.has_role(onlyfans_role) and the_person.event_triggers_dict.get("instafans_generate_content", False):
                the_person "If you like that, subscribe to my OnlyFanatics and see soooo much more!"
                $ the_person.learn_onlyfans()

            $ _slut_pos_map = {0: "stand3", 1: "kneeling1", 2: "back_peek", 3: "kneeling1"}
            $ _slut_reply_map = {0: "Thought this outfit looked sexy. What do you think?", 1: "Hey everyone, what do you think of this pose? I think it makes my tits look great!", 2: "Ass was looking great, just had to take a pic!", 3: "Do I look good down on my knees?"}
            $ the_person.event_triggers_dict["insta_last_public_post"] = {"type": "public", "outfit": skimpy_outfit, "position": _slut_pos_map.get(ran_num, "default"), "reply": _slut_reply_map.get(ran_num, "Looked great in this outfit!")}
            $ the_person.apply_planned_outfit() # Reset them to their normal daily wear.
            $ del skimpy_outfit
        elif the_person.is_wearing_uniform and not (the_person.vagina_visible or the_person.tits_visible):
            $ ran_num = renpy.random.randint(0,1)
            if ran_num == 0:
                $ mc.change_locked_clarity(5)
                $ the_person.draw_person()
                the_person "Getting dressed for work. I make this uniform work!"

            elif ran_num == 1:
                $ mc.change_locked_clarity(10)
                $ the_person.draw_person(position = "back_peek")
                the_person "I think my boss makes me wear this just because it makes my butt look good. At least he's right!"

        else:
            $ ran_num = renpy.random.randint(0,1)
            if ran_num == 0:
                $ the_person.draw_person()
                the_person "Good morning everyone!"

            elif ran_num == 1:
                $ the_person.draw_person(position = "back_peek")
                the_person "About to head out the door. I've got a full day ahead of me!"

    if not posted_today:
        #TODO: Include a chance for something flavourful like "It's just pictures of food. Pages and pages of food!"
        "You scan [the_person.title]'s profile. Nothing new today."

    call instapic_comment_loop(the_person, posted_today) from _call_instapic_comment_loop
    $ clear_scene()
    $ the_person.event_triggers_dict["insta_generate_pic"] = False
    $ the_person.event_triggers_dict.pop("insta_last_public_post", None)
    return

label save_public_post(the_person):
    $ _post_data = the_person.event_triggers_dict.pop("insta_last_public_post", None)
    if _post_data:
        $ add_insta_photo_to_history(the_person, _post_data.get("type", "public"), _post_data.get("outfit"), _post_data.get("position"), _post_data.get("reply"))
        "Photo saved to your private messages with [the_person.title]."
    call instapic_comment_loop(the_person, posted_today = False) from _call_instapic_comment_loop_save
    return

label instapic_comment_loop(the_person, posted_today = False):
    call screen main_choice_display(build_menu_items(build_instapic_comment_actions(the_person, posted_today)))
    if isinstance(_return, Action):
        $ _return.call_action(the_person)
    return

label comment_description(comment_type, the_person):
    $ the_person.set_event_day("insta_commented_day")
    $ save_mc_insta_response(the_person, comment_type)
    if comment_type == "obedience_mild":
        mc.name "You look amazing! I'd love it if you posted more often for your fans."
        $ _amt = the_person.change_obedience(1, add_to_log = False)
        $ mc.log_notification(f"{the_person.display_name}: {_amt:+.0f} {{image=triskelion_token_small}} (instapic)", "float_text_obedience") if _amt else None
        $ the_person.change_happiness(the_person.opinion.taking_control - 1, add_to_log = False)
    elif comment_type == "obedience_strong":
        mc.name "You really should be posting more. Your fans deserve better content from you."
        $ _amt = the_person.change_obedience(3, add_to_log = False)
        $ mc.log_notification(f"{the_person.display_name}: {_amt:+.0f} {{image=triskelion_token_small}} (instapic)", "float_text_obedience") if _amt else None
        $ _penalty = -(_amt // 2)
        $ the_person.change_slut(_penalty, add_to_log = False) if _penalty else None
        $ mc.log_notification(f"{the_person.display_name}: {_penalty:+.0f} {{image=gold_heart_token_small}} (instapic)", "float_text_slut") if _penalty else None
        $ the_person.change_happiness(the_person.opinion.taking_control - 2, add_to_log = False)
    elif comment_type == "slut_mild":
        mc.name "Incredible figure! You should definitely show more of it. 🔥"
        $ _amt = the_person.change_slut(1, 40, add_to_log = False)
        $ mc.log_notification(f"{the_person.display_name}: {_amt:+.0f} {{image=gold_heart_token_small}} (instapic)", "float_text_slut") if _amt else None
        $ the_person.change_happiness(the_person.opinion(("showing her tits", "showing her ass")) - 1, add_to_log = False)
    elif comment_type == "slut_strong":
        mc.name "Stop hiding it! Your body is way too good to keep covered. Show it off!"
        $ _amt = the_person.change_slut(3, 60, add_to_log = False)
        $ mc.log_notification(f"{the_person.display_name}: {_amt:+.0f} {{image=gold_heart_token_small}} (instapic)", "float_text_slut") if _amt else None
        $ _penalty = -(_amt // 2)
        $ the_person.change_love(_penalty, add_to_log = False) if _penalty else None
        $ mc.log_notification(f"{the_person.display_name}: {_penalty:+.0f} {{image=red_heart_token_small}} (instapic)", "float_text_love") if _penalty else None
        $ the_person.change_happiness(the_person.opinion(("showing her tits", "showing her ass")) - 2, add_to_log = False)
    elif comment_type == "love_mild":
        mc.name "You're absolutely stunning. I can't stop looking at your posts. 💕"
        $ _amt = the_person.change_love(1, add_to_log = False)
        $ mc.log_notification(f"{the_person.display_name}: {_amt:+.0f} {{image=red_heart_token_small}} (instapic)", "float_text_love") if _amt else None
        $ the_person.change_happiness(1, add_to_log = False)
    elif comment_type == "love_strong":
        mc.name "I'm completely obsessed with you. You're perfect in every way. I need to see more of you."
        $ _amt = the_person.change_love(3, add_to_log = False)
        $ mc.log_notification(f"{the_person.display_name}: {_amt:+.0f} {{image=red_heart_token_small}} (instapic)", "float_text_love") if _amt else None
        $ _penalty = -(_amt // 2)
        $ the_person.change_obedience(_penalty, add_to_log = False) if _penalty else None
        $ mc.log_notification(f"{the_person.display_name}: {_penalty:+.0f} {{image=triskelion_token_small}} (instapic)", "float_text_obedience") if _penalty else None
    if the_person.event_triggers_dict.get("insta_last_public_post"):
        menu:
            "Would you like to save this photo to your collection?"
            "Yes":
                $ _post_data = the_person.event_triggers_dict.pop("insta_last_public_post", None)
                if _post_data:
                    $ add_insta_photo_to_history(the_person, _post_data.get("type", "public"), _post_data.get("outfit"), _post_data.get("position"), _post_data.get("reply"))
                    $ _mc_text = _INSTA_MC_COMMENT_TEXT.get(comment_type)
                    if _mc_text:
                        $ the_person.event_triggers_dict["insta_photo_history"][-1]["mc_response"] = _mc_text
                    "Photo saved to your private messages with [the_person.title]."
            "No":
                pass
    call instapic_comment_loop(the_person, posted_today = False) from _call_instapic_comment_loop_1
    return

label dm_description(the_person):
    call screen main_choice_display(build_menu_items(build_dm_description_actions(the_person)))
    if isinstance(_return, Action):
        $ _return.call_action(the_person)
        if _return == True:
            $ the_person.event_triggers_dict["insta_special_request_pending"] = True
            "You hit send. You'll have to wait for her to get back to you with a response."
        elif _return == False:
            "You hesitate before hitting send, then decide against messaging her at all and delete it."
    return

label dm_option_specific_outfit(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    if previous_request_level == 0:
        mc.name "I found your profile and thought that you look amazing! I was wondering if you took special requests."
        mc.name "I think you would look amazing wearing this outfit, and I'd pay you $20 if you made an InstaPic for it."

    else:# previous_request_level > 0:
        mc.name "I think you would look amazing in this outfit, you should wear it for your next InstaPic post."
        mc.name "If you do I'll send you $20, and I'm sure it'll be great for your brand!"

    call outfit_master_manager(show_overwear = False, show_underwear = False, start_mannequin = the_person) from _call_outfit_master_manager_11
    if isinstance(_return, Outfit):
        "You put together a list of links to stores she could buy everything from."
        $ add_dm_outfit_response(the_person, _return)
        $ the_person.event_triggers_dict["insta_special_request_feasible"] = (the_person.effective_sluttiness() + 5 >= _return.outfit_slut_score)
        $ the_person.event_triggers_dict["insta_special_request_type"] = "Outfit request"
        return True
    return False

label dm_option_specific_outfit_response(the_person, the_outfit):
    "Your phone buzzes: it's a response from [the_person.title] on InstaPic."
    $ the_choice = False
    if insta_would_ban(the_outfit):
        the_person "Thanks for the interest, but I couldn't wear that without getting banned!"
        if the_person.has_role(onlyfans_role):
            the_person "If you're interested in that sort of content you should check out my OnlyFanatics!"
            $ the_person.learn_onlyfans()
            "She gives you her OnlyFanatics name."
    elif the_person.effective_sluttiness() + 5 < the_outfit.outfit_slut_score:
        $ _refusal_msg = get_insta_refusal_message()
        the_person "[_refusal_msg]"
    elif the_person.judge_outfit(the_outfit, temp_sluttiness_boost = -20) and the_outfit.outfit_slut_score < 40:
        the_person "It's nice, but I don't think it's the sort of thing my audience is interested in seeing."
        the_person "Thanks for the interest though!"
    elif the_person.judge_outfit(the_outfit):
        the_person "Thanks for the interest, that outfit is so cute! I could see myself wearing it every day!"
        the_person "Send me the money and check my Insta page in a day or two!"
        $ the_choice = True
    elif the_person.judge_outfit(the_outfit, temp_sluttiness_boost = 20):
        the_person "Thanks for the interest! That's not the kind of thing I would normally wear in one of my posts, but I'm willing to give it a try!"
        the_person "Send me the money and check my Insta page in a day or two! If the reactions are good maybe I'll wear more stuff like that!"
        $ the_choice = True
    else:
        the_person "I don't take requests, I'm just doing this for fun. Sorry!"

    if the_choice:
        if the_person.effective_sluttiness() < the_outfit.outfit_slut_score:
            $ the_person.change_slut(renpy.random.randint(1, 3), the_outfit.outfit_slut_score)
        $ the_person.event_triggers_dict["insta_special_request_outfit"] = the_outfit
        if the_person.event_triggers_dict.get("insta_special_request_level",0) < 1:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 1
        $ mc.business.change_funds(-20, stat = "Shopping")
        "You wire her the cash you promised."

    $ insta_dm_cleanup(the_person)
    return

label dm_option_underwear(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    if previous_request_level == 0:
        mc.name "I just found your profile, you look so amazing! I wish you could show more, but I know InstaPic would ban you if you did."
        mc.name "Do you take private pictures? I'd be glad to pay just for some shots of you in your underwear. How does $50 sound?"

    elif previous_request_level == 1:
        mc.name "You looked so good in that last outfit, I wish you could show more without InstaPic banning you."
        mc.name "How about some private pictures, just for me? I'll pay $50 for some shots of you in your underwear."

    else:# previous_request_level == 2:
        mc.name "Interested in making another fifty bucks? I'd like some more shots of you in your underwear."

    $ add_dm_underwear_response(the_person)
    $ the_person.event_triggers_dict["insta_special_request_feasible"] = (the_person.effective_sluttiness() + 10 >= 40)
    $ the_person.event_triggers_dict["insta_special_request_type"] = "Underwear shots"

    if the_person.has_role(sister_role):
        $ the_person.event_triggers_dict["insta_special_request_sis"] = "underwear"
    return True

label dm_option_underwear_response(the_person):
    "Your phone buzzes: it's a response from [the_person.title] on InstaPic."
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    $ the_choice = False
    $ saved_insta_outfit = None
    $ saved_insta_position = None
    $ _photo_reply = None

    if the_person.effective_sluttiness() + 10 < 40:
        $ _refusal_msg = get_insta_refusal_message()
        the_person "[_refusal_msg]"
    elif the_person.effective_sluttiness() < 40: #Moderately slutty, she'll do it
        $ the_choice = True
        $ the_person.change_slut(renpy.random.randint(1, 3), 40)
        $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
        $ saved_insta_outfit.strip_to_underwear(avoid_nudity = True)
        $ saved_insta_position = renpy.random.choice(["kneeling1", "back_peek", "sitting"])
        if previous_request_level < 2: #First time
            $ _photo_reply = "This was a little out of my comfort zone, but I couldn't say no to a fan!"
            the_person "This was a little out of my comfort zone, but I couldn't say no to a fan!"
        else: #Has done it before, or already done worse
            $ _photo_reply = "It's always nice to hear from you. I hope this shot is what you were thinking of!"
            the_person "It's always nice to hear from you. I hope this shot is what you were thinking of!"

        "She sends you some private photos. Check her InstaPic album to view them."
        the_person "Enjoy, and remember to leave a nice comment on my profile!"

    else:
        $ the_choice = True
        $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
        $ saved_insta_outfit.strip_to_underwear()
        $ saved_insta_position = renpy.random.choice(["kneeling1", "back_peek", "sitting"])
        $ _photo_reply = "I had a lot of fun taking these. Always happy to do something special for a fan!"
        the_person "I had a lot of fun taking these. Always happy to do something special for a fan!"

        "She sends you a set of private photos. Check her InstaPic album to view them."
        the_person "Have fun with those, and let me know if there's anything else I can do for you!"

    if the_choice:
        if the_person.has_role(onlyfans_role) and not the_person.onlyfans_known:
            the_person "Oh, and if you liked that, check out my OnlyFanatics page. I'm sure you'll love it!"
            $ the_person.learn_onlyfans()
            "She sends you a link."

        $ mc.business.change_funds(-50, stat = "Shopping")
        if the_person.event_triggers_dict.get("insta_special_request_level",0) < 2:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 2
        $ add_insta_photo_to_history(the_person, "underwear", saved_insta_outfit, saved_insta_position, reply=_photo_reply)
        "You wire her the cash you promised."

    $ insta_dm_cleanup(the_person, photo_received=the_choice)
    return


label dm_option_topless(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    if previous_request_level == 0:
        mc.name "I just found your profile and it blew me away! You're gorgeous!"
        mc.name "Do you do topless shots? Your tits are driving me crazy, I'd pay to see them!"
        mc.name "How about $100? Would that be enough for some private pics?"
    elif previous_request_level == 1:
        mc.name "You looked so good in that last outfit, I wish you could show more without InstaPic banning you."
        mc.name "Would you consider taking some topless shots? Your tits are driving me crazy, I'd pay to see them!"
        mc.name "How about $100? Would that be enough for some private pics?"
    elif previous_request_level == 2:
        mc.name "Those last shots were so hot, I loved them!"
        mc.name "How about some topless shots? I'd pay more, of course."
    else:
        mc.name "I want some pictures of your tits, would $100 be enough?"

    $ add_dm_topless_response(the_person)
    $ the_person.event_triggers_dict["insta_special_request_feasible"] = (the_person.effective_sluttiness() + 15 >= 50)
    $ the_person.event_triggers_dict["insta_special_request_type"] = "Topless shots"

    if the_person.has_role(sister_role):
        $ the_person.event_triggers_dict["insta_special_request_sis"] = "topless"
    return True

label dm_option_topless_response(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    $ the_choice = False
    $ saved_insta_outfit = None
    $ saved_insta_position = renpy.random.choice(["kneeling1", "stand3", "stand4"])
    $ _photo_reply = None
    $ _opinion_tits = the_person.opinion.showing_her_tits
    "Your phone buzzes: it's a response from [the_person.title] on InstaPic."
    if the_person.effective_sluttiness() + 15 < 50:
        $ _refusal_msg = get_insta_refusal_message()
        the_person "[_refusal_msg]"
    else:
        $ the_choice = True
        if the_person.effective_sluttiness() < 50: #Borderline - push her a little
            $ the_person.change_slut(renpy.random.randint(1, 3), 50)
        if _opinion_tits >= 2: #Loves showing tits - does it enthusiastically
            $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ saved_insta_outfit.strip_to_tits(prefer_half_off = True)
            if previous_request_level < 3:
                $ _photo_reply = "I love showing off my tits, they're my best feature! Hope you enjoy!"
                the_person "I love showing off my tits, they're my best feature! Hope you enjoy!"
            else:
                $ _photo_reply = "Another topless set for my biggest fan! I know you love the view!"
                the_person "Another topless set for my biggest fan! I know you love the view!"
            "She sends you a set of private photos. Check her InstaPic album to view them."
            the_person "Hope that gives you something to look at tonight!"
        elif _opinion_tits >= 1: #Likes showing tits - does it willingly
            $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ saved_insta_outfit.strip_to_tits(prefer_half_off = True)
            if previous_request_level < 2:
                $ _photo_reply = "I think I look pretty good topless, why not show off a little?"
                the_person "I think I look pretty good topless, why not show off a little?"
            else:
                $ _photo_reply = "Always happy to show off for a fan! Here are those shots you asked for!"
                the_person "Always happy to show off for a fan! Here are those shots you asked for!"
            "She sends you some private photos. Check her InstaPic album to view them."
            the_person "Enjoy the view, and remember to leave me a nice comment!"
        elif _opinion_tits == 0: #Neutral - sends clothed photos
            $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            if previous_request_level < 2:
                $ _photo_reply = "This was a bit of an unusual request, but I suppose it's harmless. Hope this is what you wanted!"
                the_person "This was a bit of an unusual request, but I suppose it's harmless. Hope this is what you wanted!"
            else:
                $ _photo_reply = "Sure, I can do that for a fan! Here you go!"
                the_person "Sure, I can do that for a fan! Here you go!"
            "She sends you some photos. Check her InstaPic album to view them."
            the_person "Let me know if there is anything else I can do for you!"
        else: #Negative opinion - reluctantly, slut penalty
            $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ the_person.change_slut(-1)
            if previous_request_level < 2:
                $ _photo_reply = "I guess I can take a few shots, but I'm not really comfortable with this kind of request..."
                the_person "I guess I can take a few shots, but I'm not really comfortable with this kind of request..."
            else:
                $ _photo_reply = "I keep getting these requests... I'm a bit embarrassed honestly."
                the_person "I keep getting these requests... I'm a bit embarrassed honestly."
            "She sends you some reluctant photos. Check her InstaPic album to view them."
            the_person "Please keep these private, I don't want everyone seeing this."

    if the_choice:
        if the_person.has_role(onlyfans_role) and not the_person.onlyfans_known:
            the_person "Oh, and if you liked that, check out my OnlyFanatics page. I'm sure you'll love it!"
            "She sends you a link."
            $ the_person.learn_onlyfans()


        $ mc.business.change_funds(-100, stat = "Shopping")
        if the_person.event_triggers_dict.get("insta_special_request_level",0) < 3:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 3
        $ add_insta_photo_to_history(the_person, "topless", saved_insta_outfit, saved_insta_position, reply=_photo_reply)
        "You wire her the cash you promised."

    $ insta_dm_cleanup(the_person, photo_received=the_choice)
    return

label dm_option_nude(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    if previous_request_level == 0:
        mc.name "I just found your profile and it blew me away! You're gorgeous!"
        mc.name "Do you do more revealing shots? I'd gladly donate some money to see you au naturel!"
        mc.name "Would $200 be enough for some private pics?"
    elif previous_request_level == 1:
        mc.name "Your posts are so hot, but I really think you'd look better naked."
        mc.name "Do you do nude shots? I'd not mind contributing some money to see you naked!"
        mc.name "How about $200? Would that be enough for some private pics?"
    elif previous_request_level == 2 or previous_request_level == 3:
        mc.name "Fuck, you're so beautiful I just need to see more of you!"
        mc.name "I would love more nude pictures, could you send them to me? I'll pay you $200 for them."
    else:
        mc.name "I'm looking for some more nudes, interested? I'll pay another $200 for them."

    $ add_dm_nude_response(the_person)
    $ the_person.event_triggers_dict["insta_special_request_feasible"] = (the_person.effective_sluttiness() + 20 >= 60)
    $ the_person.event_triggers_dict["insta_special_request_type"] = "Nude shots"

    if the_person.has_role(sister_role):
        $ the_person.event_triggers_dict["insta_special_request_sis"] = "nude"
    return True

label dm_option_nude_response(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    $ the_choice = False
    $ saved_insta_outfit = None
    $ saved_insta_position = None
    $ _photo_reply = None
    "Your phone buzzes: it's a response from [the_person.title] on InstaPic."
    if the_person.effective_sluttiness() + 20 < 60:
        $ _refusal_msg = get_insta_refusal_message()
        the_person "[_refusal_msg]"
    elif the_person.effective_sluttiness() < 60: #Willing, not excited.
        $ the_choice = True
        $ the_person.change_slut(renpy.random.randint(1, 3), 60)
        $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
        $ saved_insta_outfit.strip_to_tits()
        $ saved_insta_outfit.remove_shirt()
        $ saved_insta_outfit.strip_to_vagina()
        $ saved_insta_position = renpy.random.choice(["kneeling1", "stand3", "stand4"])
        if previous_request_level < 4: #First time
            $ _photo_reply = "I wouldn't normally do something like this, but I suppose I can give it a try. Be nice!"
            the_person "I wouldn't normally do something like this, but I suppose I can give it a try. Be nice!"

        else: #You've done this before
            $ _photo_reply = "It's always nice to hear from you, of course I can take some pics for you!"
            the_person "It's always nice to hear from you, of course I can take some pics for you!"

        "She sends you some private photos. Check her InstaPic album to view them."
        the_person "Enjoy, and message me any time you have a special request."

    else: #Willing and excited
        $ the_choice = True
        $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
        $ saved_insta_outfit.strip_to_tits()
        $ saved_insta_outfit.remove_shirt()
        $ saved_insta_outfit.strip_to_vagina()
        $ saved_insta_position = renpy.random.choice(["kneeling1", "stand3", "stand4"])
        $ _photo_reply = "I love getting requests like this! Of course I can take some shots for you!"
        the_person "I love getting requests like this! Of course I can take some shots for you!"

        "She sends you a set of private photos. Check her InstaPic album to view them."
        the_person "I hope you have fun with those, I had fun taking them!"

    if the_choice:
        if the_person.has_role(onlyfans_role) and not the_person.onlyfans_known:
            the_person "Oh, and if you liked that, check out my OnlyFanatics page. I'm sure you'll love it!"
            "She sends you a link."
            $ the_person.learn_onlyfans()

        $ mc.business.change_funds(-200, stat = "Shopping")
        if the_person.event_triggers_dict.get("insta_special_request_level",0) < 4:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 4
        $ add_insta_photo_to_history(the_person, "nude", saved_insta_outfit, saved_insta_position, reply=_photo_reply)
        "You wire her the cash you promised."

    $ insta_dm_cleanup(the_person, photo_received=the_choice)
    return

label dm_option_ass(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    if previous_request_level == 0:
        mc.name "I just found your profile, you look absolutely incredible!"
        mc.name "Would you consider sending me some private photos showing off that amazing ass? I'd be happy to pay $75."
    elif previous_request_level == 1:
        mc.name "Those last pictures were so hot! You have such an amazing body."
        mc.name "Would you be willing to show off that gorgeous ass for me? I'll pay $75."
    else:
        mc.name "I'm always happy to send more your way. How about some more shots showing off that ass? $75 as usual."

    $ add_dm_ass_response(the_person)
    $ the_person.event_triggers_dict["insta_special_request_feasible"] = (the_person.effective_sluttiness() + 10 >= 40)
    $ the_person.event_triggers_dict["insta_special_request_type"] = "Ass shots"

    if the_person.has_role(sister_role):
        $ the_person.event_triggers_dict["insta_special_request_sis"] = "ass"
    return True

label dm_option_ass_response(the_person):
    $ previous_request_level = the_person.event_triggers_dict.get("insta_special_request_level", 0)
    $ the_choice = False
    $ saved_insta_outfit = None
    $ saved_insta_position = "back_peek"
    $ _photo_reply = None
    $ _opinion_ass = the_person.opinion.showing_her_ass
    "Your phone buzzes: it's a response from [the_person.title] on InstaPic."
    if the_person.effective_sluttiness() + 10 < 40:
        $ _refusal_msg = get_insta_refusal_message()
        the_person "[_refusal_msg]"
    else:
        $ the_choice = True
        if the_person.effective_sluttiness() < 40: #Borderline - push her a little
            $ the_person.change_slut(renpy.random.randint(1, 3), 40)
        if _opinion_ass >= 2: #Loves showing ass - does it naked
            $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ saved_insta_outfit.strip_to_vagina(prefer_half_off = True)
            if previous_request_level < 3:
                $ _photo_reply = "I love showing off my ass, it's one of my best features! Enjoy!"
                the_person "I love showing off my ass, it's one of my best features! Enjoy!"
            else:
                $ _photo_reply = "Another ass shot for my biggest fan! I know you love this view!"
                the_person "Another ass shot for my biggest fan! I know you love this view!"
            "She sends you a set of private photos. Check her InstaPic album to view them."
            the_person "Hope that gives you something to look at tonight!"
        elif _opinion_ass >= 1: #Likes showing ass - underwear
            $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ saved_insta_outfit.strip_bottom_to_underwear()
            if previous_request_level < 2:
                $ _photo_reply = "I think I look pretty good from behind, why not show it off a little?"
                the_person "I think I look pretty good from behind, why not show it off a little?"
            else:
                $ _photo_reply = "Always happy to show off for a fan! Here are those shots you asked for!"
                the_person "Always happy to show off for a fan! Here are those shots you asked for!"
            "She sends you some private photos. Check her InstaPic album to view them."
            the_person "Enjoy the view, and remember to leave me a nice comment!"
        elif _opinion_ass == 0: #Neutral - underwear
            $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ saved_insta_outfit.strip_bottom_to_underwear()
            if previous_request_level < 2:
                $ _photo_reply = "This was a bit of an unusual request, but I suppose it's harmless. Hope this is what you wanted!"
                the_person "This was a bit of an unusual request, but I suppose it's harmless. Hope this is what you wanted!"
            else:
                $ _photo_reply = "Sure, I can do that for a fan! Here you go!"
                the_person "Sure, I can do that for a fan! Here you go!"
            "She sends you some photos. Check her InstaPic album to view them."
            the_person "Let me know if there is anything else I can do for you!"
        else: #Negative opinion - reluctantly, slut penalty
            $ saved_insta_outfit = the_person.personalize_outfit(insta_wardrobe.pick_random_outfit())
            $ saved_insta_outfit.strip_bottom_to_underwear()
            $ the_person.change_slut(-1)
            if previous_request_level < 2:
                $ _photo_reply = "I guess I can take a few shots, but I'm not really comfortable with this kind of request..."
                the_person "I guess I can take a few shots, but I'm not really comfortable with this kind of request..."
            else:
                $ _photo_reply = "I keep getting these requests... I'm a bit embarrassed honestly."
                the_person "I keep getting these requests... I'm a bit embarrassed honestly."
            "She sends you some reluctant photos. Check her InstaPic album to view them."
            the_person "Please keep these private, I don't want everyone seeing this."

    if the_choice:
        if the_person.has_role(onlyfans_role) and not the_person.onlyfans_known:
            the_person "Oh, and if you liked that, check out my OnlyFanatics page. I'm sure you'll love it!"
            "She sends you a link."
            $ the_person.learn_onlyfans()

        $ mc.business.change_funds(-75, stat = "Shopping")
        if the_person.event_triggers_dict.get("insta_special_request_level", 0) < 2:
            $ the_person.event_triggers_dict["insta_special_request_level"] = 2
        $ add_insta_photo_to_history(the_person, "ass", saved_insta_outfit, saved_insta_position, reply=_photo_reply)
        "You wire her the cash you promised."

    $ insta_dm_cleanup(the_person, photo_received=the_choice)
    return

label dm_view_old_photos(the_person):
    call screen main_choice_display(build_menu_items(build_dm_photos_menu(the_person)), box_xalign = INSTA_PHOTO_ALBUM_BOX_XALIGN)
    if isinstance(_return, dict):
        call dm_replay_photo(the_person, _return) from _call_dm_replay_photo
        call dm_view_old_photos(the_person) from _call_dm_view_old_photos_loop
    else:
        $ clear_scene()
    return

label dm_replay_photo(the_person, photo_entry, is_new = False):
    $ photo_type = photo_entry.get("type", "unknown")
    $ photo_day = photo_entry.get("day", 0)
    $ _replay_outfit = photo_entry.get("outfit", None)
    $ _replay_position = photo_entry.get("position", "stand3")
    $ _views = photo_entry.get("views", 0)
    $ _saved_reply = photo_entry.get("reply", None)
    $ _saved_mc_response = photo_entry.get("mc_response", None)
    $ _photo_source = photo_entry.get("source", "dm")
    $ photo_entry["views"] = _views + 1
    if is_new:
        "[the_person.title] just shared these with you. Take a look!"
    elif _photo_source == "favour":
        "You look back at a photo you took of [the_person.title] (Day [photo_day])."
    else:
        "You scroll back through your saved photos from [the_person.title] (Day [photo_day])."
    if photo_type == "outfit":
        if _replay_outfit is not None:
            $ the_person.apply_outfit(_replay_outfit)
            $ the_person.draw_person(position = _replay_position)
            if _views < 3:
                $ mc.change_locked_clarity(max(1, 10 // (_views + 1)))
            if _saved_reply:
                the_person "[_saved_reply]"
            else:
                the_person "Wearing something special today: a design sent in by a fan!"
            $ the_person.apply_planned_outfit()
        else:
            $ the_person.draw_person()
            "The original outfit wasn't saved, but she still looked great."
            if _views < 3:
                $ mc.change_locked_clarity(max(1, 5 // (_views + 1)))
            $ the_person.apply_planned_outfit()
    elif photo_type == "underwear":
        if _replay_outfit is not None:
            $ the_person.apply_outfit(_replay_outfit)
        else:
            $ the_person.apply_outfit(the_person.personalize_outfit(insta_wardrobe.pick_random_outfit()))
            $ the_person.outfit.strip_to_underwear(avoid_nudity = True)
        $ the_person.draw_person(position = _replay_position)
        if _views < 3:
            $ mc.change_locked_clarity(max(1, 10 // (_views + 1)))
        if _saved_reply:
            the_person "[_saved_reply]"
        else:
            "Quite the risqué shot."
        $ the_person.apply_planned_outfit()
    elif photo_type == "topless":
        if _replay_outfit is not None:
            $ the_person.outfit = _replay_outfit.get_copy()
        else:
            $ the_person.apply_outfit(the_person.personalize_outfit(insta_wardrobe.pick_random_outfit()))
            $ the_person.outfit.strip_to_tits(prefer_half_off = True)
        $ _heel_correction = 0.25 if (the_person.has_high_heels or the_person.has_boots) else 0.0
        $ the_person.draw_person(position = _replay_position, display_transform = character_right(zoom = 2.5, yoffset = 0.65 + _heel_correction))
        if _views < 3:
            $ mc.change_locked_clarity(max(1, 15 // (_views + 1)))
        if _saved_reply:
            the_person "[_saved_reply]"
        else:
            "She wasn't shy about showing off."
        $ the_person.apply_planned_outfit()
    elif photo_type == "ass":
        if _replay_outfit is not None:
            $ the_person.outfit = _replay_outfit.get_copy()
        else:
            $ the_person.apply_outfit(the_person.personalize_outfit(insta_wardrobe.pick_random_outfit()))
            $ the_person.outfit.strip_bottom_to_underwear()
        $ _heel_correction = 0.25 if (the_person.has_high_heels or the_person.has_boots) else 0.0
        $ the_person.draw_person(position = _replay_position, display_transform = character_right(zoom = 2.5, yoffset = 0.30 + _heel_correction))
        if _views < 3:
            $ mc.change_locked_clarity(max(1, 10 // (_views + 1)))
        if _saved_reply:
            the_person "[_saved_reply]"
        else:
            "She showed off that amazing ass."
        $ the_person.apply_planned_outfit()
    elif photo_type == "nude":
        if _replay_outfit is not None:
            $ the_person.outfit = _replay_outfit.get_copy()
        else:
            $ the_person.apply_outfit(the_person.personalize_outfit(insta_wardrobe.pick_random_outfit()))
            $ the_person.outfit.strip_to_tits()
            $ the_person.outfit.remove_shirt()
            $ the_person.outfit.strip_to_vagina()
        $ _heel_correction = 0.25 if (the_person.has_high_heels or the_person.has_boots) else 0.0
        $ the_person.draw_person(position = _replay_position, display_transform = character_right(zoom = 2.5, yoffset = 0.65 + _heel_correction))
        if _views < 3:
            $ mc.change_locked_clarity(max(1, 15 // (_views + 1)))
        if _saved_reply:
            the_person "[_saved_reply]"
        else:
            "She held nothing back for this one."
        $ the_person.apply_planned_outfit()
    elif photo_type == "public":
        if _replay_outfit is not None:
            $ the_person.apply_outfit(_replay_outfit)
        $ the_person.draw_person(position = _replay_position)
        if _views < 3:
            $ mc.change_locked_clarity(max(1, 5 // (_views + 1)))
        if _saved_reply:
            the_person "[_saved_reply]"
        else:
            "She posed for her fans."
        $ the_person.apply_planned_outfit()
    if _saved_mc_response:
        "Your response was: [_saved_mc_response]"
    return

#TODO: Implement this at some point. For now it's more complexity than we need.
label insta_interrupt_check(the_person): # Returns Something???  a callback label or None. The callback should be called after the event.
    if the_person.has_role(sister_role):
        if the_person.is_at(mc.location) and the_person.is_home:
            $ the_person.draw_person()
            "[the_person.title] pulls out her phone, then looks at you."
            the_person "Hey [the_person.mc_title], I got another one of those requests on InstaPic."
            the_person "You know, to see my boobs."
            pass #We're in Lily's room.
        elif the_person.is_home and mc.is_home:
            pass #We're somewhere in the house, probably our room.
    elif the_person.is_at(mc.location):
        if the_person.is_employee and the_person.is_at_office:
            "You notice [the_person.title] look at her phone, then glances around the room as if checking to see if she's being watched."
            "She stands up and heads for the bathroom. You wonder briefly why she's being so secretive."
        else:
            "You notice [the_person.title] look at her phone, then glance up at you."
            $ the_person.draw_person()
            the_person "Back in a moment, just need to take care of this..."
            $ clear_scene()
            "She hurries away, leaving you to wonder what, exactly, she needs to take care of."

    #TODO: Check if the_person is in the same location as you, or if she would come find you (Lily specifically).
    #TODO: If at work you notice her slipping away,
    return
