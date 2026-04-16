init -100 python:
    import functools

    @renpy.pure
    def get_loaded_version():
        if "game_version" in globals():
            loaded_version = game_version
        else:
            loaded_version = "v0.33.3"
        return loaded_version

    # python 3 no longer supports callable, this is an easy fix for all places where it is used
    @renpy.pure
    def callable(obj):
        return hasattr(obj, '__call__')

    @renpy.pure
    def inform_label_not_found(label_name):
        global missing_label_name
        missing_label_name = label_name
        return "missing_label_called"

init -2:
    default persistent.serum_messages = True
    default persistent.stat_change_messages = True
    default persistent.stat_change_fade = True
    default persistent.skill_change_messages = True
    default persistent.clarity_messages = True
    default persistent.energy_messages = True
    default persistent.scene_popups = True

    default persistent.zip_cache_preload = False
    default persistent.zip_cache_size = 0 # default is small size
    default persistent.show_ntr = False     # default turn of NTR
    default persistent.keep_patreon_characters = True  # keep VREN original characters from hire process
    default persistent.mc_noncon_pref = 0   #Default to disabled. MC does not allow himself to be raped in any situation.
    default persistent.mark_unique_as_favourite = True
    default persistent.skip_end_of_day = False
    default missing_label_name = ""

    #don't force low power usage -> let the configure themselves SHIFT-G
    #default preferences.gl_framerate = 30
    #default preferences.gl_powersave = True

init python: # place first on the hijack stack
    add_label_hijack("after_load", "check_save_version")

init 5 python: # add to stack later then other mods
    add_label_hijack("normal_start", "activate_compatibility_fix")
    add_label_hijack("after_load", "update_compatibility_fix")
    add_label_hijack("start", "check_mod_installation")

init 100 python:
    add_label_hijack("normal_start", "store_game_version")

