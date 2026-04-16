


init 2 python:
    def emily_university_lunch_requirement(person):
        if not emily.event_triggers_dict.get("tutor_enabled", False):
            return False
        if emily.event_triggers_dict.get("university_lunch_done", False):
            return False
        return (person.is_at(university_hub) and mc.is_at(university_hub)
                and emily.love >= 20 and time_of_day == 1)


# Story progression actions
    def add_emily_university_lunch_action():
        emily_university_lunch_action = Action("Lunch Date with Emily", emily_university_lunch_requirement, "emily_university_lunch_label", priority = 30)
        emily.add_unique_on_room_enter_event(emily_university_lunch_action)
        return



label emily_university_lunch_label(the_person):
    $ the_person = emily
    $ the_person.draw_person()
    "[the_person.possessive_title!c] spots you near the entrance and waves enthusiastically."
    the_person "Hey! I didn't know you'd be on campus today."
    mc.name "Just taking care of some things. How's studying going?"
    the_person "Pretty well, actually! I've been putting your advice to work."
    "[the_person.possessive_title!c] grins."
    the_person "Hey, since you're here — have you eaten yet? There's a pretty good place near the library."
    menu:
        "Sure, I've got time":
            mc.name "Yeah, why not. Lead the way."
            $ the_person.draw_person(emotion = "happy")
            the_person "Great! Come on then."
            $ the_person.change_stats(love = 3, happiness = 5)
            "You spend the next hour over coffee and sandwiches, talking about everything and nothing in particular."
            "[the_person.title] is easy company. Smart, curious, and surprisingly funny when she's relaxed."
            mc.name "You know, you're pretty good at this talking thing when you're not panicking about exams."
            the_person "Hey! I'm always good company."
            mc.name "Sure you are."
            "[the_person.possessive_title!c] throws a napkin at you, grinning."
            the_person "We should do this more often. It's way better than just studying."
            $ mc.business.change_funds(-20, stat = "Teaching") #Lunch tab
            $ the_person.event_triggers_dict["university_lunch_done"] = True

        "Can't today, I'm busy":
            mc.name "I'd love to, but I've got too much on today."
            "[the_person.possessive_title!c] nods, undeterred."
            the_person "Next time then!"
            $ the_person.event_triggers_dict["university_lunch_done"] = True
    return
