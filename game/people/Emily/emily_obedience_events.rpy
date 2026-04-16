


init 2 python:
    def emily_ask_about_serum_requirement():
        if not emily.event_triggers_dict.get("student_wants_serum", False):
            return False
        return emily.is_available and (mc.is_at_office or mc.is_home or mc.is_at(university_hub))


# Story progression actions
    def add_emily_ask_about_serum_action():
        emily_ask_about_serum_action = Action("Emily gets curious about your serums", emily_ask_about_serum_requirement, "emily_ask_about_serum_label")
        mc.business.add_mandatory_crisis(emily_ask_about_serum_action)
        return



label emily_ask_about_serum_label():
    $ the_person = emily
    $ the_person.draw_person()
    "[the_person.possessive_title!c] catches up with you and pulls you aside."
    the_person "Hey! So, um... I know this is a weird thing to ask, but..."
    "[the_person.title] fidgets, picking at her sleeve."
    the_person "That stuff you gave me when we were studying. The serum. I was really hoping I could have some more."
    mc.name "Oh? What makes you say that?"
    the_person "I don't know exactly, I just felt like I was thinking so much more clearly after. Like things just... clicked."
    the_person "I ended up doing way better in my classes that week. Way better than usual."
    "[the_person.possessive_title!c] looks up at you hopefully."
    the_person "Please? I really think it helps."
    menu:
        "Give her a dose of serum" if mc.inventory.has_serum:
            mc.name "Alright. Just don't go making a habit of asking everyone in the lab for special favours."
            call give_serum(the_person) from _call_give_serum_emily_serum_crisis
            if _return:
                $ the_person.change_stats(love = 2, obedience = 1)
                $ the_person.event_triggers_dict["student_given_serum"] = the_person.event_triggers_dict.get("student_given_serum", 0) + 1
                the_person "Thank you so much! I'll make sure to bring it up at our next session."
                mc.name "Good. Now, focus on your studies."
                the_person "I will! I promise."
                $ the_person.event_triggers_dict["student_wants_serum"] = False
            else:
                mc.name "Actually, I don't seem to have any on me. I'll bring some to the next study session."
                the_person "Oh okay, thank you for checking."
                $ the_person.event_triggers_dict["student_wants_serum"] = False

        "Give her a dose of serum\n{menu_red}Requires: Serum{/menu_red} (disabled)" if not mc.inventory.has_serum:
            pass

        "Not right now":
            mc.name "I don't have any on me at the moment. We can look at it next time we study."
            "[the_person.possessive_title!c] nods, looking a little disappointed but understanding."
            the_person "Okay, sure. No problem."
            $ the_person.event_triggers_dict["student_wants_serum"] = False

    return
