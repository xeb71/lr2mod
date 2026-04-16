from __future__ import annotations
import builtins
import traceback
import renpy
from game.major_game_classes.game_logic.Action_ren import Action
from game.major_game_classes.game_logic.Role_ren import Role
from game.major_game_classes.game_logic.Room_ren import sex_store
from game.major_game_classes.character_related.Person_ren import Person, list_of_people, perk_system, mc, starbuck, aunt
from game.major_game_classes.clothing_related.Outfit_ren import Outfit
from game.major_game_classes.serum_related.SerumDesign_ren import SerumDesign
from game.helper_functions.game_speed_constants_ren import TIER_2_TIME_DELAY
from game.bugfix_additions.debug_info_ren import write_log

day = 0
time_of_day = 0
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -1 python:
"""

# Sale price multiplier for items placed "on special" (20% discount)
SPECIAL_DISCOUNT = 0.8
# Flat probability (0.0–1.0) that a visitor decides to buy on this visit.
# Normal difficulty: 33%, Hard difficulty: 25%.
BUY_CHANCE_NORMAL = 0.33
BUY_CHANCE_HARD = 0.25

def get_buy_chance() -> float:
    """Return the buy-chance probability appropriate for the current difficulty.
    Falls back to normal difficulty if mc or hard_mode attribute is unavailable."""
    return BUY_CHANCE_HARD if getattr(mc, 'hard_mode', False) else BUY_CHANCE_NORMAL

# Minimum sluttiness an NPC needs to visit the sex shop and consider buying toys
MIN_SHOP_VISITOR_SLUTTINESS = 10
# Multiplier converting a toy design's total_arousal_rating into the minimum NPC
# sluttiness needed to purchase it (same formula shown on the stock screen).
AROUSAL_TO_SLUT_MULTIPLIER = 5
# When True the initial random buy-chance roll is skipped — every visitor
# always enters the candidate-selection loop.  They can still leave empty-
# handed if no toy passes ownership/slot rules or inventory is empty.
FORCE_BUY = False
# Remaining arousal (absolute value) required after a first orgasm for the
# NPC to immediately orgasm a second time with doubled trance chance.
DOUBLE_ORGASM_THRESHOLD = 100

def starbuck_vaginal_skillup_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() < 2 or person.progress.lust_step < 3:
        return False
    if perk_system.has_stat_perk("Vibrating Cock Ring"):
        return "Already Active"
    if not mc.business.has_funds(500):
        return "Requires: $500"
    return mc.is_at(sex_store)

def starbuck_anal_skillup_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() < 2 or person.progress.lust_step < 4:
        return False
    if perk_system.has_stat_perk("Perfect Anal Lube"):
        return "Already Active"
    if not mc.business.has_funds(800):
        return "Requires: $800"
    return mc.is_at(sex_store)

def starbuck_foreplay_skillup_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() < 1 or person.progress.lust_step < 1:
        return False
    if perk_system.has_stat_perk("Small Finger Vibrator"):
        return "Already Active"
    if not mc.business.has_funds(100):
        return "Requires: $100"
    return mc.is_at(sex_store)

def starbuck_oral_skillup_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() < 1 or person.progress.lust_step < 2:
        return False
    if perk_system.has_stat_perk("Stimulating Lip Balm"):
        return "Already Active"
    if not mc.business.has_funds(250):
        return "Requires: $250"
    return mc.is_at(sex_store)

def starbuck_sex_store_investment_one_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() != 0:
        return False
    if not mc.business.has_funds(1000):
        return "Requires: $1000"
    return True

def starbuck_sex_store_investment_two_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() != 1:
        return False
    if person.days_since_event("shop_stage_one_day") > 7:
        if not mc.business.has_funds(5000):
            return "Requires: $5000"
        return True
    return "Wait for her stock to balance out"

def starbuck_sex_store_investment_three_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() != 2:
        return False
    if person.days_since_event("shop_stage_two_day") > 7:
        if not mc.business.has_funds(15000):
            return "Requires: $15000"
        return True
    return "Wait for her stock to balance out"

def starbuck_sex_store_promo_one_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() == 0:
        return False
    if get_shop_promo_stage() != 1.0:
        return False
    if person.progress.love_step < 2 and person.progress.lust_step < 1 and person.progress.obedience_step < 2:
        return "Requires story progression"
    return True

def starbuck_sex_store_promo_two_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() == 0:
        return False
    if get_shop_promo_stage() != 2.0:
        return False
    if person.progress.love_step < 3 and person.progress.lust_step < 2 and person.progress.obedience_step < 3:
        return "Requires story progression"
    return get_shop_promo_stage() == 2.0 and person.days_since_event("promo_event") > TIER_2_TIME_DELAY

def starbuck_sex_store_promo_three_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() < 2:
        return False
    if get_shop_promo_stage() != 3.0 or not person.days_since_event("promo_event") > TIER_2_TIME_DELAY:
        return False
    if person.progress.love_step < 4 and person.progress.lust_step < 3 and person.progress.obedience_step < 4:
        return "Requires story progression"
    # if person.sluttiness < 60:
    #     return "Requires: 60+ sluttiness"
    # if person.love < 50:
    #     return "Requires: 50+ Love"
    return True

def starbuck_sex_store_promo_four_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() < 2:
        return False
    if get_shop_promo_stage() != 4.0 or not person.days_since_event("promo_event") > TIER_2_TIME_DELAY:
        return False
    if person.progress.love_step < 5 and person.progress.lust_step < 3 and person.progress.obedience_step < 5:
        return "Requires story progression"
    # if person.sluttiness < 70:
    #     return "Requires: 70+ sluttiness"
    # if person.love < 60:
    #     return "Requires: 60+ Love"
    return True

def starbuck_sex_store_promo_five_requirement(person: Person):
    if not person.is_at_work or sex_shop_stage() < 3:
        return False
    if get_shop_promo_stage() != 5.0 or not person.days_since_event("promo_event") > TIER_2_TIME_DELAY:
        return False
    if person.progress.love_step < 6 and person.progress.lust_step < 4 and person.progress.obedience_step < 6:
        return "Requires story progression"
    # if person.sluttiness < 90:
    #     return "Requires: 90+ sluttiness"
    # if person.love < 70:
    #     return "Requires: 70+ Love"
    return True

def starbuck_spend_the_night_requirement(person: Person):
    if get_shop_promo_stage() != 6.0 or not person.is_home:
        return False
    if time_of_day != 4:
        return "Only at night"
    return True

def starbuck_close_up_requirement(person: Person):
    if sex_shop_stage() == 0 or not person.is_at_work:
        return False
    if time_of_day != 3:
        return "She closes in the evening"
    return True

def starbuck_anal_fetish_swing_demo_requirement(person: Person):
    return person.is_at_work and person.has_anal_fetish

def sex_shop_cashier_wardrobe_requirement(person: Person):
    return person.progress.obedience_step >= 3

def get_starbuck_role_actions():
    starbuck_vaginal_skillup = Action("Ask about temporarily improving vaginal skill", starbuck_vaginal_skillup_requirement, "starbuck_vaginal_skillup_label")
    starbuck_anal_skillup = Action("Ask about temporarily improving anal skill", starbuck_anal_skillup_requirement, "starbuck_anal_skillup_label")
    starbuck_oral_skillup = Action("Ask about temporarily improving oral skill", starbuck_oral_skillup_requirement, "starbuck_oral_skillup_label")
    starbuck_foreplay_skillup = Action("Ask about temporarily improving foreplay", starbuck_foreplay_skillup_requirement, "starbuck_foreplay_skillup_label")
    starbuck_sex_store_investment_one = Action("Ask about investing in her store", starbuck_sex_store_investment_one_requirement, "starbuck_sex_store_investment_one_label")
    starbuck_sex_store_investment_two = Action("Ask about stock levels", starbuck_sex_store_investment_two_requirement, "starbuck_sex_store_investment_two_label")
    starbuck_sex_store_investment_three = Action("Ask about further investment", starbuck_sex_store_investment_three_requirement, "starbuck_sex_store_investment_three_label")
    starbuck_sex_store_promo_one = Action("Ask how business is going", starbuck_sex_store_promo_one_requirement, "starbuck_sex_store_promo_one_label")
    starbuck_sex_store_promo_two = Action("Ask if advertising is working", starbuck_sex_store_promo_two_requirement, "starbuck_sex_store_promo_two_label")
    starbuck_sex_store_promo_three = Action("Ask if women are coming in", starbuck_sex_store_promo_three_requirement, "starbuck_sex_store_promo_three_label")
    starbuck_sex_store_promo_four = Action("Ask if couples are coming in", starbuck_sex_store_promo_four_requirement, "starbuck_sex_store_promo_four_label")
    starbuck_sex_store_promo_five = Action("Ask if couples are coming in", starbuck_sex_store_promo_five_requirement, "starbuck_sex_store_promo_five_label")
    starbuck_spend_the_night = Action("Spend the night with her", starbuck_spend_the_night_requirement, "starbuck_spend_the_night_label")
    starbuck_close_up = Action("Help close the store {image=time_advance}", starbuck_close_up_requirement, "starbuck_close_up_label")
    starbuck_anal_fetish_swing_demo = Action("Anal Sex Swing Demo", starbuck_anal_fetish_swing_demo_requirement, "starbuck_anal_fetish_swing_demo_label")
    sex_shop_cashier_wardrobe_change = Action("Modify Sex Shop Wardrobe", sex_shop_cashier_wardrobe_requirement, "sex_shop_cashier_wardrobe_label")
    return [starbuck_vaginal_skillup, starbuck_anal_skillup, starbuck_oral_skillup, starbuck_foreplay_skillup, starbuck_sex_store_investment_one,
        starbuck_sex_store_investment_two, starbuck_sex_store_investment_three, starbuck_sex_store_promo_one, starbuck_sex_store_promo_two, starbuck_sex_store_promo_three, starbuck_sex_store_promo_four,
        starbuck_sex_store_promo_five, starbuck_spend_the_night, starbuck_close_up, starbuck_anal_fetish_swing_demo, sex_shop_cashier_wardrobe_change]

def sex_shop_invest_basic_requirement(person: Person):
    if sex_shop_stage() == 0 or not person.is_at_work:
        return False
    if person.event_triggers_dict.get("shop_investment_basic_total", 0) > 5000:
        return "No more investment opportunity."
    if not mc.business.has_funds(1000):
        return "Requires: $1000"
    return True

def sex_shop_invest_advanced_requirement(person: Person):
    if sex_shop_stage() < 2 or not person.is_at_work:
        return False
    if person.event_triggers_dict.get("shop_investment_advanced_total", 0) > 20000:
        return "No more investment opportunity."
    if not mc.business.has_funds(5000):
        return "Requires: $5000"
    return True

def sex_shop_invest_fetish_requirement(person: Person):
    if sex_shop_stage() < 3 or not person.is_at_work:
        return False
    if person.event_triggers_dict.get("shop_investment_fetish_total", 0) > 45000:
        return "No more investment opportunity."
    if not mc.business.has_funds(15000):
        return "Requires: $15000"
    return True

def sex_shop_discuss_selling_requirement(person: Person):
    if sex_shop_stage() == 0 or not person.is_at_work:
        return False
    if person.event_triggers_dict.get("shop_investment_basic_total", 0) <= 0:
        return "Invest in basic inventory first"
    if mc.business.event_triggers_dict.get("engineering_division_policy_avail", False):
        return False
    return True

def sex_store_check_stock_requirement():
    _e_div = globals().get("e_division", None)
    return _e_div is not None and getattr(_e_div, 'visible', False)

# Alias preserving the original name introduced in this PR so that any saves
# that pickled Action objects referencing sex_shop_check_stock_requirement can
# still deserialize correctly if the canonical function is later renamed.
sex_shop_check_stock_requirement = sex_store_check_stock_requirement

def sex_store_actions():
    sex_store_check_stock = Action("Check stock", sex_store_check_stock_requirement, "sex_shop_check_stock_label")
    return [sex_store_check_stock]

def get_sex_shop_invest_role_actions():
    sex_shop_invest_basic = Action("Invest in more basic inventory", sex_shop_invest_basic_requirement, "sex_shop_invest_basic_label")
    sex_shop_invest_advanced = Action("Invest in more advanced inventory", sex_shop_invest_advanced_requirement, "sex_shop_invest_advanced_label")
    sex_shop_invest_fetish = Action("Invest in more fetish inventory", sex_shop_invest_fetish_requirement, "sex_shop_invest_fetish_label")
    sex_shop_discuss_selling = Action("Discuss selling your own inventory", sex_shop_discuss_selling_requirement, "sex_shop_discuss_selling_label")
    return [sex_shop_invest_basic, sex_shop_invest_advanced, sex_shop_invest_fetish, sex_shop_discuss_selling]

def sex_shop_owner_on_turn(person: Person):
    if sex_shop_stage() == 0:
        return
    try:
        toy_revenue = sell_toys_at_sex_shop()
    except Exception as e:
        write_log(f"sell_toys_at_sex_shop error: {e}\n{traceback.format_exc()}")
        return
    if toy_revenue > 0:
        mc.business.add_normal_message(f"Sex shop sold toys for ${toy_revenue:,.0f}!")

def sex_shop_owner_on_day(person: Person): #Use this function to determine if she is going to act on jealous score. also can check for date events here.
    if sex_shop_stage() == 0:
        return
    investment_return = sex_shop_investment_return(person)
    if investment_return > 0:
        mc.business.change_funds(investment_return, stat = "Return On Investments", add_to_log = False)
        mc.business.add_normal_message(f"Sex shop has returned ${investment_return:,.0f} on your investment!")
    daily_voucher_sweep()


def daily_voucher_sweep():
    """At end of each day, guarantee at least one pending voucher is used if possible.

    Finds named clients who still hold an unspent voucher and qualifies for at
    least one in-stock toy (with the voucher's -5 slut reduction applied).
    Processes the purchase for the best candidate (highest sluttiness first).
    Skipped only when no eligible candidate exists — e.g. empty stock or nobody
    qualifies even with the discount.
    """
    if sex_shop_stage() == 0:
        return
    if day % 7 == 6:  # shop closed on Sundays
        return
    toy_inv = getattr(mc.business, 'toy_inventory', {})
    if not toy_inv:
        return

    # Collect the most-recent purchase entry per unique NPC identifier.
    client_log = getattr(mc.business, 'toy_client_log', [])
    seen_ids = set()
    voucher_holders = []
    for entry in reversed(client_log):
        npc_id = entry[3] if len(entry) > 3 else None
        if npc_id is None or npc_id in seen_ids:
            continue
        seen_ids.add(npc_id)
        npc = Person.get_person_by_identifier(npc_id)
        if npc is None:
            continue
        if not getattr(npc, 'has_toy_voucher', False):
            continue
        voucher_holders.append(npc)

    if not voucher_holders:
        return

    # Sort by sluttiness descending — most eligible buyer first.
    voucher_holders.sort(key=lambda p: getattr(p, 'sluttiness', 0), reverse=True)
    for npc in voucher_holders:
        # force_buy=True bypasses the random BUY_CHANCE gate so the purchase
        # is certain if the NPC qualifies for any in-stock toy.
        sale_value = npc_toy_purchase(npc, mc.business, force_buy=True)
        if sale_value > 0:
            mc.business.add_normal_message(
                f"{npc.fname} used her discount voucher and bought a toy for ${sale_value:,.0f}!"
            )
            return  # at least one voucher used today; done

def sex_shop_introduction_requirement(person: Person):
    return person.is_at_work

def sex_shop_unlock_requirement():
    # Daytime hours (1-3) after aunt moves out, only if not already unlocked.
    # Require a day gap so the package event fires the day after the leave event, not the same day.
    return not sex_store.visible and aunt.has_event_day("moved_out") and time_of_day in (1, 2, 3) and day > aunt.get_event_day("moved_out")

def make_sex_shop_owner(person: Person):
    person.event_triggers_dict["shop_progress_stage"] = 0   #For story purposes
    person.event_triggers_dict["shop_investment_total"] = 0 #For calculation purposes
    person.event_triggers_dict["shop_investment_rate"] = 0  #For balance purposes
    person.event_triggers_dict["shop_investment_basic_total"] = 0
    person.event_triggers_dict["shop_investment_advanced_total"] = 0
    person.event_triggers_dict["shop_investment_fetish_total"] = 0
    person.event_triggers_dict["shop_promo_market_rate"] = 0  #For extra income if we've spent a lot of time on promo videos etc.
    sex_shop_invest_role = Role(role_name ="Sex Shop Invest Role", actions = get_sex_shop_invest_role_actions(), on_turn = sex_shop_owner_on_turn, on_move = None, on_day = sex_shop_owner_on_day, hidden = True)
    person.add_role(sex_shop_invest_role)
    person.set_override_schedule(person.home)   # hide her at home until we need her
    person.add_unique_on_room_enter_event(
        Action("Starbuck's Sex Shop", sex_shop_introduction_requirement, "starbuck_greetings", menu_tooltip = "Starbuck's Sex Shop", priority = 30)
    )
    mc.business.add_mandatory_crisis(
        Action("Starbuck unlock sex shop", sex_shop_unlock_requirement, "sex_shop_unlock_label", priority = 30)
    )

def unlock_sex_shop_and_starbuck():
    sex_store.visible = True
    starbuck.set_override_schedule(None)

def sex_shop_investment_return(person: Person):
    if day % 7 == 6:    # not open on sundays
        return 0
    investment_return = 30
    investment_return += int(person.event_triggers_dict.get("shop_investment_basic_total", 0) * get_shop_investment_rate() * 0.01)
    investment_return += int(person.event_triggers_dict.get("shop_investment_advanced_total", 0) * get_shop_investment_rate() * 0.004)
    investment_return += int(person.event_triggers_dict.get("shop_investment_fetish_total", 0) * get_shop_investment_rate() * 0.004)

    #This function returns a variation of 50% to 150%... is this really what we want?
    return builtins.int(investment_return * (renpy.random.random() + .5))    # make it variable rounded to whole dollars

def sex_shop_investment_average_return():
    investment_return = 30
    investment_return += int(starbuck.event_triggers_dict.get("shop_investment_basic_total", 0) * get_shop_investment_rate() * 0.01)
    investment_return += int(starbuck.event_triggers_dict.get("shop_investment_advanced_total", 0) * get_shop_investment_rate() * 0.004)
    investment_return += int(starbuck.event_triggers_dict.get("shop_investment_fetish_total", 0) * get_shop_investment_rate() * 0.004)
    return investment_return


def npc_toy_purchase(npc: Person, business, force_buy=False) -> int:
    """Attempt to have an NPC woman buy a toy from the sex shop.

    NPCs have no money — there is no price check.  Purchase probability
    scales with sluttiness.  She always picks the most demanding toy she
    qualifies for (highest slut level requirement she meets).
    Ownership rules (max 2 toys, one per type):
    - If she owns a toy of the same type (anal/vaginal), she only upgrades if
      the new toy has a strictly higher total_arousal_rating; the old toy is
      removed.
    - If the new toy is a different type she can add it (up to 2 total).
    - She will not buy a toy when she already owns 2 and no upgrade is available.

    Returns the sale value if a purchase was made, 0 otherwise.
    """
    slut = npc.sluttiness

    # BUY_CHANCE probability to consider buying at all.
    # When FORCE_BUY is True or force_buy=True this check is skipped.
    if not FORCE_BUY and not force_buy:
        if renpy.random.random() >= get_buy_chance():
            return 0

    toy_inv = getattr(business, 'toy_inventory', {})
    if not toy_inv:
        return 0

    designs = getattr(business, 'toy_designs', [])
    specials = getattr(business, 'toy_specials', set())

    # Map of toy_type -> currently owned ToyItem of that type (None if not owned)
    npc_toys = getattr(npc, 'toy_inventory', [])
    owned_by_type = {}
    for _t in npc_toys:
        _t_type = getattr(_t, 'toy_type', 'vaginal')
        owned_by_type[_t_type] = _t

    # -----------------------------------------------------------------
    # TOY REQUIREMENTS — this is where each toy is tested against the NPC:
    #   1. Per-toy sluttiness gate: total_arousal_rating * AROUSAL_TO_SLUT_MULTIPLIER
    #      gives the minimum NPC sluttiness needed to buy or consider buying
    #      that toy (matching the formula shown on the design screen).
    #   2. Ownership/slot rules: she can hold at most 2 toys (one per type).
    #      Same-type purchase is only allowed as an upgrade (higher arousal).
    #      Different-type purchase only allowed if she has < 2 toys total.
    # NPCs have no money, so there is no price check — any in-stock toy she
    # qualifies for by sluttiness is considered acceptable.
    # -----------------------------------------------------------------
    # Build candidate list: (toy_name, price, old_toy_to_replace_or_None, min_sluttiness)
    # Each candidate is either an upgrade (same type, higher arousal) or
    # a new type addition (she doesn't yet own that type and has < 2 toys).
    candidates = []
    for toy_name, count in toy_inv.items():
        if count <= 0:
            continue
        design = next((d for d in designs if d.name == toy_name), None)
        if design is None:
            continue
        # 1. Per-toy sluttiness gate (same formula as the design screen).
        #    When on special the threshold is discounted by SPECIAL_DISCOUNT so
        #    NPCs with slightly lower sluttiness can still buy the toy.
        toy_min_slut = getattr(design, 'total_arousal_rating', 0) * AROUSAL_TO_SLUT_MULTIPLIER
        is_special = toy_name in specials
        effective_min_slut = builtins.int(toy_min_slut * SPECIAL_DISCOUNT) if is_special else toy_min_slut
        # A $5 voucher lowers the sluttiness requirement by 5.
        if getattr(npc, 'has_toy_voucher', False):
            effective_min_slut = max(0, effective_min_slut - 5)
        if slut < effective_min_slut:
            continue  # NPC not slutty enough for this toy
        price = builtins.int(design.base_value * SPECIAL_DISCOUNT) if is_special else design.base_value
        new_type = getattr(design.blueprint, 'toy_type', 'vaginal')
        new_arousal = getattr(design, 'total_arousal_rating', 0)

        if new_type in owned_by_type:
            # She already has a toy of this type — only upgrade (higher arousal)
            old_toy = owned_by_type[new_type]
            old_arousal = getattr(getattr(old_toy, 'design', None), 'total_arousal_rating', 0) if old_toy else 0
            if new_arousal <= old_arousal:
                continue  # not an upgrade
            candidates.append((toy_name, price, old_toy, effective_min_slut))
        else:
            # Different type — can add if she has fewer than 2 toys total
            if len(npc_toys) >= 2:
                continue  # already at capacity, no slot for a new type
            candidates.append((toy_name, price, None, effective_min_slut))

    if not candidates:
        return 0

    # Always pick the most demanding toy the NPC qualifies for (highest min_sluttiness).
    # Ties are broken by price descending (higher-value toy wins), then name for stability.
    # Tuple layout: (toy_name[0], price[1], old_toy[2], min_sluttiness[3])
    candidates.sort(key=lambda x: (x[3], x[1], x[0]), reverse=True)
    chosen_name, _chosen_price, old_toy, _chosen_min_slut = candidates[0]

    # withdraw_toy removes the item from stock and returns a ToyItem
    toy_item = business.withdraw_toy(chosen_name)
    if toy_item is None:
        return 0

    # If upgrading, remove the old toy now that we have the replacement in hand
    if old_toy is not None:
        npc.take_toy(old_toy)

    # Give the toy to the NPC
    npc.give_toy(toy_item)

    # Decide carry vs installed: installed-capable toys are worn immediately
    # with a probability that rises with sluttiness
    if "installed" in toy_item.valid_usages:
        install_chance = 0.3 + slut / 200.0  # 30 %–80 % chance to install
        if renpy.random.random() < install_chance:
            npc.install_toy(toy_item)

    # Record the sale (withdraw_toy does not call change_funds)
    # Apply special discount if applicable
    is_special = chosen_name in specials
    sale_value = builtins.int(toy_item.design.base_value * SPECIAL_DISCOUNT) if is_special else toy_item.design.base_value
    # Consume voucher: $5 off the sale price
    if getattr(npc, 'has_toy_voucher', False):
        sale_value = max(0, sale_value - 5)
        npc.has_toy_voucher = False
        npc.voucher_was_used = True
    business.change_funds(sale_value, stat="Toy Sales")
    business.sales_made += sale_value
    if not hasattr(business, 'toys_sold'):
        business.toys_sold = 0
    business.toys_sold += 1
    if not hasattr(business, 'daily_toy_revenue'):
        business.daily_toy_revenue = 0
    business.daily_toy_revenue += sale_value
    log = getattr(business, 'toy_sales_log', {})
    if chosen_name not in log:
        log[chosen_name] = [0, 0]
    log[chosen_name][0] += 1
    log[chosen_name][1] += sale_value - toy_item.design.production_cost
    business.toy_sales_log = log
    # Record named-NPC purchase for client/warranty list
    client_log = getattr(business, 'toy_client_log', [])
    client_log.append([npc.name, chosen_name, day, npc.identifier])
    business.toy_client_log = client_log

    write_log(f"TOY SALE: {npc.name} bought {chosen_name} for ${sale_value}")
    return sale_value


def sell_toys_at_sex_shop() -> int:
    """Let NPCs physically present at the sex shop buy manufactured toys.

    Called from sex_shop_owner_on_turn every turn (not gated on Starbuck's work
    schedule) so the shop sells on every time-slot while it is open.
    Only NPCs who are actually present in the sex_store right now (e.g. because
    the player or her own schedule brought her there) get a purchase attempt.

    The shop is closed on Sundays. Returns total revenue from toy sales.
    """
    if day % 7 == 6:  # closed on Sundays
        return 0

    toy_inv = getattr(mc.business, 'toy_inventory', {})
    if not toy_inv:
        return 0

    total_revenue = 0

    # NPCs physically present at the sex store get a purchase attempt.
    _sex_store = globals().get("sex_store", None)
    if _sex_store is not None:
        for npc in list(_sex_store.people):
            if npc is mc:
                continue
            if getattr(npc, 'sluttiness', 0) < MIN_SHOP_VISITOR_SLUTTINESS:
                continue
            if not getattr(mc.business, 'toy_inventory', {}):
                break
            sale_value = npc_toy_purchase(npc, mc.business)
            total_revenue += sale_value

    return total_revenue


def starbuck_is_business_partner():
    return sex_shop_stage() >= 1

def sex_shop_stage():
    return starbuck.event_triggers_dict.get("shop_progress_stage", 0)

def get_shop_promo_stage():
    return starbuck.event_triggers_dict.get("shop_investment_rate", 1)

def get_shop_investment_rate():
    return starbuck.event_triggers_dict.get("shop_investment_rate", 1) + starbuck.event_triggers_dict.get("shop_promo_market_rate", 0)

#Use this function to check and make sure an outfit is legal to be added to starbuck's uniform wardrobe.
def sex_shop_owner_outfit_check(outfit: Outfit, outfit_type = "full"):
    if not isinstance(outfit, Outfit):
        return False
    if not outfit.is_legal_in_public:
        return False
    if outfit.vagina_visible or outfit.tits_visible:
        return False
    if starbuck.progress.obedience_step < 3:
        if outfit_type == "full":
            return outfit.outfit_slut_score > 30 and outfit.outfit_slut_score <= 50
        elif outfit_type == "over":
            return outfit.overwear_slut_score > 10 and outfit.overwear_slut_score <= 30
        else:
            return outfit.underwear_slut_score > 10 and outfit.underwear_slut_score <= 30
    else:
        if outfit_type == "full":
            return outfit.outfit_slut_score > 30 and outfit.outfit_slut_score <= max(starbuck.sluttiness, 50)
        elif outfit_type == "over":
            return outfit.overwear_slut_score > 10 and outfit.overwear_slut_score <= max(int(starbuck.sluttiness * .6), 30)
        else:
            return outfit.underwear_slut_score > 10 and outfit.underwear_slut_score <= max(int(starbuck.sluttiness * .6), 30)
    return True

def starbuck_serum_is_acceptable_lubricant(serum: SerumDesign):   #Make a lubricant trait and assign it to this.
    return False    #Disabled for now
    #return serum.attention <= 3 and serum.has_trait(energy_drink_serum_trait)

def toggle_toy_special(toy_name: str):
    """Toggle a toy design's 'on special' status on the business.
    While on special, the toy sells at 80% of base price."""
    specials = getattr(mc.business, 'toy_specials', set())
    if toy_name in specials:
        specials.discard(toy_name)
    else:
        specials.add(toy_name)
    mc.business.toy_specials = specials
