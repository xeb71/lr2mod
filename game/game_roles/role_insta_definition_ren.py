from __future__ import annotations
import renpy
from game.game_roles._role_definitions_ren import instapic_role
from game.major_game_classes.clothing_related.Outfit_ren import Outfit
from game.major_game_classes.character_related.Person_ren import Person, mc
from game.major_game_classes.game_logic.Action_ren import Action
from game.helper_functions.game_speed_constants_ren import TIER_1_TIME_DELAY, TIER_2_TIME_DELAY
day = 0
time_of_day = 0
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -2 python:
"""
def insta_would_ban(outfit: Outfit): #Helper function for Insta related stuff. Returns True if an outfit would get you banned from InstaPic.
    return outfit.tits_visible or outfit.vagina_visible

def comment_action_requirement(person: Person):
    return True

def dm_action_requirement(person: Person):
    if person.event_triggers_dict.get("insta_special_request_pending", False):
        return "Waiting for her reply"
    return True

def dm_option_specific_outfit_requirement(person: Person):
    return True

def dm_option_underwear_requirement(person: Person):
    return True

def dm_option_topless_requirement(person: Person):
    return True

def dm_option_nude_requirement(person: Person):
    return True

def dm_option_ass_requirement(person: Person):
    return True

def dm_view_old_photos_requirement(person: Person):
    if not person.event_triggers_dict.get("insta_photo_history", []):
        return "No saved photos"
    return True

def save_public_post_requirement(person: Person):
    if not person.event_triggers_dict.get("insta_last_public_post"):
        return "No photo to save"
    return True

def dm_response_requirement(person: Person):
    if renpy.random.randint(0, 100) < 60 and not person.event_triggers_dict.get("insta_special_request_asap", False): #Respond at a random time, not as soon as possible.
        return False
    elif person.is_at_work and person.obedience >= 160: #Obedient girls don't try and take pics at work.
        return False
    elif person.is_at(mc.location) and mc.location.is_public:
        return False #If she's in the same location as us and we are in public she doesn't take the picture.
    elif mc.is_at(person.home) and person.is_home: #Doesn't do it if she's at home and you're in the room with her (mainly for Lily/Mom)
        return False
    return True

def insta_dm_cleanup(person: Person, photo_received: bool = False): #Resets all the appropriate flags that should be reset after a response has been given.
    person.event_triggers_dict["insta_special_request_pending"] = False
    person.event_triggers_dict["insta_special_request_feasible"] = None
    if person.event_triggers_dict.get("insta_special_request_sis", None):
        person.event_triggers_dict["insta_special_request_sis"] = None
    if person.event_triggers_dict.get("insta_special_request_type", None):
        person.event_triggers_dict["insta_special_request_responded"] = True
    person.event_triggers_dict["insta_dm_photo_available"] = photo_received
    return

_INSTA_PHOTO_DEFAULT_REPLIES = {
    "outfit":    "Wearing something special today: a design sent in by a fan!",
    "underwear": "Happy to do something special for a fan!",
    "topless":   "Hope you enjoy this private look!",
    "ass":       "Hope you like the view!",
    "nude":      "These are just for you!",
}

# MC comment texts keyed by comment_type (mirrors the mc.name lines in comment_description)
_INSTA_MC_COMMENT_TEXT = {
    "obedience_mild":   "You look amazing! I'd love it if you posted more often for your fans.",
    "obedience_strong": "You really should be posting more. Your fans deserve better content from you.",
    "slut_mild":        "Incredible figure! You should definitely show more of it. 🔥",
    "slut_strong":      "Stop hiding it! Your body is way too good to keep covered. Show it off!",
    "love_mild":        "You're absolutely stunning. I can't stop looking at your posts. 💕",
    "love_strong":      "I'm completely obsessed with you. You're perfect in every way. I need to see more of you.",
}

def save_mc_insta_response(person: Person, comment_type: str):
    """If the player just viewed a new DM photo, store their comment text in the latest photo entry."""
    if not person.event_triggers_dict.get("insta_awaiting_mc_response", False):
        return
    history = person.event_triggers_dict.get("insta_photo_history", [])
    if not history:
        return
    mc_text = _INSTA_MC_COMMENT_TEXT.get(comment_type)
    if mc_text:
        history[-1]["mc_response"] = mc_text
    person.event_triggers_dict["insta_awaiting_mc_response"] = False

def add_insta_photo_to_history(person: Person, photo_type: str, outfit: Outfit | None = None, position: str | None = None, reply: str | None = None, source: str = "dm"):
    if "insta_photo_history" not in person.event_triggers_dict:
        person.event_triggers_dict["insta_photo_history"] = []
    entry = {"type": photo_type, "day": day, "views": 0, "source": source}
    if outfit is not None:
        entry["outfit"] = outfit
    if position is not None:
        entry["position"] = position
    # Always persist the reply so dm_replay_photo can display it for old photos.
    # Fall back to a type-appropriate default when the caller did not supply one.
    entry["reply"] = reply if reply is not None else _INSTA_PHOTO_DEFAULT_REPLIES.get(
        photo_type, "Here are those photos you requested!"
    )
    person.event_triggers_dict["insta_photo_history"].append(entry)

def build_insta_menu():
    insta_list = ["Accounts You Know"]
    insta_list.extend((x for x in mc.phone.get_person_list() if x.instapic_known))

    other_options_list = ["Other Options", "Back"]
    return [insta_list, other_options_list]

def build_instapic_comment_actions(person: Person, posted_today: bool):
    display_list = []

    if posted_today:
        obedience_mild_action = Action("Make a mild request", comment_action_requirement, "comment_description", requirement_args = person, args = ["obedience_mild"])
        obedience_strong_action = Action("Make a demanding comment", comment_action_requirement, "comment_description", requirement_args = person, args = ["obedience_strong"])
        slut_mild_action = Action("Compliment her figure", comment_action_requirement, "comment_description", requirement_args = person, args = ["slut_mild"])
        slut_strong_action = Action("Leave a lewd comment", comment_action_requirement, "comment_description", requirement_args = person, args = ["slut_strong"])
        love_mild_action = Action("Leave a flattering comment", comment_action_requirement, "comment_description", requirement_args = person, args = ["love_mild"])
        love_strong_action = Action("Express your obsession", comment_action_requirement, "comment_description", requirement_args = person, args = ["love_strong"])
        save_post_action = Action("Save this photo", save_public_post_requirement, "save_public_post", requirement_args = person)

        comment_list = ["Comment", obedience_mild_action, obedience_strong_action, slut_mild_action, slut_strong_action, love_mild_action, love_strong_action, save_post_action]
        display_list.append(comment_list)

    dm_request_action = Action("Ask for something special", dm_action_requirement, "dm_description", requirement_args = person)
    view_photos_action = Action("View old photos", dm_view_old_photos_requirement, "dm_view_old_photos", requirement_args = person)
    dm_list = ["Direct message her", dm_request_action, view_photos_action]
    display_list.append(dm_list)

    other_list = ["Other Options"]
    other_list.append("Back")
    display_list.append(other_list)
    return display_list

def _dm_request_name(text: str, cost: str, feasible: bool) -> str:
    if feasible:
        return f"{text}\n{{menu_red}}Costs: {cost}{{/menu_red}}"
    return f"{{color=#ff4444}}{text}{{/color}}\n{{menu_red}}Costs: {cost}{{/menu_red}}"

def get_insta_refusal_message() -> str:
    return renpy.random.choice([
        "Sorry, can not do that... yet...",
        "That's a bit more than I'm comfortable with right now.",
        "I'm not quite ready for that kind of request. Maybe later?",
        "Hmm, I don't think I can go that far yet. Sorry!",
        "That's a little too much for me at the moment.",
        "I appreciate the offer, but I'm not ready for that yet.",
        "Maybe when we know each other better? Not ready for that right now.",
    ])

def build_dm_description_actions(person: Person):
    _underwear_feasible = person.effective_sluttiness() + 10 >= 40
    _topless_feasible = person.effective_sluttiness() + 15 >= 50
    _ass_feasible = person.effective_sluttiness() + 10 >= 40
    _nude_feasible = person.effective_sluttiness() + 20 >= 60

    dm_option_specific_outfit_action = Action("Wear a specific outfit\n{menu_red}Costs: $20{/menu_red}", dm_option_specific_outfit_requirement, "dm_option_specific_outfit", requirement_args = person)
    dm_option_underwear_action = Action(_dm_request_name("Show me your underwear", "$50", _underwear_feasible), dm_option_underwear_requirement, "dm_option_underwear", requirement_args = person)
    dm_option_ass_action = Action(_dm_request_name("Show me your ass", "$75", _ass_feasible), dm_option_ass_requirement, "dm_option_ass", requirement_args = person)
    dm_option_topless_action = Action(_dm_request_name("Show me your tits", "$100", _topless_feasible), dm_option_topless_requirement, "dm_option_topless", requirement_args = person)
    dm_option_nude_action = Action(_dm_request_name("Send me some nudes", "$200", _nude_feasible), dm_option_nude_requirement, "dm_option_nude", requirement_args = person)
    dm_options = ["Make a request", dm_option_specific_outfit_action, dm_option_underwear_action, dm_option_ass_action, dm_option_topless_action, dm_option_nude_action]

    other_list = ["Other Options"]
    other_list.append("Back")
    return [dm_options, other_list]

def build_dm_photos_menu(person: Person):
    history = person.event_triggers_dict.get("insta_photo_history", [])
    photo_list = ["Saved Photos"]
    for entry in reversed(history):
        photo_type = entry.get("type", "unknown")
        entry_day = entry.get("day", 0)
        entry_source = entry.get("source", "dm")
        if entry_source == "favour":
            if photo_type == "outfit":
                label = "Contact photo - Day " + str(entry_day)
            else:
                label = photo_type.capitalize() + " snap (personal) - Day " + str(entry_day)
        elif photo_type == "outfit":
            label = "Outfit request - Day " + str(entry_day)
        else:
            label = photo_type.capitalize() + " shots - Day " + str(entry_day)
        photo_list.append([label, entry])
    other_list = ["Other Options", "Back"]
    return [other_list, photo_list]

def add_dm_outfit_response(person: Person, outfit: Outfit):
    mc.business.add_mandatory_crisis(
        Action("DM outfit response", dm_response_requirement, "dm_option_specific_outfit_response", args = [person, outfit], requirement_args = person)
    )

def add_dm_underwear_response(person: Person):
    mc.business.add_mandatory_crisis(
        Action("DM underwear response", dm_response_requirement, "dm_option_underwear_response", args = person, requirement_args = person)
    )

def add_dm_topless_response(person: Person):
    mc.business.add_mandatory_crisis(
        Action("DM topless response", dm_response_requirement, "dm_option_topless_response", args = person, requirement_args = person)
    )

def add_dm_nude_response(person: Person):
    mc.business.add_mandatory_crisis(
        Action("DM topless response", dm_response_requirement, "dm_option_nude_response", args = person, requirement_args = person)
    )

def add_dm_ass_response(person: Person):
    mc.business.add_mandatory_crisis(
        Action("DM ass response", dm_response_requirement, "dm_option_ass_response", args = person, requirement_args = person)
    )
