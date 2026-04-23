from __future__ import annotations
import renpy
from game.major_game_classes.game_logic.Room_ren import sex_store
from game.major_game_classes.character_related.Person_ren import Person, town_relationships, mc, alexia, camila, candace, nora, starbuck
from game.major_game_classes.game_logic.Action_ren import Action

day = 0
time_of_day = 0
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init 10 python:
"""

######################
# Camila and Alexia #
######################

def camila_alexia_boudoir_setup_reminder_requirement():
    if mc_business_has_expensive_camera() and alexia_is_model():
        if time_of_day == 2 and camila.event_triggers_dict.get("boudoir_stage", 0) == 0:  # afternoon
            return True
    return False

def camila_alexia_boudoir_setup_intro_requirement(person: Person):
    return (
        person.is_at_work
        and person.is_available
        and mc_business_has_expensive_camera()
        and alexia_is_model()
        and camila.event_triggers_dict.get("help_with_lingerie", False)
        and camila.event_triggers_dict.get("love_path", None) is not None
        and camila.event_triggers_dict.get("boudoir_stage", 0) == 0
        and not camila.event_triggers_dict.get("boudoir_scheduled", False)
    )

def camila_alexia_boudoir_intro_setup():   #Use this function to add the appropriate labels to the game for when boudoir photos can begin.
    if camila.event_triggers_dict.get("boudoir_stage", 0) > 0 or camila.event_triggers_dict.get("boudoir_scheduled", False):
        return
    if mc_business_has_expensive_camera() and alexia_is_model():
        alexia.add_unique_on_room_enter_event(
            Action("Arrange photos with Alexia", camila_alexia_boudoir_setup_intro_requirement, "camila_alexia_boudoir_setup_intro_label", priority = 30)
        )
    else:
        mc.business.add_mandatory_crisis(
            Action("Boudoir Reminder", camila_alexia_boudoir_setup_reminder_requirement, "camila_alexia_boudoir_setup_reminder_label")
        )

def mc_business_has_expensive_camera():
    return mc.business.event_triggers_dict.get("has_expensive_camera", False)

def alexia_is_model():
    return alexia == mc.business.company_model

def alexia_has_flirty_ad():
    if alexia_is_model():
        return alexia.event_triggers_dict.get("camera_flirt", False)
    return False

def alexia_has_underwear_ad():
    if alexia_is_model():
        return alexia.event_triggers_dict.get("camera_flash", False)
    return False

def alexia_has_nude_ad():
    if alexia_is_model():
        return alexia.event_triggers_dict.get("camera_naked", False)
    return False

def alexia_has_blowjob_ad():
    if alexia_is_model():
        return alexia.event_triggers_dict.get("camera_suck", False)
    return False

def alexia_has_sex_ad():
    if alexia_is_model():
        return alexia.event_triggers_dict.get("camera_fuck", False)
    return False

def camila_boudoir_get_stage():
    return camila.event_triggers_dict.get("boudoir_stage", 0)

def camila_nora_goal_sync_requirement(person: Person):
    return (
        person.is_at_work
        and person.is_available
        and person.event_triggers_dict.get("obedience_ass_man", False)
        and nora.event_triggers_dict.get("nora_contracts_intro_complete", False)
        and not person.event_triggers_dict.get("nora_goal_teamup_intro", False)
        and not person.event_triggers_dict.get("nora_goal_teamup_scheduled", False)
    )

def add_camila_nora_goal_sync_action():
    camila.add_unique_on_talk_event(
        Action("Compare notes with Nora", camila_nora_goal_sync_requirement, "camila_nora_goal_sync_setup_label", priority = 30)
    )

def camila_nora_goal_sync_intro_requirement():
    return (
        time_of_day == 2  # afternoon
        and camila.event_triggers_dict.get("nora_goal_teamup_scheduled", False)
        and nora.event_triggers_dict.get("nora_contracts_intro_complete", False)
    )

def add_camila_nora_goal_sync_intro_action():
    mc.business.add_mandatory_crisis(
        Action("Camila Meets Nora", camila_nora_goal_sync_intro_requirement, "camila_nora_goal_sync_intro_label", priority = 30)
    )


########################
# Candace and Starbuck #
########################

def starbuck_candace_product_demo_requirement(person: Person):
    return starbuck.is_at(sex_store) and person.is_at_office

def add_starbuck_candace_product_demo_action():
    candace.add_unique_on_talk_event(
        Action("Candace helps with product demo", starbuck_candace_product_demo_requirement, "starbuck_candace_product_demo_label", priority = 30)
    )

def starbuck_candace_recurring_event_requirement(person: Person):
    if day % 7 != 5 or time_of_day != 3:
        return False
    return starbuck.is_at(sex_store) and candace.is_at(sex_store)

def add_starbuck_candace_recurring_event_action():
    starbuck.add_unique_on_room_enter_event(
        Action("Candace and Starbuck hanging out", starbuck_candace_recurring_event_requirement, "starbuck_candace_recurring_event_label", priority = 30)
    )

def update_candace_starbuck_relationship():
    town_relationships.update_relationship(candace, starbuck, "Best Friend")
    candace.set_override_schedule(sex_store, day_slots = [5], time_slots = [3])
    starbuck.set_override_schedule(sex_store, day_slots = [5], time_slots = [3])
    candace.set_event_day("friends_with_starbuck")