init -5 python:
    # override some of the default settings to improve performance
    config.image_cache_size = None  # when None the image_cache_size_mb value is used
    if is64Bit:
        config.image_cache_size_mb = 768 # fixed at 768 Mb * 4 bytes per pixel
    else:
        config.image_cache_size_mb = 384 # fixed at 384 Mb * 4 bytes per pixel

    # disable gl2 extensions
    if renpy.android or renpy.mobile:
        config.gl2 = False

    # allow for more idle objects
    config.automatic_images = None
    config.check_conflicting_properties = True
    config.optimize_texture_bounds = True
    config.predict_statements = 64 if is64Bit else 32
    config.rollback_length = 64 if is64Bit else 32      # since refactor we can allow a longer rollback history
    config.cache_surfaces = False
    config.predict_screen_statements = False
    config.predict_screens = False
    config.list_compression_length = 200        # increase list compression length for rollback
    config.missing_label_callback = inform_label_not_found
    # disable auto save
    config.autosave_on_choice = False
    config.autosave_on_quit = False
    config.autosave_on_input = False
    config.autosave_frequency = None
    config.has_autosave = True
    config.has_quicksave = True
    config.autosave_slots = 6
    # config.autosave_frequency = 200 # default: 200

    # for DEBUG only (uncomment when you get a cPickle error)
    # config.debug_image_cache = True

    # disable sound settings
    config.has_sound = True
    config.has_music = False
    config.has_voice = False

    # remove full outfits / overwear from default wardrobe that have no shoes or no layer 2 clothing items (nude outfits)
    # to prevent messed up outfits to be used by girls in daily life
    def cleanup_default_wardrobe():
        remove = []
        for outfit in default_wardrobe.outfit_sets + default_wardrobe.overwear_sets:
            if not any(x for x in outfit.feet if x.layer == 2):
                remove.append(outfit)
            elif not any(x for x in outfit.upper_body if x.layer == 3 or x.layer == 4):
                remove.append(outfit)
            elif not any(x for x in outfit.upper_body if x.layer == 3 and x.has_extension) and \
                not any(x for x in outfit.lower_body if x.layer == 3):
                remove.append(outfit)

        if builtins.len(remove) > 10:
            write_log("WARNING: Something is wrong with the clothing layers, too many outfits ({}) are being removed.".format(len(remove)))
        # print("Removing {} outfits from default wardrobe.".format(len(remove)))
        for outfit in remove:
            # print("Removing: " + outfit.name)
            default_wardrobe.remove_outfit(outfit)
        return

    # add code here to keep save games compatible
    def save_game_compatibility():
        # NOTE: Do NOT use function-level "from _ren import X" here.
        # At runtime Ren'Py _ren.py modules are not standard Python modules,
        # and re-importing them triggers top-level code (e.g. "from renpy
        # import str") that only works during Ren'Py init.  All names defined
        # in _ren.py files are already available as store globals.

        if not sarah.has_event_day("day_met") and day >= TIER_1_TIME_DELAY:
            sarah.set_event_day("day_met", TIER_1_TIME_DELAY)
        if not camila.has_event_day("day_met") and not camila.is_stranger:
            camila.set_event_day("day_met", min(day, 7))
        if not iris.has_event_day("day_met") and not iris.is_stranger:
            iris.set_event_day("day_met", min(day, 56))
        if not nora.has_event_day("day_met") and not nora.is_stranger:
            nora.set_event_day("day_met", min(day, 44))
        if not salon_manager.has_event_day("day_met") and not salon_manager.is_stranger:
            salon_manager.set_event_day("day_met", min(day, 44))
        if not candace.has_event_day("day_met") and not candace.is_stranger:
            candace.set_event_day("day_met", min(day, 44))
        if not myra.has_event_day("day_met") and not myra.is_stranger:
            myra.set_event_day("day_met", min(day, 50))
        if not kaya.has_event_day("day_met") and not kaya.is_stranger:
            kaya.set_event_day("day_met", min(day, 50))
        if not naomi.has_event_day("day_met") and not naomi.is_stranger:
            naomi.set_event_day("day_met", min(day, 50))
        if not sakari.has_event_day("day_met") and not sakari.is_stranger:
            sakari.set_event_day("day_met", min(day, 50))

        # Special case: mom's two named children are always Lily and the MC.
        # Old saves may have birthdate=0 placeholder entries generated by the
        # generic loop below; strip those and insert the proper named Kids.
        mom.kids_list[:] = [k for k in mom.kids_list if k.birthdate != 0]
        if not any(k.first_name == lily.name and k.gender == "female" for k in mom.kids_list):
            mom.kids_list.insert(0, Kid(lily.name, lily.last_name, -(lily.age * 360), "female", mom, "Unknown", "Unknown"))
        if not any(k.first_name == mc.name and k.gender == "male" for k in mom.kids_list):
            mom.kids_list.insert(0, Kid(mc.name, mc.last_name, -(22 * 360), "male", mom, "Unknown", "Unknown"))

        # generate placeholder Kid records for old saves that predate kids_list
        for person in list_of_people:
            missing = person.kids - len(person.kids_list)
            if missing <= 0:
                continue
            already_mc_fathered = sum(1 for k in person.kids_list if k.bio_father != "Unknown")
            mc_remaining = max(0, person.sex_record.get("Children with MC", 0) - already_mc_fathered)
            for _ in range(missing):
                kid_gender = renpy.random.choice(("female", "male"))
                if kid_gender == "female":
                    kid_first_name = Person.get_random_name()
                else:
                    kid_first_name = Person.get_random_male_name()
                if mc_remaining > 0:
                    father_name = f"{mc.name} {mc.last_name}"
                    mc_remaining -= 1
                else:
                    father_name = "Unknown"
                person.kids_list.append(
                    Kid(
                        first_name=kid_first_name,
                        last_name=person.last_name,
                        birthdate=0,
                        gender=kid_gender,
                        mother=person,
                        father=father_name,
                        bio_father=father_name,
                    )
                )

        # Recreate canonical Personality instances so Personality._REGISTRY is
        # populated for saves that predate the gain-multiplier attributes.
        # Personality objects pickled in older saves lack love_gain_multiplier etc.;
        # __getattr__ resolves them by looking up the canonical instance in
        # _REGISTRY, which is a class-level (non-pickled) dict rebuilt here.
        list_of_personalities.clear()
        init_base_personalities()
        init_special_personalities()

        # replace broken 'stand' object with enhanced floor object
        for x in list_of_places:
            stand= next((x for x in x.objects if x.name == "stand"), None)
            if stand:
                x.objects.remove(stand)

            floor= next((x for x in x.objects if x.name == "floor"), None)
            if floor:
                if not "Stand" in floor.traits:
                    floor.traits.append("Stand")
            else:
                x.objects.append(make_floor())

        # Initialise like_men/like_women for saves that predate this attribute.
        for person in list_of_people:
            if not hasattr(person, "like_men"):
                person.like_men = 5
            if not hasattr(person, "like_women"):
                person.like_women = 0
            if not hasattr(person, "vaginal_stimulator"):
                person.vaginal_stimulator = 0
            if not hasattr(person, "anal_stimulator"):
                person.anal_stimulator = 0
            if not hasattr(person, "like_vaginal"):
                person.like_vaginal = 0
            if not hasattr(person, "like_anal"):
                person.like_anal = 0

        # Aunt Rebecca dislikes vaginal stimulation initially (-5). Clamp saves
        # that received the generic 0 default so her story arc is preserved.
        # Only reset when exactly 0 (the generic init value) — do NOT touch saves
        # where like_vaginal has been legitimately trained to a positive value.
        if not aunt.is_stranger and aunt.like_vaginal == 0:
            aunt.like_vaginal = -5

        # Remove the legacy "vaginal sex" sexy_opinion from Rebecca — her
        # dislike is tracked via like_vaginal and the dealbreaker trainable
        # should not trigger for her (she has a custom story arc instead).
        if not aunt.is_stranger:
            aunt.sexy_opinions.pop("vaginal sex", None)

        # Ensure cousin (Gabrielle) is registered as aunt's daughter.
        # Saves created before this relationship was explicitly established
        # would see aunt.kids=1 but no matching entry in town_relationships,
        # which could cause generic-daughter generation to trigger for her.
        if not aunt.is_stranger and town_relationships.get_relationship_type(aunt, cousin) is None:
            town_relationships.update_relationship(aunt, cousin, "Daughter", "Mother")

        # Initialise engineering department attributes for saves that predate it.
        if not hasattr(mc.business, 'e_uniform'):
            mc.business.e_uniform = Wardrobe(mc.business.name + " Engineering Wardrobe")
        if not hasattr(mc.business, 'e_serum'):
            mc.business.e_serum = None
        if not hasattr(mc.business, '_e_div'):
            mc.business._e_div = mc.business._h_div
        if not hasattr(mc.business, '_engineering_team'):
            mc.business._engineering_team = MappedList(Person, all_people_in_the_game)
        if not hasattr(mc.business, 'toy_blueprints'):
            mc.business.toy_blueprints = []
        if not hasattr(mc.business, 'toy_designs'):
            mc.business.toy_designs = []
        # Strip any auto-generated plain ToyDesigns (no attributes) that were
        # created by the old toy_design_progress() before this was changed.
        # All user-created designs have at least one attribute (battery required).
        mc.business.toy_designs = [
            d for d in mc.business.toy_designs
            if len(getattr(d, 'attributes', [])) > 0
        ]
        if not hasattr(mc.business, 'active_toy_research'):
            mc.business.active_toy_research = None
        if not hasattr(mc.business, 'toy_attributes'):
            mc.business.toy_attributes = []
        if not hasattr(mc.business, 'active_attribute_research'):
            mc.business.active_attribute_research = None
        if not hasattr(mc.business, 'printers'):
            mc.business.printers = [Printer("Basic 3D Printer", speed_modifier=1.0)]
        if not hasattr(mc.business, 'toy_inventory'):
            mc.business.toy_inventory = {}
        if not hasattr(mc.business, 'toys_manufactured'):
            mc.business.toys_manufactured = 0
        if not hasattr(mc.business, 'toys_sold'):
            mc.business.toys_sold = 0
        if not hasattr(mc.business, 'toy_sales_log'):
            mc.business.toy_sales_log = {}
        if not hasattr(mc.business, 'daily_toy_revenue'):
            mc.business.daily_toy_revenue = 0
        if not hasattr(mc.business, 'toy_client_log'):
            mc.business.toy_client_log = []
        if not hasattr(mc.business, 'toy_specials'):
            mc.business.toy_specials = set()
        if not hasattr(mc.business, 'research_complete_notifications'):
            mc.business.research_complete_notifications = []
        # Initialise toy inventory and usage counters on Person for saves that predate them.
        for person in list_of_people:
            if not hasattr(person, "toy_inventory"):
                person.toy_inventory = []
            if not hasattr(person, "toy_use_count"):
                person.toy_use_count = 0
            if not hasattr(person, "toy_orgasm_count"):
                person.toy_orgasm_count = 0
            if not hasattr(person, "toy_trance_count"):
                person.toy_trance_count = 0
            if not hasattr(person, "toy_switchoff_count"):
                person.toy_switchoff_count = 0
            if not hasattr(person, "has_toy_voucher"):
                person.has_toy_voucher = False
            if not hasattr(person, "voucher_was_used"):
                person.voucher_was_used = False
            if not hasattr(person, "favour_count_small"):
                person.favour_count_small = 0
            if not hasattr(person, "favour_count_small_success"):
                person.favour_count_small_success = person.favour_count_small
            if not hasattr(person, "favour_count_moderate"):
                person.favour_count_moderate = 0
            if not hasattr(person, "favour_count_moderate_success"):
                person.favour_count_moderate_success = person.favour_count_moderate
            if not hasattr(person, "favour_count_large"):
                person.favour_count_large = 0
            if not hasattr(person, "has_phone_photo"):
                person.has_phone_photo = False
            if not hasattr(person, "engineering_skill"):
                person.engineering_skill = 0
            # Ensure existing ToyItem objects have an intensity attribute.
            for _toy in getattr(person, 'toy_inventory', []):
                if not hasattr(_toy, 'intensity'):
                    _toy.intensity = 1 if getattr(_toy, 'installed', False) else 0
                if not hasattr(_toy, 'switched_off_until'):
                    _toy.switched_off_until = 0

        # Ensure client log entries have an identifier field (4th element).
        # Old saves stored only [name, toy_name, day]; append None for those.
        _clog = getattr(mc.business, 'toy_client_log', [])
        for _entry in _clog:
            if len(_entry) < 4:
                _entry.append(None)

        # Ensure engineering division room exists for old saves.
        # Must run BEFORE init_job_list() so engineering_job gets the correct location.
        # Room.actions is serialized; saves made before engineering was added
        # won't have the engineering division room.
        if "e_division" not in globals() or globals()["e_division"] is None:
            globals()["e_division"] = Room("eng_div", "Engineering Division", "Engineering_Background",
                [make_floor(), make_desk(), make_window(), make_chair(), make_wall()],
                actions = engineering_division_actions(),
                map_pos = [0,0], lighting_conditions = standard_indoor_lighting,
                privacy_level = 2)
            list_of_places.append(globals()["e_division"])
            office_hub.locations.append(globals()["e_division"])

        # Always fix background_name in case an old save serialized the misspelled value.
        globals()["e_division"].background_name = "Engineering_Background"

        # Always refresh e_division actions so saves with old action names
        # (engineering_design_action_description, engineering_attribute_research_action_description)
        # pick up the current combined engineering_research_action_description.
        globals()["e_division"].actions = ActionList(engineering_division_actions())

        # Update _e_div to point to the real engineering division.
        # Older saves (or saves that used the old compat code) had _e_div = _h_div (office).
        if not hasattr(mc.business, '_e_div') or mc.business._e_div == mc.business._h_div:
            mc.business._e_div = globals()["e_division"].identifier
        # Always clear the cached e_div property so the next access (e.g. in init_job_list)
        # recomputes from the (now-correct) _e_div.  The cache may hold a stale Room
        # if it was computed before _e_div was updated or serialised in an old save.
        mc.business.__dict__.pop("e_div", None)

        # Re-initialise duty and job globals so engineering definitions exist.
        # Clear lists first to prevent duplicates, then recreate all duties.
        import sys
        _duty_mod = sys.modules.get("game.game_roles.business_roles._duty_definitions_ren")
        general_duties_list.clear()
        general_rd_duties.clear()
        general_market_duties.clear()
        general_supply_duties.clear()
        general_production_duties.clear()
        general_hr_duties.clear()
        # For engineering duties: clear if present (save made with engineering),
        # or create a new list in both store and module (old save without it).
        if "general_engineering_duties" in globals():
            general_engineering_duties.clear()
        else:
            globals()["general_engineering_duties"] = []
        # Also sync the module namespace so init_duty_lists() global ref works.
        if _duty_mod is not None:
            _duty_mod.general_engineering_duties = globals()["general_engineering_duties"]
        init_duty_lists()
        init_job_list()
        # Ensure engineering_job is registered in industrial_home_hub so that
        # engineers hired on old saves have their home tracked by the hub and
        # appear on the map / navigate correctly.
        _eng_job = globals().get("engineering_job", None)
        if _eng_job is not None and _eng_job not in industrial_home_hub.jobs:
            industrial_home_hub.jobs.append(_eng_job)
        # Clear cached employee properties so they pick up new job definitions.
        mc.business._clear_employee_cache()
        # Patch existing engineers: update seniority_level to 2, point job_definition to the
        # current engineering_job (so available_duties reflects current options), and enforce
        # research/manufacture exclusivity.
        _research_duty_names = {"Toy Design Research"}
        _manufacture_duty_name = "3D Print Manufacturing"
        _attribute_rd_name = "Toy Attribute R&D"
        _current_engineering_job = globals().get("engineering_job", None)
        for _emp in mc.business.employee_list:
            for _job in _emp.jobs:
                if hasattr(_job, 'job_definition') and getattr(_job.job_definition, 'job_title', '') == "Engineer":
                    # Update job_definition to the freshly-built engineering_job so that
                    # available_duties no longer includes removed duties like "Toy Attribute R&D".
                    if _current_engineering_job is not None:
                        _job.job_definition = _current_engineering_job
                    if _job.seniority_level < 2:
                        _job.seniority_level = 2
                    # Remove the removed "Toy Attribute R&D" duty from any existing engineer jobs.
                    _job.duties = [d for d in _job.duties if d.duty_name != _attribute_rd_name]
                    _has_research = any(d.duty_name in _research_duty_names for d in _job.duties)
                    _has_manufacture = any(d.duty_name == _manufacture_duty_name for d in _job.duties)
                    if _has_research and _has_manufacture:
                        _job.duties = [d for d in _job.duties if d.duty_name != _manufacture_duty_name]
        # Initialise toy blueprints and attributes if not yet populated.
        if not mc.business.toy_blueprints:
            init_toy_blueprints(mc.business)
        if not mc.business.toy_attributes:
            init_toy_attributes(mc.business)

        # Patch power values on all existing blueprint objects to match current design.
        # This ensures saves made before power values were added/revised stay consistent.
        _bp_power_map = {
            "Basic Vibrator": -4, "Basic Dildo": -4, "Basic Plug": -4,
            "Remote Control Vibrator": -3, "Realistic Dildo": -3, "Vibrating Plug": -3,
            "Luxury Wand Massager": -2, "Couples Toy Set": -2,
        }
        for _bp in mc.business.toy_blueprints:
            if _bp.name in _bp_power_map:
                _bp.power = _bp_power_map[_bp.name]

        # Patch arousal_rating on all existing blueprint objects.
        _bp_arousal_map = {
            "Basic Vibrator": 2, "Basic Dildo": 2, "Basic Plug": 1,
            "Intensity Control Vibrator": 3, "Remote Control Vibrator": 3,
            "Realistic Dildo": 3, "Vibrating Plug": 3,
            "Luxury Wand Massager": 4, "Couples Toy Set": 4,
        }
        for _bp in mc.business.toy_blueprints:
            if not hasattr(_bp, 'arousal_rating'):
                _bp.arousal_rating = _bp_arousal_map.get(_bp.name, 0)

        # Rename "100m Waterproofing" to "Extra Robust" and update its description.
        for _attr in mc.business.toy_attributes:
            if _attr.name == "100m Waterproofing":
                _attr.name = "Extra Robust"
                _attr.desc = "Rated to 100 meters water depth and shock proof — ideal for more active users."
                _attr.identifier = generate_identifier((_attr.name, "attribute"))
        # Update Temperature Control's requires list to use renamed Extra Robust.
        _robust_attr = next((_a for _a in mc.business.toy_attributes if _a.name == "Extra Robust"), None)
        _temp_ctrl = next((_a for _a in mc.business.toy_attributes if _a.name == "Temperature Control"), None)
        if _robust_attr and _temp_ctrl:
            _temp_ctrl.requires = [_a for _a in _temp_ctrl.requires if _a.name not in ("100m Waterproofing", "Extra Robust")]
            _temp_ctrl.requires.append(_robust_attr)

        # Patch power_add values on all existing attribute objects.
        _attr_power_map = {
            "Basic Battery": 5, "Enhanced Battery": 10, "Power Cell": 15,
            "Bluetooth Module": -1,
            "Cellular Module": -2, "LED Lighting": -1, "Extra Robust": 0,
            "Electro Heat Transfer": 5,
            "Pressure Sensors": -1,
            "GPS Tracker": -3, "Electro Stimulator": -4, "Temperature Control": -3,
            "Diagnostics Module": -3, "AI-Adaptive Patterns": -6,
            "Haptic Feedback": -4, "Pressure Point Stimulator": -5,
        }
        for _attr in mc.business.toy_attributes:
            if _attr.name in _attr_power_map:
                _attr.power_add = _attr_power_map[_attr.name]

        # Patch arousal_rating_add on all existing attribute objects.
        _attr_arousal_map = {
            "Basic Battery": 0, "Enhanced Battery": 0, "Power Cell": 0,
            "Bluetooth Module": 0, "Internet Connection, with Bluetooth": 0,
            "LED Lighting": 0, "Extra Robust": 0, "Electro Heat Transfer": 0,
            "Pressure Sensors": 1,
            "GPS Tracker": 0, "Electro Stimulator": 5, "Temperature Control": 2,
            "Diagnostics Module": 0, "AI-Adaptive Patterns": 3,
            "Haptic Feedback": 2, "Pressure Point Stimulator": 3,
        }
        for _attr in mc.business.toy_attributes:
            if not hasattr(_attr, 'arousal_rating_add'):
                _attr.arousal_rating_add = _attr_arousal_map.get(_attr.name, 0)

        # Correct arousal_rating_add values that have been revised from old definitions.
        _attr_arousal_correction = {
            "Electro Stimulator": 5,
        }
        for _attr in mc.business.toy_attributes:
            if _attr.name in _attr_arousal_correction:
                _attr.arousal_rating_add = _attr_arousal_correction[_attr.name]

        # Patch research_needed values on existing attribute objects.
        _attr_research_map = {
            "Bluetooth Module": 100,
        }
        for _attr in mc.business.toy_attributes:
            if _attr.name in _attr_research_map:
                _attr.research_needed = _attr_research_map[_attr.name]

        # Add any newly introduced attributes that are missing from existing saves.
        _existing_attr_names = {_a.name for _a in mc.business.toy_attributes}

        if "Basic Battery" not in _existing_attr_names:
            _new_bb = ToyAttribute("Basic Battery",
                "A compact rechargeable cell providing reliable power for entry-level designs.",
                research_needed=150, production_cost_add=1, value_add=5, power_add=5)
            mc.business.toy_attributes.insert(0, _new_bb)
            _existing_attr_names.add("Basic Battery")

        if "Enhanced Battery" not in _existing_attr_names:
            _basic_bat = next((_a for _a in mc.business.toy_attributes if _a.name == "Basic Battery"), None)
            _new_eb = ToyAttribute("Enhanced Battery",
                "High-capacity lithium pack with extended runtime and faster charging.",
                research_needed=400, requires=_basic_bat if _basic_bat else [],
                production_cost_add=2, value_add=10, power_add=10)
            mc.business.toy_attributes.insert(1, _new_eb)
            _existing_attr_names.add("Enhanced Battery")

        if "Power Cell" not in _existing_attr_names:
            _enh_bat = next((_a for _a in mc.business.toy_attributes if _a.name == "Enhanced Battery"), None)
            _new_pc = ToyAttribute("Power Cell",
                "Advanced solid-state cell delivering sustained high-output power for premium components.",
                research_needed=750, requires=_enh_bat if _enh_bat else [],
                production_cost_add=4, value_add=18, power_add=15)
            mc.business.toy_attributes.insert(2, _new_pc)
            _existing_attr_names.add("Power Cell")

        if "Bluetooth Module" not in _existing_attr_names:
            _new_bt = ToyAttribute("Bluetooth Module",
                "Adds short-range wireless connectivity for device-to-device control.",
                research_needed=100, production_cost_add=1, value_add=6, power_add=-1)
            # Insert right after the 3 battery entries
            _bt_insert_pos = next(
                (_i for _i, _a in enumerate(mc.business.toy_attributes)
                 if _a.name not in ("Basic Battery", "Enhanced Battery", "Power Cell")),
                len(mc.business.toy_attributes))
            mc.business.toy_attributes.insert(_bt_insert_pos, _new_bt)
            _existing_attr_names.add("Bluetooth Module")

        if "Extra Robust" not in _existing_attr_names:
            _new_er = ToyAttribute("Extra Robust",
                "Rated to 100 meters water depth and shock proof — ideal for more active users.",
                research_needed=200, production_cost_add=2, value_add=8, power_add=0)
            # Insert after LED Lighting if present, else after Bluetooth Module
            _er_insert_pos = next(
                (_i + 1 for _i, _a in enumerate(mc.business.toy_attributes)
                 if _a.name == "LED Lighting"),
                next((_i + 1 for _i, _a in enumerate(mc.business.toy_attributes)
                 if _a.name == "Bluetooth Module"),
                len(mc.business.toy_attributes)))
            mc.business.toy_attributes.insert(_er_insert_pos, _new_er)
            _existing_attr_names.add("Extra Robust")

        if "Electro Heat Transfer" not in _existing_attr_names:
            _new_eht = ToyAttribute("Electro Heat Transfer",
                "A thermoelectric module that harvests heat from operation and feeds it back as charge, adding +5 to the power budget.",
                research_needed=300, production_cost_add=2, value_add=10, power_add=5)
            # Insert after Extra Robust
            _eht_insert_pos = next(
                (_i + 1 for _i, _a in enumerate(mc.business.toy_attributes)
                 if _a.name == "Extra Robust"),
                len(mc.business.toy_attributes))
            mc.business.toy_attributes.insert(_eht_insert_pos, _new_eht)
            _existing_attr_names.add("Electro Heat Transfer")

        if "Electro Shocker" not in _existing_attr_names:
            _req_es = next((_a for _a in mc.business.toy_attributes if _a.name == "Electro Stimulator"), None)
            _new_eshock = ToyAttribute("Electro Shocker",
                "High-voltage shock pads that deliver sharp, punishing electrical bursts — deeply unpleasant and highly effective.",
                research_needed=750, requires=_req_es if _req_es else [],
                production_cost_add=5, value_add=22, power_add=-4, arousal_rating_add=-5)
            # Insert after Electro Stimulator
            _eshock_insert_pos = next(
                (_i + 1 for _i, _a in enumerate(mc.business.toy_attributes)
                 if _a.name == "Electro Stimulator"),
                len(mc.business.toy_attributes))
            mc.business.toy_attributes.insert(_eshock_insert_pos, _new_eshock)
            _existing_attr_names.add("Electro Shocker")

        # Patch module_space_add on existing attribute objects that predate the field.
        for _attr in mc.business.toy_attributes:
            if not hasattr(_attr, 'module_space_add'):
                _attr.module_space_add = 0

        if "Extension Module" not in _existing_attr_names:
            _req_robust = next((_a for _a in mc.business.toy_attributes if _a.name == "Extra Robust"), None)
            _new_ext = ToyAttribute("Extension Module",
                "A modular chassis expansion that adds two additional component slots at the cost of one. Requires a robust casing to support the extra hardware.",
                research_needed=350, requires=_req_robust if _req_robust else [],
                production_cost_add=3, value_add=12, power_add=-1, arousal_rating_add=0,
                module_space_add=2)
            mc.business.toy_attributes.append(_new_ext)
            _existing_attr_names.add("Extension Module")

        # Add any newly introduced blueprints that are missing from existing saves.
        _existing_bp_names = {_bp.name for _bp in mc.business.toy_blueprints}

        if "Egg Vibrator" not in _existing_bp_names:
            _req_basic_vib = next((_bp for _bp in mc.business.toy_blueprints if _bp.name == "Basic Vibrator"), None)
            _new_ev = ToyBlueprint("Egg Vibrator",
                "A small, discreet insertable vibrating egg. Designed to be worn throughout the day.",
                research_needed=500, tier=3, requires=_req_basic_vib if _req_basic_vib else [],
                production_cost=5, base_value=30, power=-3, arousal_rating=3,
                usage=("installed",))
            # Insert after the Intensity Control Vibrator (formerly Remote Control Vibrator)
            _icv_idx = next(
                (_i for _i, _bp in enumerate(mc.business.toy_blueprints)
                 if _bp.name in ("Intensity Control Vibrator", "Remote Control Vibrator")),
                len(mc.business.toy_blueprints) - 1)
            mc.business.toy_blueprints.insert(_icv_idx + 1, _new_ev)
            _existing_bp_names.add("Egg Vibrator")

        if "Vibrating Plug XL" not in _existing_bp_names:
            _req_vib_plug = next((_bp for _bp in mc.business.toy_blueprints if _bp.name == "Vibrating Plug"), None)
            _new_vpxl = ToyBlueprint("Vibrating Plug XL",
                "An oversized vibrating plug with a powerful motor and extra-wide base for secure wear.",
                research_needed=750, tier=3, requires=_req_vib_plug if _req_vib_plug else [],
                production_cost=9, base_value=55, power=-2, arousal_rating=4,
                usage=("installed",), toy_type="anal")
            mc.business.toy_blueprints.append(_new_vpxl)
            _existing_bp_names.add("Vibrating Plug XL")

        # Patch toy_type on all existing blueprint objects that predate the field.
        _bp_type_map = {
            "Basic Plug": "anal",
            "Vibrating Plug": "anal",
            "Vibrating Plug XL": "anal",
        }
        for _bp in mc.business.toy_blueprints:
            if not hasattr(_bp, 'toy_type'):
                _bp.toy_type = _bp_type_map.get(_bp.name, "vaginal")

        # Remove engineering actions from the main office if they were added by
        # earlier compatibility code.  They now belong to e_division.
        for label in [
            "engineering_design_action_description",
            "engineering_research_action_description",
            "engineering_manufacture_action_description",
            "engineering_attribute_research_action_description",
            "engineering_manage_printers_description",
            "engineering_manage_blueprints_description",
            "engineering_manage_attributes_description",
        ]:
            office.remove_action(label)

        # Add the Engineering Division policy to special_policies_list if missing
        # (saves created before this policy was added won't have it).
        # NOTE: engineering_division_policy global only exists after init_special_policies()
        # runs (new-game path). For old saves it never ran, so we check by name and
        # create the Policy object directly using the requirement/unlock functions that
        # ARE available as store globals (defined in init 2 python: blocks).
        _sp_list = globals().get("special_policies_list", None)
        if _sp_list is not None:
            _eng_pol_name = "Open Engineering Division"
            if not any(getattr(p, 'name', None) == _eng_pol_name for p in _sp_list):
                _PolicyCls = globals().get("Policy", None)
                _req_fn = globals().get("engineering_division_policy_requirement", None)
                _unlock_fn = globals().get("unlock_engineering_division", None)
                if _PolicyCls is not None:
                    _new_eng_pol = _PolicyCls(
                        name = _eng_pol_name,
                        desc = "Renovate an area of your office building into a dedicated Engineering Division where your team can design and manufacture sex toys to sell through Cara's shop.",
                        cost = 10000,
                        requirement = _req_fn,
                        on_buy_function = _unlock_fn,
                    )
                    globals()["engineering_division_policy"] = _new_eng_pol
                    _sp_list.append(_new_eng_pol)

        # Refresh sex_store actions so old saves pick up the Check Stock location action.
        _sex_store = globals().get("sex_store", None)
        if _sex_store is not None:
            _sex_store.actions = ActionList(sex_store_actions())

        # Backfill reply field for InstaPic photo history entries that predate the reply feature.
        # Entries created before the reply was introduced lack the "reply" key.
        for _person in list_of_people:
            _hist = _person.event_triggers_dict.get("insta_photo_history", [])
            for _pe in _hist:
                if "reply" in _pe:
                    continue
                _pt = _pe.get("type", "")
                if _pt == "ass":
                    _op = getattr(getattr(_person, "opinion", None), "showing_her_ass", 0) or 0
                    if _op >= 2:
                        _pe["reply"] = "I love showing off my ass, it's one of my best features! Enjoy!"
                    elif _op >= 1:
                        _pe["reply"] = "I think I look pretty good from behind, why not show it off a little?"
                    elif _op == 0:
                        _pe["reply"] = "This was a bit of an unusual request, but I suppose it's harmless. Hope this is what you wanted!"
                    else:
                        _pe["reply"] = "I guess I can take a few shots, but I'm not really comfortable with this kind of request..."
                elif _pt == "topless":
                    _op = getattr(getattr(_person, "opinion", None), "showing_her_tits", 0) or 0
                    if _op >= 2:
                        _pe["reply"] = "I love showing off my tits, they're my best feature! Hope you enjoy!"
                    elif _op >= 1:
                        _pe["reply"] = "I think I look pretty good topless, why not show off a little?"
                    elif _op == 0:
                        _pe["reply"] = "This was a bit of an unusual request, but I suppose it's harmless. Hope this is what you wanted!"
                    else:
                        _pe["reply"] = "I guess I can take a few shots, but I'm not really comfortable with this kind of request..."
                elif _pt == "underwear":
                    _slut = _person.effective_sluttiness() if hasattr(_person, "effective_sluttiness") else 0
                    if _slut >= 40:
                        _pe["reply"] = "I had a lot of fun taking these. Always happy to do something special for a fan!"
                    else:
                        _pe["reply"] = "This was a little out of my comfort zone, but I couldn't say no to a fan!"
                elif _pt == "nude":
                    _slut = _person.effective_sluttiness() if hasattr(_person, "effective_sluttiness") else 0
                    if _slut >= 60:
                        _pe["reply"] = "I love getting requests like this! Of course I can take some shots for you!"
                    else:
                        _pe["reply"] = "I wouldn't normally do something like this, but I suppose I can give it a try. Be nice!"
                elif _pt == "outfit":
                    _pe["reply"] = "Wearing something special today: a design sent in by a fan!"
                else:
                    # Unknown / pre-feature photo type – supply a generic reply so the
                    # gallery always shows something when the photo is replayed.
                    _pe["reply"] = "Here are those photos you requested!"

        # Ensure starbuck's Sex Shop Invest Role has the current "Discuss selling" action.
        # If the role doesn't exist at all (very old saves where make_sex_shop_owner was
        # never called), create it from the current definition.
        _starbuck = globals().get("starbuck", None)
        if _starbuck is not None:
            _invest_role = _starbuck.get_role_reference("Sex Shop Invest Role")
            if _invest_role is None:
                # Very old save — the role was never created.  Build it from the
                # current definition (includes all up-to-date actions).
                # Do NOT call make_sex_shop_owner(): that resets event_triggers.
                _invest_role = Role(
                    role_name="Sex Shop Invest Role",
                    actions=get_sex_shop_invest_role_actions(),
                    on_turn=sex_shop_owner_on_turn,
                    on_move=None,
                    on_day=sex_shop_owner_on_day,
                    hidden=True,
                )
                _starbuck.add_role(_invest_role)
            else:
                if not _invest_role.actions.has_action("sex_shop_discuss_selling_label"):
                    _invest_role.add_action(Action(
                        "Discuss selling your own inventory",
                        sex_shop_discuss_selling_requirement,
                        "sex_shop_discuss_selling_label",
                    ))
                # Remove any stale check_stock action from old saves where it lived on the role.
                _invest_role.actions.remove_action("sex_shop_check_stock_label")

        # --- Tennis sponsorship event: register morning crisis for old saves ---
        # The crisis is normally registered in create_jennifer_character() which
        # only runs during new-game start.  For old saves we need to add it here
        # so the event can fire.
        if not mom.event_triggers_dict.get("tennis_sponsorship_done", False):
            if not mc.business.has_queued_crisis("mom_tennis_sponsorship_label"):
                add_mom_tennis_sponsorship_action()

        # --- Tennis leaders & NPC members for old saves ---
        # Leaders and NPC members are now created lazily when the sponsorship
        # event fires.  For old saves where the event has ALREADY been completed
        # we still need to back-fill them so the roster isn't empty.
        write_log("[tennis compat] tennis_sponsorship_done=%s perky_leader=%s", mom.event_triggers_dict.get("tennis_sponsorship_done", False), perky_leader)
        if mom.event_triggers_dict.get("tennis_sponsorship_done", False):
            write_log("[tennis compat] sponsorship done; perky_leader is None: %s", perky_leader is None)
            if perky_leader is None:
                write_log("[tennis compat] creating tennis leaders from scratch")
                create_tennis_leaders()
                write_log("[tennis compat] after create: perky_leader=%s in_list=%s dest=%s", perky_leader, perky_leader in list_of_people, perky_leader.get_destination(day % 7, time_of_day) if perky_leader else None)
            else:
                # Captains already exist but may have old schedules.
                # Re-apply the correct schedule: Tue-Sun, early morning & morning.
                write_log("[tennis compat] captains exist; re-applying schedules and ensuring in list_of_people")
                perky_leader.set_schedule(sports_center_tennis_courts, day_slots=[1, 2, 3, 4, 5, 6], time_slots=[0, 1])
                showoff_leader.set_schedule(sports_center_tennis_courts, day_slots=[1, 2, 3, 4, 5, 6], time_slots=[0, 1])
                commando_leader.set_schedule(sports_center_tennis_courts, day_slots=[1, 2, 3, 4, 5, 6], time_slots=[0, 1])
                # Fix homes: captains should live in downtown apartments, not at
                # the tennis courts or purgatory.
                _compat_homes = [generic_bedroom_1, generic_bedroom_2, generic_bedroom_3]
                for _compat_idx, _compat_leader in enumerate([perky_leader, showoff_leader, commando_leader]):
                    _compat_home = _compat_homes[_compat_idx]
                    if _compat_leader.home in (purgatory, sports_center_tennis_courts):
                        _compat_leader._set_home(_compat_home)
                    _compat_home.add_person(_compat_leader)
                write_log("[tennis compat] perky_leader in list_of_people: %s", perky_leader in list_of_people)
                write_log("[tennis compat] showoff_leader in list_of_people: %s", showoff_leader in list_of_people)
                write_log("[tennis compat] commando_leader in list_of_people: %s", commando_leader in list_of_people)
                write_log("[tennis compat] perky_leader dest(day=%s,time=%s)=%s", day % 7, time_of_day, perky_leader.get_destination(day % 7, time_of_day))
                write_log("[tennis compat] showoff_leader dest(day=%s,time=%s)=%s", day % 7, time_of_day, showoff_leader.get_destination(day % 7, time_of_day))
                write_log("[tennis compat] commando_leader dest(day=%s,time=%s)=%s", day % 7, time_of_day, commando_leader.get_destination(day % 7, time_of_day))
            write_log("[tennis compat] tennis_teams perky=%s showoff=%s commando=%s", bool(tennis_teams["perky"]), bool(tennis_teams["showoff"]), bool(tennis_teams["commando"]))
            if not tennis_teams["perky"] and not tennis_teams["showoff"] and not tennis_teams["commando"]:
                write_log("[tennis compat] creating NPC members")
                create_tennis_npc_members()
            # Also ensure mom's tennis court schedule is set for old saves
            # where setup_mom_tennis_schedule() may not have been called.
            write_log("[tennis compat] calling setup_mom_tennis_schedule")
            setup_mom_tennis_schedule()

        # Ensure the tennis limited wardrobe exists for ALL saves (not just
        # those where sponsorship is done).  The validation function itself
        # already checks whether the person is at the tennis courts, so the
        # wardrobe is harmless when present but unused.
        if not any(getattr(w, 'validation_func', None) == tennis_wardrobe_validation for w in limited_wardrobes):
            write_log("[tennis compat] adding tennis wardrobe to limited_wardrobes")
            limited_wardrobes.append(LimitedWardrobe("Default_Tennis_Wardrobe", 6, tennis_wardrobe_validation, allow_personalisation=False, sluttiness_alpha=True))

        # Patch sluttiness_alpha onto any existing tennis wardrobe added by older compat code.
        _tennis_lw = next((w for w in limited_wardrobes if getattr(w, 'validation_func', None) == tennis_wardrobe_validation), None)
        if _tennis_lw is not None and not getattr(_tennis_lw, 'sluttiness_alpha', False):
            _tennis_lw.sluttiness_alpha = True
            write_log("[tennis compat] enabled sluttiness_alpha on existing tennis wardrobe")

        # Also set the standalone store variable so _get_tennis_outfit() can
        # find it.  Look it up from the collection we just ensured exists.
        if not hasattr(renpy.store, 'limited_tennis_wardrobe') or renpy.store.limited_tennis_wardrobe is None:
            if _tennis_lw is not None:
                renpy.store.limited_tennis_wardrobe = _tennis_lw
                write_log("[tennis compat] set limited_tennis_wardrobe store variable")

        # Ensure the pool limited wardrobe exists for ALL saves.
        # The validation function checks whether the person is at the pool.
        if not any(getattr(w, 'validation_func', None) == pool_wardrobe_validation for w in limited_wardrobes):
            write_log("[pool compat] adding pool wardrobe to limited_wardrobes")
            limited_wardrobes.append(LimitedWardrobe("Default_Pool_Wardrobe", 6, pool_wardrobe_validation, allow_personalisation=True, sluttiness_alpha=True))

        # Patch sluttiness_alpha onto any existing pool wardrobe added by older compat code.
        _pool_lw = next((w for w in limited_wardrobes if getattr(w, 'validation_func', None) == pool_wardrobe_validation), None)
        if _pool_lw is not None and not getattr(_pool_lw, 'sluttiness_alpha', False):
            _pool_lw.sluttiness_alpha = True
            write_log("[pool compat] enabled sluttiness_alpha on existing pool wardrobe")

        # Also set the standalone store variable so _get_pool_outfit() can
        # find it.  Look it up from the collection we just ensured exists.
        if not hasattr(renpy.store, 'limited_pool_wardrobe') or renpy.store.limited_pool_wardrobe is None:
            if _pool_lw is not None:
                renpy.store.limited_pool_wardrobe = _pool_lw
                write_log("[pool compat] set limited_pool_wardrobe store variable")

        # Clear any per-person cached tennis/pool outfits so the new transparency
        # factor is recomputed on the next visit (relevant when loading old saves
        # that cached outfits before sluttiness_alpha was enabled).
        for _p in list_of_people:
            if getattr(_p, '_tennis_outfit', None) is not None:
                _p._tennis_outfit = None
            if getattr(_p, '_pool_outfit', None) is not None:
                _p._pool_outfit = None

        # Always reload limited wardrobe XMLs to pick up layout/content changes
        # (e.g. tennis wardrobe changed from FullSets to OverwearSets).
        # Also rebuilds _sorted to fix any stale ordering from save.
        if hasattr(limited_wardrobes, 'reload_wardrobes'):
            limited_wardrobes.reload_wardrobes()

        # Re-register the "Ask about her research interests" action on Nora for
        # saves where the boss-trait phase already fired before this action was
        # introduced. The condition mirrors add_study_person_for_nora_actions():
        # the university already has 'nora_special_research' registered.
        if university.has_action('nora_special_research') and not nora.has_action('nora_ask_trait_hint_label'):
            nora.add_action(
                Action("Ask about her research interests", nora_ask_trait_hint_requirement, "nora_ask_trait_hint_label",
                menu_tooltip = "Ask Nora what kind of person she would find most interesting to study next.")
            )
            write_log("[nora compat] registered nora_ask_trait_hint_label action on nora")

        return

label check_mod_installation(stack):
    $ execute_hijack_call(stack)
    return

label activate_compatibility_fix(stack):
    # make sure we store the crisis tracker in the save game
    $ crisis_tracker_dict = {}
    $ execute_hijack_call(stack)
    return

label update_compatibility_fix(stack):
    if not "crisis_tracker_dict" in globals():
        $ crisis_tracker_dict = {}

    $ save_game_compatibility()

    $ execute_hijack_call(stack)
    return

label store_game_version(stack):
    $ game_version = config.version
    $ execute_hijack_call(stack)
    return

label check_save_version(stack):
    $ loaded_version = get_loaded_version()

    if "game_version" in globals() and loaded_version != game_version:
        "Warning" "You are loading a game created by a previous build ([loaded_version]), you might run into errors because of this. Before reporting errors, please start a new game with and see if the problem persists."
    $ execute_hijack_call(stack)
    return

label missing_label_called(arg1 = None, Arg2 = None):
    "System" "Something went wrong, the game called label '[missing_label_name]', but this label does not exist."
    return
