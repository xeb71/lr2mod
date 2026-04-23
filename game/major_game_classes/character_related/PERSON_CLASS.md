# `Person` — Functional Reference

> **Files:**
> - `game/major_game_classes/character_related/Person_ren.py` (6 109 lines, `init -2`)
> - `game/major_game_classes/character_related/_person_stat_mixin_ren.py` (600 lines, `init -3`)

---

## 1. Overview

`Person` is the central NPC data-model class.  Every female character in the game — both named story characters and procedurally generated randoms — is a `Person` instance stored in the module-level list `list_of_people`.

A single instance records everything that needs to be known about one character:

| Concern | What it covers |
|---|---|
| Identity | Name, age, physical appearance, dialogue character |
| Location | Current room, home, schedule, follow-MC flag |
| Relationships | Relationship status, significant other, family links |
| Stats | Love, sluttiness, obedience, suggestibility, happiness, arousal, energy |
| Skills | Work skills (HR / Marketing / Research / Production / Supply) and sex skills |
| Opinions | Per-topic opinion scores (normal and "sexy"); taboo tracking |
| Wardrobe | Outfit, wardrobe, planned outfit, uniform handling |
| Serums | Active serum effects, tolerance, stat change methods |
| Story | `Story_Tracker`, `Progression`, event-trigger dictionary |
| Jobs / Roles | Primary / secondary / side jobs, special roles, duties |
| Sex Mechanics | Arousal, pregnancy, fertility, sex record, fetishes |
| Display | Ren'Py `Character` object, sprite compositing, animations |

---

## 2. Class Hierarchy

```
PersonStatMixin   (_person_stat_mixin_ren.py, init -3)
        │
    Person        (Person_ren.py,              init -2)
```

`Person` inherits from `PersonStatMixin` via Python's normal MRO.  The mixin provides 47 methods covering serum administration, all stat/skill change helpers, and the five work-potential properties.  `Person` itself defines the remaining ~532 methods.

---

## 3. Module-Level Globals (`Person_ren.py`)

| Name | Type | Purpose |
|---|---|---|
| `list_of_people` | `list[Person]` | All active Person instances |
| `list_of_patreon_characters` | `list[Person]` | Patreon-only characters |
| `list_of_instantiation_functions` | `list[Callable]` | Functions called to create each NPC at game start |
| `tan_images_dict` | `dict[str, Clothing]` | Cached tan-layer Clothing objects |
| `body_images_dict` | `dict[str, Clothing]` | Cached body Clothing objects |
| `town_relationships` | `RelationshipArray` | Global inter-character relationship store |
| `character_right` | ATL transform | Default on-screen character position |
| `clothing_fade` / `fast_clothing_fade` | ATL transform | Clothing change animations |
| `day` | `int` | Current in-game day (Ren'Py store) |
| `time_of_day` | `int` | 0 = morning, 1 = afternoon, 2 = night |
| `report_log` | `dict[str, int]` | Sex-scene reporting dict (injected by sex mechanic) |
| `GAME_SPEED` | `int` | Current speed setting (0–3) |

### Stat-tier threshold constants

| Constant | Value | Usage |
|---|---|---|
| `SUGGESTIBILITY_TIER_THRESHOLDS` | `(15, 35, 55, 75)` | `suggest_tier` property (tiers 0–4) |
| `OBEDIENCE_TIER_THRESHOLDS` | `(100, 120, 140, 160, 180)` | `obedience_tier` property (tiers 0–5) |
| `SLUTTINESS_TIER_STEP` | `20` | `sluttiness_tier` step size |
| `SLUTTINESS_TIER_OFFSET` | `5` | `sluttiness_tier` baseline offset |

---

## 4. Class-Level Constants

All defined on the `Person` class body (before `__init__`).

### Stat ranges

| Constant | Value | Meaning |
|---|---|---|
| `_final_stat_floor` | 0 | Minimum value for Cha / Int / Focus after serum growth |
| `_initial_stat_floor` | 1 | Minimum starting value for Cha / Int / Focus |
| `_initial_stat_ceiling` | 5 | Maximum starting value for Cha / Int / Focus |
| `_final_skill_floor` | 0 | Minimum work-skill value |
| `_initial_skill_floor` | 1 | Minimum starting work-skill value |
| `_initial_skill_ceiling` | 5 | Maximum starting work-skill value |
| `_final_sex_skill_floor` | 0 | Minimum sex-skill value |
| `_initial_sex_skill_floor` | 1 | Minimum starting sex-skill |
| `_initial_sex_skill_ceiling` | 5 | Maximum starting sex-skill |
| `_final_happiness_floor` | 0 | Minimum happiness |
| `_initial_happiness_floor` | 90 | Starting happiness minimum |
| `_initial_happiness_ceiling` | 110 | Starting happiness maximum |
| `_initial_suggestibility_floor` | 0 | Starting suggestibility minimum |
| `_initial_suggestibility_ceiling` | 15 | Starting suggestibility maximum |
| `_initial_sluttiness_floor` | 0 | Starting sluttiness minimum |
| `_initial_sluttiness_ceiling` | 10 | Starting sluttiness maximum |
| `_final_love_floor` | −100 | Minimum love |
| `_final_love_ceiling` | 100 | Maximum love |
| `_final_obedience_floor` | 0 | Minimum obedience |
| `_initial_obedience_floor` | 90 | Starting obedience minimum |
| `_initial_obedience_ceiling` | 110 | Starting obedience maximum |

### Age & height ranges

| Constant | Value |
|---|---|
| `_initial_age_floor` | 18 |
| `_initial_age_ceiling` | 50 |
| `_final_age_floor` | 18 |
| `_final_age_ceiling` | 60 |
| `_teen_age_ceiling` | 19 |
| `_old_age_floor` | 40 |
| `_height_step` | 0.015 (= 1 inch in game units) |
| `_initial_height_floor` | 5′0″ equivalent |
| `_initial_height_ceiling` | 5′10″ equivalent |
| `_final_height_floor` | 4′0″ equivalent |
| `_final_height_ceiling` | 7′0″ equivalent |
| `_short_height_ceiling` | 5′3″ equivalent |
| `_tall_height_floor` | 5′9″ equivalent |

### Other class-level data

| Constant | Purpose |
|---|---|
| `_base_list_of_relationships` | Weighted list for random SO relationship status |
| `_large_tit_minimum` | `"D"` — minimum cup for "large" |
| `_huge_tit_minimum` | `"E"` — minimum cup for "huge" |
| `_small_tit_maximum` | `"C"` — maximum cup for "small" |
| `_tiny_tit_maximum` | `"AA"` — maximum cup for "tiny" |
| `_list_of_tits` | Weighted cup-size list for random generation |
| `_list_of_names` / `_list_of_last_names` / `_list_of_male_names` | Name pools |
| `_list_of_hairs` / `_list_of_faces` / `_list_of_eyes` | Appearance pools |
| `_list_of_skins` | Weighted skin-type list |
| `_list_of_body_types` | `["thin_body", "standard_body", "curvy_body"]` |
| `_coffee_list` | Coffee preference strings |
| `_record_skill_map` | Maps sex-record keys → which sex skill to raise |
| `_record_opinion_map` | Maps sex-record keys → which opinions to update |
| `_opinions_list` / `_sexy_opinions_list` | All valid opinion topic strings |
| `_location_clear_keys` | Attribute names flushed from the `cached_property` cache on location change |

---

## 5. Instance Attributes

All set in `__init__` (lines 785–1034).

### Identity / dialogue

| Attribute | Type | Description |
|---|---|---|
| `type` | `str` | `"random"` or `"story"` |
| `func_name` | `str` | Lower-cased name used for dynamic label calls |
| `char` | `Character` | Ren'Py `Character` object used for all dialogue |
| `name` | `str` | First name |
| `last_name` | `str` | Last name |
| `identifier` | `int` | Unique integer derived from (name, last_name, age) |
| `title` / `possessive_title` / `mc_title` | `str` | Display titles (formatted with font/colour tags) |
| `what_font` / `who_font` | `str` | Dialogue body / name font |
| `what_color` | `str` | Dialogue colour hex code |
| `text_modifiers` | `list[Callable]` | Functions applied to dialogue text |
| `event_triggers_dict` | `dict` | General-purpose event-state storage |

### Physical appearance

| Attribute | Type | Description |
|---|---|---|
| `age` | `int` | Character age |
| `body_type` | `str` | `"thin_body"`, `"standard_body"`, `"curvy_body"` (or `"standard_preg_body"`) |
| `tits` | `str` | Cup size: `"AA"` … `"FF"` |
| `height` | `float` | Height in game units (multiply by 1/0.015 for inches) |
| `face_style` | `str` | Face image identifier |
| `hair_style` | `Clothing` | Hair-style Clothing object |
| `hair_colour` | `tuple` | `(name_str, [r, g, b, a])` |
| `pubes_style` | `Clothing` | Pubic-hair Clothing object |
| `pubes_colour` | `None` | Reserved; not currently used |
| `skin` | `str` | `"white"`, `"black"`, or `"tan"` |
| `tan` | `str` | Tan-style identifier |
| `eyes` | `tuple` | `(name_str, [r, g, b, a])` |

### Core stats

| Attribute | Type | Range | Description |
|---|---|---|---|
| `love` | `int` | −100 … 100 | Romantic attachment to MC |
| `_sluttiness` | `int` | 0 … 100 | Base sluttiness (use `sluttiness` property) |
| `situational_sluttiness` | `dict` | — | `{source: (amount, description)}` |
| `_obedience` | `int` | 0 … 300 | Base obedience (use `obedience` property) |
| `situational_obedience` | `dict` | — | `{source: (amount, description)}` |
| `happiness` | `int` | 0 … 300 | Happiness / morale |
| `suggestibility` | `int` | 0 … 100 | Susceptibility to the MC's serums / trance |
| `suggest_bag` | `list[int]` | — | Active suggestion-effect stack |
| `arousal` | `int` | 0 … `max_arousal` | Sexual arousal level |
| `max_arousal` | `int` | — | Arousal cap (default 100) |
| `novelty` | `int` | 0 … 100 | Novelty factor; decays with repeated sex acts |

### Personality stats

| Attribute | Type | Range |
|---|---|---|
| `charisma` | `int` | 0 + |
| `int` | `int` | 0 + |
| `focus` | `int` | 0 + |
| `charisma_debt` / `int_debt` / `focus_debt` | `int` | Negative-balance tracking |

### Work skills & energy

| Attribute | Type |
|---|---|
| `hr_skill` / `market_skill` / `research_skill` / `production_skill` / `supply_skill` | `int` (1–5 init) |
| `work_experience` | `int` |
| `salary_modifier` | `float` (default 1.0) |
| `productivity_adjustment` | `float` (default 1.0) |
| `energy` / `max_energy` | `int` (default 100) |

### Sex skills

| Attribute | Key | Range |
|---|---|---|
| `sex_skills` | `"Foreplay"`, `"Oral"`, `"Vaginal"`, `"Anal"` | 0–5 |

### Serum / stat-effect state

| Attribute | Type | Description |
|---|---|---|
| `serum_effects` | `list[SerumDesign]` | Currently active serums |
| `_serum_tolerance` | `int` | Base tolerance (max active serums; default 2) |
| `total_serum_count` | `int` | Cumulative serums ever given |

### Location & movement

| Attribute | Type | Description |
|---|---|---|
| `_location` | `int \| None` | Room identifier for current location |
| `_home` | `int \| None` | Room identifier for home |
| `_follow_mc` | `bool` | Whether she is currently following the MC |
| `schedule` | `Schedule` | Regular weekly schedule |
| `override_schedule` | `Schedule` | Mandatory schedule (overrides regular) |

### Relationship & family

| Attribute | Type | Description |
|---|---|---|
| `relationship` | `str` | `"Single"`, `"Girlfriend"`, `"Fiancée"`, or `"Married"` |
| `SO_name` | `str \| None` | Significant other's name |
| `kids` | `int` | Number of children |
| `personality` | `Personality` | Current personality object. Exposes `love_gain_multiplier`, `happiness_gain_multiplier`, `obedience_gain_multiplier`, and `slut_gain_multiplier` (floats, default 1.0) that scale positive stat gains during interactions. |

### Opinions

| Attribute | Type | Description |
|---|---|---|
| `opinions` | `dict[str, list]` | `{topic: [score (−2…2), known (bool)]}` — general topics |
| `sexy_opinions` | `dict[str, list]` | Same structure — sexual/kink topics |

### Wardrobe & outfit

| Attribute | Type | Description |
|---|---|---|
| `wardrobe` | `Wardrobe \| None` | Full clothing wardrobe |
| `base_outfit` | `Outfit` | Default/fallback outfit |
| `outfit` | `Outfit \| None` | Currently worn outfit |
| `planned_outfit` | `Outfit \| None` | Planned non-work outfit |
| `next_day_outfit` | `Outfit \| None` | Tomorrow's outfit |

### Jobs & roles

| Attribute | Type | Description |
|---|---|---|
| `primary_job` | `ActiveJob \| None` | Main job |
| `secondary_job` | `ActiveJob \| None` | Fills schedule gaps left by primary |
| `side_job` | `ActiveJob \| None` | Temporarily overrides primary job schedule |
| `base_role` | `Role` | Hidden base role (holds base actions) |
| `special_role` | `list[Role]` | Active special roles (girlfriend, harem, pregnant, …) |
| `on_room_enter_event_list` | `ActionList` | Events fired when MC enters her room |
| `on_talk_event_list` | `ActionList` | Events fired when MC talks to her |

### Sex mechanics & reproduction

| Attribute | Type | Description |
|---|---|---|
| `sex_record` | `dict[str, int]` | Cumulative sex activity counters |
| `broken_taboos` | `list[str]` | Taboos that have been broken |
| `on_birth_control` | `bool` | Birth-control status |
| `bc_penalty` | `int` | Effectiveness reduction (default 0) |
| `fertility_percent` | `float` | Per-creampie pregnancy probability |
| `ideal_fertile_day` | `int` | Most-fertile day of month (0–29) |
| `lactation_sources` | `int` | Number of active lactation triggers |
| `breast_milk` | `float` | Available breast milk volume |

### Story & progression

| Attribute | Type | Description |
|---|---|---|
| `story_tracker` | `Story_Tracker` | Tracks story arc flags and milestones |
| `gtk_list` | `ActionList \| None` | "Get To Know" small-talk conversation events |
| `training_log` | `defaultdict[int]` | Tracks training-tag costs for `Trainable` objects |

### Miscellaneous

| Attribute | Type | Description |
|---|---|---|
| `available` | `bool` | Whether available for event/interaction |
| `is_favourite` | `bool` | MC has marked her as favourite |
| `stay_wet` | `bool` | Always stays aroused |
| `slave_collar` | `bool` | Is wearing slave collar |
| `drink_level` | `int` | Current intoxication level (0–3) |
| `sexed_count` | `int` | Times approached for sex today |
| `coffee_style` | `str` | Coffee preference string |

---

## 6. Special Methods

### `__init__(self, name, last_name, age, body_type, tits, hair_style, hair_colour, skin, tan, eyes, face_style, personality, height, what_font, who_font, what_color, who_color, relationship, SO_name, kids, ...)`  *(L785)*

Initialises all instance attributes.  After calling `__init__`, callers typically also call `init_person_variables()` and then add the instance to `list_of_people`.

---

### `__call__(self, what, *args, **kwargs)`  *(L1036)*

Enables `person("dialogue text")` syntax.  Applies the following pipeline before forwarding to the Ren'Py `Character`:

1. Run all `text_modifiers` on the input string.
2. Build and set a portrait for the dialogue box.
3. If text effects are enabled, dynamically transform erotic keywords:
   - Trance: desaturates text colour based on trance depth.
   - Sexual keywords (e.g. `"cum"`, `"cock"`, `"pussy"`, `"pregnant"`, `"fuck"`): scales size, adds bounce/drop/colour effects proportional to her current arousal.
4. Calls the underlying `char()` to display the dialogue.

---

### `__hash__(self)` / `__eq__(self, other)`  *(L1134 / L1137)*

Hash and equality are based solely on `identifier`.  This means `Person` objects can be used in sets and as dict keys, and two instances with the same identifier compare equal.

---

### `__getstate__(self)`  *(L1142)*

Ren'Py serialises `Person` instances to save files via pickle.  `__getstate__` strips cached properties before serialisation to keep save files small and prevent stale data on load:

**Excluded from saves:**
- `"bedroom"`, `"opinion"`, `"known_opinion"`, `"progress"` — `cached_property` accessors
- All keys in `_location_clear_keys`: `"location"`, `"current_location_hub"`, `"current_job"`, `"is_at_work"`, `"is_at_office"`, `"is_at_stripclub"`, `"is_at_mc_house"`

---

## 7. Sections & Method Reference

The class is divided into 11 named sections (marked with `# SECTION:` comments) plus several smaller subsections appended at the end of the Jobs section.

---

### Section 1 — Class / Static Factory Methods  *(L330–780)*

Utility class-methods for generating and querying character attributes. No instance state required.

#### Tit / cup-size helpers

| Method | Signature | Purpose |
|---|---|---|
| `get_random_tit` | `(cls, start, end) → str` | Weighted random cup size in range |
| `get_tit_weighted_list` | `(cls, start, end)` | Weighted list slice |
| `get_maximum_tit` | `(cls) → str` | Largest cup size (`"FF"`) |
| `get_tit_index` | `(cls, current_tits) → int` | Index of cup size in master list |
| `rank_tits` | `(cls, the_tits) → int` | Integer rank for size comparison |
| `get_smaller_tit` | `(cls, current_tit) → str` | One cup size smaller |
| `get_larger_tit` | `(cls, current_tit) → str` | One cup size larger |
| `get_random_tiny_tit` | `(cls) → str` | Random tiny cup (≤ AA) |
| `get_random_small_tit` | `(cls) → str` | Random small cup (≤ C) |
| `get_random_large_tit` | `(cls) → str` | Random large cup (≥ D) |
| `get_random_huge_tit` | `(cls) → str` | Random huge cup (≥ E) |
| `get_maximum_tiny_tit` | `(cls) → str` | Largest "tiny" cup |
| `get_maximum_small_tit` | `(cls) → str` | Largest "small" cup |
| `get_minimum_large_tit` | `(cls) → str` | Smallest "large" cup |
| `get_minimum_huge_tit` | `(cls) → str` | Smallest "huge" cup |
| `get_tiny_tits_weighted_list` | `(cls)` | Weighted list of tiny cups |
| `get_small_tits_weighted_list` | `(cls)` | Weighted list of small cups |
| `get_large_tits_weighted_list` | `(cls)` | Weighted list of large cups |
| `get_huge_tits_weighted_list` | `(cls)` | Weighted list of huge cups |
| `tit_is_in_weighted_tits_list` | `(tit, list) → bool` | *(staticmethod)* Cup in list |
| `tit_is_tiny` | `(cls, tit) → bool` | Cup ≤ tiny maximum |
| `tit_is_small` | `(cls, tit) → bool` | Cup ≤ small maximum |
| `tit_is_large` | `(cls, tit) → bool` | Cup ≥ large minimum |
| `tit_is_huge` | `(cls, tit) → bool` | Cup ≥ huge minimum |

#### Appearance generators

| Method | Signature | Purpose |
|---|---|---|
| `get_random_skin` | `(cls) → str` | Weighted random skin type |
| `get_random_hair_colour` | `(cls)` | Weighted random hair colour |
| `get_darkened_colour` | `(the_colour, var) → list` | *(staticmethod)* Darken a colour by variation constant |
| `generate_hair_colour` | `(cls, base, create_variation) → tuple` | Generate hair colour with optional variation |
| `get_random_eye` | `(cls) → tuple` | Weighted random eye colour |
| `generate_eye_colour` | `(cls, base, create_variation) → tuple` | Generate eye colour tuple |
| `get_random_hair_style` | `(cls) → Clothing` | Random hair-style object |
| `get_random_pubes_style` | `(cls) → Clothing` | Random pubic-hair object |
| `get_random_face` | `(cls) → str` | Random face identifier |
| `get_random_name` | `(cls) → str` | Random female first name |
| `get_random_last_name` | `(cls) → str` | Random last name |
| `get_random_male_name` | `(cls) → str` | Random male first name |
| `get_random_glasses_frame_colour` | `(cls) → tuple` | Random glasses colour |
| `get_random_body_type` | `(cls) → str` | Weighted random body type |
| `get_random_coffee_style` | `(cls) → str` | Random coffee preference |

#### Opinion helpers

| Method | Signature | Purpose |
|---|---|---|
| `get_normal_opinions_list` | `(cls) → list[str]` | All valid non-sexual opinion topics |
| `get_sexy_opinions_list` | `(cls) → list[str]` | All valid sexual opinion topics |
| `get_random_normal_opinion` | `(cls) → str` | Random non-sexual topic |
| `get_random_sexy_opinion` | `(cls) → str` | Random sexual topic |
| `get_list_of_hairs` | `(cls) → list` | All hair-style objects |
| `get_list_of_eyes` | `(cls) → list` | All eye definitions |

#### Stat range accessors

Each pair returns the floor/ceiling for a given stat in initial or final form:

`get_stat_floor(initial)`, `get_stat_ceiling()`, `get_skill_floor(initial)`, `get_skill_ceiling()`, `get_sex_skill_floor(initial)`, `get_sex_skill_ceiling()`, `get_happiness_floor(initial)`, `get_happiness_ceiling()`, `get_suggestibility_floor()`, `get_suggestibility_ceiling()`, `get_sluttiness_floor()`, `get_sluttiness_ceiling()`, `get_love_floor(initial)`, `get_love_ceiling(initial)`, `get_obedience_floor(initial)`, `get_obedience_ceiling()`, `get_work_experience_floor(initial)`, `get_work_experience_ceiling(initial)`, `get_age_floor(initial)`, `get_age_ceiling(initial)`, `get_height_floor(initial)`, `get_height_ceiling(initial)`, `get_old_age_floor()`, `get_teen_age_ceiling()`, `get_tall_height_floor()`, `get_short_height_ceiling()`, `get_height_step()`

#### Person lookup

| Method | Signature | Purpose |
|---|---|---|
| `get_person_by_identifier` | `(identifier) → Person` | *(staticmethod)* Retrieve instance from `list_of_people` |
| `get_initial_kids_range` | `(age_range, relationships_array) → list` | *(staticmethod)* Candidate kid-count range for age bracket |
| `finalize_kids_range` | `(cls, kids_range, age_range, rel_list, age, relationship) → list` | Narrow down kid counts by actual age + relationship |
| `finalize_relationships_weight` | `(cls, relationships_list, age)` | Adjust relationship weights by age |
| `get_potential_relationships_list` | `(cls)` | Base weighted relationship list copy |

---

### Section 2 — Instance Initialisation  *(L781–1167)*

| Method | Signature | Purpose |
|---|---|---|
| `__init__` | *(see §6)* | Construct and fully initialise instance |
| `__call__` | `(what, *args, **kwargs)` | Dialogue with dynamic arousal text effects |
| `__wrap_text_with_tag` | `(text, tag_open, tag_close, words, case_insensitive) → str` | Internal: wrap matched words in Ren'Py tags |
| `__hash__` | `() → int` | Hash by `identifier` |
| `__eq__` | `(other) → bool` | Equality by `identifier` |
| `__getstate__` | `() → dict` | Pickle hook — strips cached properties |
| `wrap_string` | `(string, the_colour, the_font, size_mod) → str` | Wrap text in colour/font/size Ren'Py tags |
| `reset_event_parameters` | `()` | Clear `event_triggers_dict` |
| `init_person_variables` | `()` | Initialise or reset character-specific sub-system variables |
| `generate_home` | `(set_home_time, force_new_home) → Room` | Create a `Room` for this character's home |
| `generate_daughter` | `(force_live_at_home, age, job) → Person` | Create a random daughter character |
| `generate_mother` | `(lives_with_daughter, age, job) → Person` | Create a random mother character |

---

### Section 3 — Location & Movement  *(L1168–1520)*

| Method / Property | Returns | Purpose |
|---|---|---|
| `idle_pose` *(property + setter)* | `str` | Current idle pose name; setter clears display cache |
| `location` *(cached_property)* | `Room` | Current `Room` object |
| `_set_location(value)` | — | Internal setter — updates `_location` and fires listener |
| `_clear_location_cache()` | — | Flush all `_location_clear_keys` cached properties |
| `current_location_hub` *(cached_property)* | `MapHub` | Hub containing current location |
| `home` *(cached_property)* | `Room` | Home `Room` |
| `_set_home(value)` | — | Internal home setter |
| `home_hub` *(cached_property)* | `HomeHub` | Hub containing home |
| `learn_home()` | `bool` | Make MC aware of her home address |
| `change_home_location(new_home)` | — | Move to a different home `Room` |
| `toggle_favourite()` | — | Toggle `is_favourite` |
| `is_home` *(property)* | `bool` | Currently at home |
| `is_at(location)` | `bool` | At given `Room` or `MapHub` |
| `living_with` *(property)* | `list[Person]` | Others living at the same home |
| `lives_alone` *(property)* | `bool` | Nobody else at home |
| `mc_knows_address` *(property)* | `bool` | MC knows where she lives |
| `is_job_known` *(property)* | `bool` | MC knows her job |
| `learn_job(job)` | — | Make job known to MC |
| `current_job` *(cached_property)* | `ActiveJob \| None` | Job currently being worked (at work location) |
| `is_at_work` *(cached_property)* | `bool` | At her work location |
| `is_at_office` *(cached_property)* | `bool` | At the MC's office |
| `is_at_stripclub` *(cached_property)* | `bool` | At the strip club |
| `is_at_mc_house` *(cached_property)* | `bool` | At the MC's house |
| `bedroom` *(cached_property)* | `Room` | Her bedroom `Room` |
| `change_location(destination)` | `bool` | Move to a `Room`; returns True on success |
| `change_to_bedroom()` | — | Move to her bedroom |
| `change_to_hallway()` | — | Move to her hallway |
| `can_clone` *(property)* | `bool` | Eligible to be cloned |
| `follow_mc` *(property + setter)* | `bool` | Whether she follows MC within the current hub |
| `follow_mc_everywhere` *(property + setter)* | `bool` | Whether she follows MC across all hubs |
| `body_images` *(property)* | `Clothing` | Body-layer Clothing sprite |
| `tan_images` *(property)* | `Clothing` | Tan-layer Clothing sprite |
| `expression_images` *(property)* | `Clothing` | Expression-layer Clothing sprite |

---

### Section 4 — Status / Role / Relationship Properties  *(L1521–1942)*

#### Key computed properties

| Property | Returns | Description |
|---|---|---|
| `fname` | `str` | First name only |
| `display_name` | `str` | Contextual display name (title, name, or "this woman") |
| `arousal_perc` | `float` | `arousal / max_arousal` |
| `is_unique` | `bool` | Named (story) character |
| `is_family` | `bool` | Has a family role |
| `is_employee` | `bool` | Works for the MC |
| `is_strip_club_employee` | `bool` | Works at strip club |
| `is_clone` | `bool` | Is a clone |
| `suggest_tier` | `int` 0–4 | Tier from `SUGGESTIBILITY_TIER_THRESHOLDS` |
| `obedience_tier` | `int` 0–5 | Tier from `OBEDIENCE_TIER_THRESHOLDS` |
| `sluttiness_tier` | `int` 0–5 | `clamp(0, 5, (sluttiness − 5) // 20)` |
| `is_available` | `bool` | Can be interacted with right now |
| `is_bald` | `bool` | Wearing bald hair style |
| `is_dominant` | `bool` | Dominant based on personality (alpha/wild/cougar bonus), `taking_control` vs `being_submissive` opinions, and obedience. Mutually exclusive with `is_submissive` |
| `is_submissive` | `bool` | Submissive based on slave status, personality (alpha/wild/cougar resist), `being_submissive` vs `taking_control` opinions, and obedience. Mutually exclusive with `is_dominant` |
| `is_slave` | `bool` | Has slave role |
| `is_stranger` | `bool` | Unknown / not introduced |
| `has_significant_other` | `bool` | Has a partner |
| `is_single` | `bool` | Relationship == "Single" |
| `in_harem` | `bool` | Has harem role |
| `is_girlfriend` | `bool` | Has girlfriend role |
| `is_affair` | `bool` | Has affair role |
| `has_relation_with_mc` | `bool` | Girlfriend / affair / harem |
| `formal_address` | `str` | How MC addresses her professionally |
| `weight` *(property + setter)* | `float` | Body weight; setter clamps to valid range |

#### Key methods

| Method | Signature | Purpose |
|---|---|---|
| `change_height(amount, chance)` | `bool` | Randomly adjust height; returns True if changed |
| `change_weight(amount, chance)` | `bool` | Randomly adjust weight |
| `hair_description` *(property)* | `str` | Human-readable hair description |
| `pubes_description` *(property)* | `str` | Human-readable pubic hair description |
| `tits_description` *(property)* | `str` | Human-readable breast-size description |

---

### Section 5 — Per-Turn & Per-Day Game Loop  *(L1943–2256)*

Called by the game loop each turn / each day.

| Method / Property | Signature | Purpose |
|---|---|---|
| `_remove_expired_serums()` | — | Remove serums whose duration has elapsed |
| `_remove_expired_infractions()` | — | Clear expired workplace infractions |
| `_remove_expired_limited_time_actions()` | — | Remove timed interaction actions |
| `_auto_develop_fetishes()` | — | Fire fetish-start quests when opinion thresholds are met |
| `_update_daily_stat_changes()` | — | Apply per-day stat decay / growth rules |
| `serum_tolerance` *(property)* | `int` | `_serum_tolerance` + antidote bonus |
| `active_serum_count` *(property)* | `int` | Number of active serums |
| `is_affected_by_serum(serum)` | `bool` | True if `serum` is in `serum_effects` |
| `active_serum_with_tag(tag)` | `bool` | Any active serum has the given tag |
| `active_serum_with_hidden_tag(tag)` | `bool` | Any active serum has the given hidden tag |
| `_check_serum_tolerance()` | — | Apply tolerance penalties if over-limit |
| `_update_breast_milk()` | — | Advance lactation state |
| `run_turn()` | — | **Main per-turn hook** — runs energy regen, serums, duties, and role turns |
| `update_daily_outfit()` | — | Select tomorrow's outfit at start of new day |
| `run_move()` | — | Process movement according to schedule |
| `run_day()` | — | **Main per-day hook** — resets arousal, updates drink level, fires daily stat changes |
| `apply_turn_based_outfit_bonus()` | — | Apply stat bonuses from currently worn outfit (per turn) |
| `apply_daily_outfit_bonus(outfit)` | — | Apply stat bonuses from outfit (per day) |

---

### Section 6 — Display / Rendering  *(L2257–2592)*

| Method | Signature | Purpose |
|---|---|---|
| `get_display_colour_code(saturation, given_alpha)` | `str` | Compute a display colour code for the dialogue box |
| `build_person_portrait(special_modifier)` | displayable | Build a portrait-sized composite sprite |
| `build_person_displayable(position, emotion, lighting, ...)` | displayable | Build a full-size composite character displayable |
| `draw_person(position, emotion, lighting, ...)` | — | Render the character on-screen |
| `hide_person(draw_layer)` | — | Remove character sprite |
| `draw_animated_removal(clothing, ...)` | — | Animate clothing removal |
| `draw_quick_removal(clothing, ...)` | — | Remove clothing without animation |
| `draw_quick_addition(clothing, ...)` | — | Add clothing without animation |
| `quick_draw_slide_back(clothing, ...)` | — | Slide removed clothing back on |
| `get_emotion()` | `str` | Compute current emotion from arousal / state |
| `call_dialogue(label_name, *args, **kwargs)` | — | Call a Ren'Py label with this person and personality as args |

---

### Section 7 — Opinions & Taboos  *(L2593–3026)*

#### Opinion score methods

| Method | Signature | Purpose |
|---|---|---|
| `get_opinion_score(topic)` | `int` | Opinion score for topic (−2 … 2; 0 if unknown) |
| `get_known_opinion_score(topic)` | `int` | Score only if MC has discovered it, else 0 |
| `get_known_opinion_list(...)` | `list` | All opinion entries MC knows |
| `get_opinion_topics_list(...)` | `list[str]` | All topic strings |
| `get_opinion_topic(topic)` | `list` | `[score, known]` for topic |
| `get_random_opinion(...)` | `tuple` | Random `(topic, score, known)` |
| `favourite_opinion(topics)` | `str` | Topic with highest score |
| `has_opinion(topic)` | `bool` | Has any entry for topic |
| `has_unknown_opinions` *(property)* | `bool` | At least one undiscovered opinion |
| `has_unknown_normal_opinions` *(property)* | `bool` | At least one undiscovered non-sexual opinion |
| `has_unknown_sexy_opinions` *(property)* | `bool` | At least one undiscovered sexual opinion |

#### Opinion mutation methods

| Method | Signature | Purpose |
|---|---|---|
| `discover_opinion(topic, add_to_log)` | `bool` | Mark opinion as known to MC |
| `discover_random_opinion(...)` | — | Discover a random unknown opinion |
| `set_opinion(topic, score, known)` | — | Set opinion to exact value |
| `remove_opinion(topic)` | — | Delete opinion entry |
| `update_opinion_with_score(topic, score, add_to_log)` | — | Set score preserving known flag |
| `strengthen_opinion(topic, add_to_log)` | — | +1 to opinion score |
| `increase_opinion_score(topic, max_value, add_to_log, weighted)` | — | Increase opinion, respecting max |
| `weaken_opinion(topic, add_to_log)` | — | −1 to opinion score |
| `decrease_opinion_score(topic, add_to_log)` | — | Decrease opinion score |
| `max_opinion_score(topic, add_to_log)` | — | Set opinion to maximum (2) |
| `create_opinion(topic, start_positive, start_known, add_to_log)` | — | Create new opinion entry |
| `add_opinion(topic, score, known, sexy_opinion, add_to_global, add_to_log)` | — | Add or update opinion |
| `reset_opinions()` | — | Clear all general opinions |
| `reset_sexy_opinions()` | — | Clear all sexual opinions |
| `hated_color_opinions` *(property)* | `list[str]` | Topics involving disliked clothing colours |
| `loved_color_opinions` *(property)* | `list[str]` | Topics involving liked clothing colours |
| `hated_outfit_opinions` *(property)* | `list[str]` | Outfit topics with negative score |
| `loved_outfit_opinions` *(property)* | `list[str]` | Outfit topics with positive score |

#### Taboo methods

| Method | Signature | Purpose |
|---|---|---|
| `has_taboo(taboos)` | `bool` | Has any of the given taboos |
| `has_broken_taboo(taboos)` | `bool` | Has broken any of the given taboos |
| `break_taboo(the_taboo, add_to_log, fire_event)` | — | Move taboo from active to broken |
| `restore_taboo(the_taboo, add_to_log)` | `bool` | Restore a previously broken taboo |

#### Sex-record helpers

| Method | Signature | Purpose |
|---|---|---|
| `pick_position_comment(position)` | — | Select dialogue for this position |
| `update_person_sex_record(report_log)` | — | Update `sex_record` from a completed sex-scene report |

---

### Section 8 — Wardrobe & Outfit Management  *(L3027–3473)*

#### Outfit selection

| Method / Property | Purpose |
|---|---|
| `current_planned_outfit` *(property + setter)* | Today's planned non-work outfit |
| `add_outfit(outfit)` | Add outfit to wardrobe |
| `decide_on_outfit()` | Choose which outfit to wear for the session |
| `get_random_appropriate_outfit()` | Random outfit from wardrobe matching current context |
| `get_random_appropriate_underwear()` | Random appropriate underwear |
| `get_random_appropriate_overwear()` | Random appropriate over-garment |
| `personalize_outfit()` | Apply personal-preference adjustments to current outfit |
| `apply_outfit_bottom_preference()` | Pick dress vs skirt vs pants per opinion |
| `set_sexier_panties()` | Replace panties with sexier option |
| `set_sexier_bra()` | Replace bra with sexier option |

#### Uniform & dress code

| Method / Property | Purpose |
|---|---|
| `is_wearing_uniform` *(property)* | Currently wearing work uniform |
| `is_wearing_forced_uniform` *(property)* | Uniform required unconditionally |
| `should_wear_uniform` *(property)* | Should be in uniform right now |
| `is_wearing_dress_code` *(property)* | Currently meeting dress code |
| `should_wear_dress_code` *(property)* | Should be in dress code right now |
| `is_wearing_planned_outfit` *(property)* | Currently wearing planned outfit |
| `wear_apron()` | Put on apron |
| `wear_bathrobe()` | Put on bathrobe |
| `wear_uniform()` | Apply work uniform to current outfit |
| `apply_outfit(outfit)` | Wear a specific outfit |
| `show_dress_sequence()` | Animate dressing |
| `apply_planned_outfit()` | Wear the planned outfit |

#### Outfit evaluation

| Method | Purpose |
|---|---|
| `approves_outfit_color(outfit)` | Returns True if outfit colours match opinions |
| `review_outfit(outfit)` | MC-style opinion of her current outfit |
| `judge_outfit(outfit, slut_boost)` | Returns True if outfit is too conservative for her sluttiness |
| `update_outfit_taboos()` | Apply/remove taboo effects based on outfit |

#### Clothing removal

| Method | Purpose |
|---|---|
| `strip_outfit_to_max_sluttiness(...)` | Progressively undress to her sluttiness comfort level |
| `strip_top_to_underwear()` | Remove outer top only |
| `strip_bottom_to_underwear()` | Remove outer bottom only |
| `strip_to_underwear()` | Remove everything except underwear |
| `strip_to_tits()` | Undress to expose breasts |
| `strip_to_vagina()` | Undress to expose genitals |
| `strip_full_outfit()` | Remove all clothing |
| `remove_clothing(clothing, ...)` | Remove specific item(s) with optional animation |
| `strip_outfit(top_layer_first, ...)` | Progressively strip items |
| `choose_strip_clothing_item()` | Decide which item to strip next based on opinions |

---

### Section 9 — Serum & Stat Management  *(L3474–3881)*

> **Note:** The core serum and stat-change methods live in `PersonStatMixin` (see §10).  The methods listed here remain in `Person` itself and extend the outfit-stripping concern.

| Method | Purpose |
|---|---|
| `get_no_condom_threshold(situational_modifier)` | Calculate minimum effective sluttiness for condom refusal |
| `wants_condom(situational_modifier, use_taboos)` | True if she wants a condom |
| `has_family_taboo` *(property)* | Family incest taboo is active |
| `has_large_tits` *(property)* | Cup size ≥ D |
| `increase_tit_size()` | Move up one cup size |
| `decrease_tit_size()` | Move down one cup size |
| `wants_creampie` *(property)* | She is positively disposed to creampies |
| `days_from_ideal_fertility` *(property)* | Days from peak fertile day |
| `bc_status_known` *(property)* | MC knows her birth-control status |
| `update_birth_control_knowledge()` | Make BC status known to MC |
| `on_birth_control` *(property + setter)* | Birth control active |
| `is_mc_father` *(property)* | MC is the biological father |
| `has_child_with_mc` *(property)* | Has at least one child with MC |
| `number_of_children_with_mc` *(property)* | Count of children with MC |
| `had_sex_today` *(property)* | Had sex today |
| `is_pregnant` *(property)* | Currently pregnant |
| `is_pregnancy_wanted` *(property)* | Actively wants to get pregnant |
| `is_lactating` *(property)* | Currently producing breast milk |
| `knows_pregnant` *(property + setter)* | Is aware of own pregnancy |
| `pregnancy_due_day` *(property)* | In-game day of expected birth |
| `pregnancy_is_visible` *(property)* | Pregnancy visually apparent |
| `pregnancy_show_day` *(property)* | Day pregnancy becomes visible |
| `baby_desire` *(property)* | How strongly she wants a baby |
| `change_baby_desire(amount)` | Adjust baby-desire score |
| `is_highly_fertile` *(property)* | Significantly higher than average fertility |
| `is_infertile` *(property)* | Cannot become pregnant |
| `effective_sluttiness(taboo)` | Sluttiness adjusted for active taboos |
| `run_orgasm(...)` | Trigger orgasm effects |
| `is_in_trance` *(property)* | In any trance state |
| `is_in_very_heavy_trance` *(property)* | In very heavy trance |
| `trance_training_available` *(property)* | Can be trance-trained right now |
| `increase_trance()` | Deepen trance level |
| `trance_multiplier` *(property)* | Happiness multiplier from trance |
| `is_tipsy` *(property)* | Slightly drunk (drink_level == 1) |
| `is_drunk` *(property)* | Moderately drunk (drink_level == 2) |
| `is_wasted` *(property)* | Very drunk (drink_level == 3) |
| `increase_drink_level()` | Increase intoxication |

---

### Section 10 — Sex Mechanics  *(L3882–4381)*

| Method / Property | Purpose |
|---|---|
| *(See stripping / condom / pregnancy / trance methods in §9 — they reside inside this physical section in the file)* | — |
| *Position and clothing-exposure properties* (`is_naked`, `tits_available`, `tits_visible`, `vagina_available`, `vagina_visible`, `underwear_visible`, `wearing_bra`, `wearing_panties`, `bra_covered`, `panties_covered`, `has_underwear`, `is_wearing_underwear`, `is_bra_visible`, `are_panties_visible`, `bra`, `panties`, `can_remove_bra`, `can_remove_panties`) | State checks for sex scene UI |
| *Cum-state properties* (`cum_covered`, `has_mouth_cum`, `has_tits_cum`, `has_stomach_cum`, `has_face_cum`, `has_ass_cum`, `has_creampie_cum`) | Track applied cum effects |
| *Clothing-type properties* (`has_dress`, `has_skirt`, `has_pants`, `has_shirt`, `has_socks`, `has_low_socks`, `has_thigh_high_socks`, `has_shoes`, `has_boots`, `has_high_heels`, `has_one_piece`, `has_bracet`, `has_glasses`) | Fast outfit-type checks |
| `restore_all_clothing()` | Restore all clothing to outfit |
| `get_full_strip_list()` | Ordered list of all removable items |
| `get_underwear_strip_list()` | Underwear items only |
| `get_tit_strip_list()` | Items blocking breast access |
| `get_vagina_strip_list()` | Items blocking genital access |
| `can_half_off_to_tits()` / `get_half_off_to_tits_list()` | Check / get half-off route to breasts |
| `can_half_off_to_vagina()` / `get_half_off_to_vagina_list()` | Check / get half-off route to genitals |
| `get_sex_goal()` | Compute MC's sex goal for this character |
| `facial_or_swallow()` | Decide facial vs swallow based on opinions |
| `shows_off_her_ass` / `shows_off_her_tits` *(properties)* | Outfit exposes body areas |

---

### Section 11 — Jobs, Roles & Schedule  *(L4382–5291)*

#### Strip club economics

| Method / Property | Purpose |
|---|---|
| `stripclub_salary` *(property)* | Daily wage at strip club |
| `stripclub_profit` *(property)* | Estimated nightly profit |
| `calculate_job_efficiency()` | `productivity_adjustment × current_job.productivity_adjustment` |

#### Schedule management

| Method | Signature | Purpose |
|---|---|---|
| `set_schedule(location, day_slots, time_slots)` | — | Add location to weekly schedule |
| `clear_schedule(location)` | — | Remove location from schedule |
| `get_scheduled_location(day, time)` | `Room \| None` | Where she should be at given day/time |
| `is_scheduled_for(location)` | `bool` | Location is in regular schedule |

#### Salary

| Method / Property | Purpose |
|---|---|
| `salary` *(property)* | Current job salary |
| `get_salary_range()` | Expected salary range based on job/skills |
| `change_salary(amount)` | Adjust salary modifier |

#### Job management

| Method | Signature | Purpose |
|---|---|---|
| `is_at_job(job)` | `bool` | Currently working at given job |
| `has_job(job)` | `bool` | Holds a job of given definition |
| `is_primary_job(job)` | `bool` | Given job is primary |
| `get_job(job)` | `ActiveJob \| None` | Retrieve ActiveJob by definition |
| `has_job_role(role)` | `bool` | Any job has the given role |
| `jobs` *(property)* | `list[ActiveJob]` | All active jobs |
| `job_roles` *(property)* | `list[Role]` | All roles from all jobs |
| `current_job_roles` *(property)* | `list[Role]` | Roles from job at current location |
| `current_job_actions` *(property)* | `list[Action]` | Actions from job at current location |
| `current_job_internet_actions` *(property)* | `list[Action]` | Internet actions from current job |
| `change_job(job_def, ...)` | — | Assign a new primary/secondary/side job |
| `change_job_assignment(job, assignment)` | — | Change which slot a job occupies |
| `set_side_job(job_def, ...)` | — | Set a temporary side job |
| `quit_job(job)` | — | Remove job from all slots |

#### Duties

| Method / Property | Purpose |
|---|---|
| `duties` *(property)* | All duties from all jobs |
| `has_duty(duty)` | True if she has given duty active |
| `active_duties` *(property)* | Currently active (non-suspended) duties |
| `daily_duties` *(property)* | Duties that run each day |
| `current_duty_actions` *(property)* | Actions from duties at current location |
| `current_duty_internet_actions` *(property)* | Internet actions from duties |

#### Role management

| Method | Signature | Purpose |
|---|---|---|
| `add_role(role)` | `bool` | Add a special role (guards against duplicates) |
| `remove_role(role, remove_linked)` | `bool` | Remove role and linked roles |
| `has_role(role)` | `bool` | Has role or role parent |
| `has_exact_role(role)` | `bool` | Exact role match |
| `add_action(action)` | — | Add action to base role |
| `remove_action(action)` | — | Remove action from base role |
| `has_action(action)` | `bool` | Base role has action |
| `get_role_reference(role)` | `Role \| None` | Retrieve actual role instance |

#### Queued events & infractions

| Method | Purpose |
|---|---|
| `is_sleeping` *(property)* | Currently in sleep state |
| `has_queued_event(event)` | Has event waiting in queue |
| `remove_queued_event(event)` | Remove event from queue |
| `add_infraction(infraction)` | Add workplace infraction record |
| `remove_infraction(infraction)` | Remove infraction record |

#### Appearance management

| Method | Purpose |
|---|---|
| `match_skin(skin)` | Adjust outfit to match skin tone |
| `set_eye_colour(eye)` | Change eye colour |
| `set_hair_colour(colour)` | Change hair colour |
| `lighten_hair_colour()` | Lighten hair colour |
| `darken_hair_colour()` | Darken hair colour |

#### Titles

| Method | Purpose |
|---|---|
| `get_titles()` | All possible titles for this character |
| `get_random_title()` | Random title from available titles |
| `get_possessive_titles()` | All possible possessive titles |
| `get_random_possessive_title()` | Random possessive title |
| `get_player_titles()` | What she can call the MC |
| `get_random_player_title()` | Random MC title |
| `set_title(title)` | Set and format title |
| `set_possessive_title(title)` | Set and format possessive title |
| `set_mc_title(title)` | Set how she addresses MC |

#### Personality & removal

| Method | Purpose |
|---|---|
| `change_personality(personality)` | Switch to a new `Personality` |
| `restore_original_personality()` | Revert to initial personality |
| `remove_person_from_game()` | Cleanly remove character from all lists and relationships |

---

### Appendix subsections *(L5312–6109)*

These groups of tightly scoped methods appear after the main sections:

| Subsection | Line | Contents |
|---|---|---|
| Phone message information | 5312 | `has_instapic_post`, `instapic_known`, `learn_instapic`, `has_onlyfan_post`, `onlyfans_known`, `learn_onlyfans`, `has_dikdok_post`, `dikdok_known`, `learn_dikdok` |
| Outfit method wrappers | 5358 | Delegates `is_naked`, `tits_available`, `tits_visible`, `vagina_available`, `vagina_visible`, `underwear_visible`, `wearing_bra`, `wearing_panties`, `bra_covered`, `panties_covered`, `has_underwear`, `is_wearing_underwear`, `is_bra_visible`, `are_panties_visible`, `bra`, `panties`, `can_remove_bra`, `can_remove_panties`, clothing-type checks, strip-list helpers |
| Body descriptor wrappers | 5585 | `body_is_thin`, `body_is_average`, `body_is_thick`, `body_is_pregnant` |
| Fetish wrappers | 5605 | `fetish_count`, `has_anal_fetish`, `has_cum_fetish`, `has_breeding_fetish`, `has_exhibition_fetish`, `has_started_*_fetish` (×4) |
| Roleplay functions | 5645 | `change_to_lingerie`, `roleplay_mc_title_swap`, `roleplay_mc_title_revert`, `roleplay_title_swap`, `roleplay_title_revert`, `roleplay_possessive_title_swap`, `roleplay_possessive_title_revert`, `roleplay_personality_swap`, `roleplay_personality_revert` |
| Misc | 5687 | `is_intern`, `is_jealous`, `is_free_use`, `have_orgasm`, `favourite_colour`, `has_story`, `progress` *(cached_property)*, `clean_cache`, `current_position` *(property + setter)*, `maximum_milk_in_breasts`, `so_title`, `so_girl_title` |
| Event day functions | 5782 | `has_event_day`, `has_event_delay`, `set_event_day`, `get_event_day`, `days_since_event`, `story_event_ready`, `story_event_log`, `string_since_event` |
| Get To Know functions | 5852 | `set_gtk_list`, `has_gtk_list`, `has_gtk_avail`, `build_gtk_list` |
| Jealous Sister functions | 5888 | `is_jealous_sister`, `add_jealous_event`, `get_jealous_description`, `get_jealous_act`, `reset_jealous_list`, `get_jealous_list`, `jealous_score`, `jealous_score_reset`, `jealous_change_score`, `reset_all_jealousy`, `jealous_witness_public_sex`, `jealous_witness_publix_sex_list`, `jealous_sister_get_target_ident`, `jealous_sister_get_revenge_tuple` |
| Unique crisis addition | 5958 | `add_unique_on_talk_event`, `add_unique_on_room_enter_event`, `remove_on_talk_event`, `remove_on_room_enter_event` |
| Sex skill wrappers | 5996 | `foreplay_sex_skill`, `oral_sex_skill`, `vaginal_sex_skill`, `anal_sex_skill` *(all properties)* |
| Opinion score wrappers | 6016 | `opinion` *(cached_property → Opinion)*, `known_opinion` *(cached_property → Opinion)* |
| Sex record wrappers | 6029 | `increase_handjobs`, `increase_cunnilingus`, `increase_tit_fucks`, `increase_blowjobs`, `increase_vaginal_sex`, `increase_anal_sex`, `increase_fill_up_condom`, `blowjob_count`, `vaginal_sex_count`, `anal_sex_count`, `vaginal_creampie_count`, `anal_creampie_count`, `cum_facial_count`, `cum_mouth_count`, `cum_covered_count`, `public_sex_count`, `cum_exposure_count`, `is_cum_dump`, `is_cum_bucket` |

---

## 8. PersonStatMixin Method Reference

All 47 methods from `_person_stat_mixin_ren.py` become instance methods on `Person` via MRO.

### Serum administration

| Method | Signature | Purpose |
|---|---|---|
| `give_serum(serum, add_to_log)` | `SerumDesign → None` | Apply a serum; increment tolerance counter |
| `apply_serum_study(add_to_log)` | `→ None` | Raise mastery of all active serum traits by 0.2 |

### Suggestibility

| Method | Signature | Purpose |
|---|---|---|
| `change_suggest(amount, add_to_log)` | `int → None` | Permanently change base suggestibility |
| `change_modded_suggestibility(amount, max_amt, add_to_log)` | — | Change suggestibility up to a cap (for serum-aura effects) |
| `add_suggest_effect(amount, add_to_log)` | `int → None` | Add a temporary suggestion to the bag |
| `remove_suggest_effect(amount)` | `int → None` | Remove one suggestion value from the bag |
| `max_stat_change_calc(max_change, serum_check, stat_cap)` | `→ int` | Compute effective stat-change cap based on suggestibility + active serum bonus |

### Love / sluttiness / happiness / obedience

| Method / Property | Signature | Purpose |
|---|---|---|
| `change_love(amount, max_amount, add_to_log)` | `int → int` | Change love; returns actual change applied |
| `sluttiness` *(property)* | `→ int` | `_sluttiness + sum(situational_sluttiness)` |
| `change_slut(amount, max_amount, add_to_log)` | `int → int` | Change sluttiness |
| `add_situational_slut(source, amount, description)` | — | Add a named temporary sluttiness modifier |
| `clear_situational_slut(source)` | — | Remove named sluttiness modifier |
| `change_happiness(amount, max_amount, add_to_log)` | `int → int` | Change happiness |
| `obedience` *(property + setter)* | `→ int` | `_obedience + sum(situational_obedience)` |
| `change_obedience(amount, max_amount, add_to_log)` | `int → int` | Change obedience |
| `add_situational_obedience(source, amount, description)` | — | Add a named temporary obedience modifier |
| `clear_situational_obedience(source)` | — | Remove named obedience modifier |

### Personality stats (Cha / Int / Focus)

| Method | Purpose |
|---|---|
| `change_cha(amount, add_to_log)` | Change charisma; debt-tracking ensures no negative values |
| `change_int(amount, add_to_log)` | Change intelligence |
| `change_focus(amount, add_to_log)` | Change focus |

### Work skills & potentials

| Method / Property | Purpose |
|---|---|
| `change_hr_skill(amount, add_to_log)` | Change HR skill |
| `change_market_skill(amount, add_to_log)` | Change Marketing skill |
| `extra_market_skill` *(property)* | Bonus from `work_for_tips` duty |
| `change_research_skill(amount, add_to_log)` | Change Research skill |
| `change_production_skill(amount, add_to_log)` | Change Production skill |
| `change_supply_skill(amount, add_to_log)` | Change Supply skill |
| `research_potential` *(property)* | `int(3×int + focus + 2×research_skill + 10) × researcher_bonus` |
| `human_resource_potential` *(property)* | `int((3×cha + int + 2×hr_skill + 15) / 5)` |
| `marketing_potential` *(property)* | `int(3×cha + focus + 2×(market_skill + extra_market_skill) + 20)` |
| `production_potential` *(property)* | `int(3×focus + int + 2×production_skill + 10)` |
| `supply_potential` *(property)* | `int(5×focus + 3×cha + 3×supply_skill + 20)` |
| `increase_work_skill(skill, max_value, add_to_log)` | Increase one work skill by 1 |
| `decrease_work_skill(skill, add_to_log)` | Decrease one work skill by 1 |
| `update_work_skill(skill, score, add_to_log)` | Set work skill to exact value |

### Sex skills

| Method | Purpose |
|---|---|
| `change_sex_skill(skill_name, amount, add_to_log)` | Change a sex skill by amount |
| `increase_sex_skill(skill, max_value, add_to_log)` | Increase sex skill by 1 |
| `decrease_sex_skill(skill, add_to_log)` | Decrease sex skill by 1 |
| `update_sex_skill(skill, score, add_to_log)` | Set sex skill to exact value |

### Batch stat change

| Method | Signature | Purpose |
|---|---|---|
| `change_stats(obedience, happiness, arousal, love, slut, max_slut, max_love, max_obedience, energy, novelty, add_to_log)` | — | Change multiple stats in one call; logs a combined notification |

### Arousal / energy / novelty

| Method | Purpose |
|---|---|
| `change_arousal(amount, add_to_log)` | Change arousal |
| `reset_arousal()` | Reset arousal to 0 |
| `change_max_arousal(amount, add_to_log)` | Change arousal ceiling |
| `change_novelty(amount, add_to_log)` | Change novelty score |
| `change_energy(amount, add_to_log)` | Change energy |
| `change_max_energy(amount, add_to_log)` | Change energy ceiling (floor 20, ceiling 200) |

---

## 9. Serialisation & Save-Game Compatibility

`Person` is a Ren'Py persisted object. Key notes:

- **`__getstate__`** strips `cached_property` attributes before pickling. On load, these properties recompute themselves on first access.
- **`identifier`** is the stable key.  `get_person_by_identifier()` is the canonical way to resolve a saved person reference.
- Adding new `__init__` attributes is generally safe if you provide a default fallback in any code that reads them, because older saves will not have them in `__dict__`.
- **Do not rename** existing `__dict__` attributes in place — rename + migration helper required.

---

## 10. Relationships to Other Classes

| Class | Attribute(s) on Person | Notes |
|---|---|---|
| `Opinion` | `opinion`, `known_opinion` *(cached_property)* | Proxy wrapper over `get_opinion_score` / `get_known_opinion_score` |
| `Progression` | `progress` *(cached_property)* | Tracks stat and story thresholds |
| `Story_Tracker` | `story_tracker` | Story-flag storage |
| `Schedule` | `schedule`, `override_schedule` | Weekly location schedule |
| `Wardrobe` | `wardrobe` | Outfit collection |
| `Outfit` | `outfit`, `base_outfit`, `planned_outfit`, `next_day_outfit` | Currently worn / planned clothing |
| `ActiveJob` | `primary_job`, `secondary_job`, `side_job` | Job wrappers |
| `Role` | `base_role`, `special_role[]` | Game-state roles |
| `SerumDesign` | `serum_effects[]` | Active serums |
| `Personality` | `personality` | Affects dialogue path, `call_dialogue` routing, and stat-gain multipliers (`love_gain_multiplier`, `happiness_gain_multiplier`, `obedience_gain_multiplier`, `slut_gain_multiplier`) |
| `RelationshipArray` | `town_relationships` (module-level) | Global inter-character relationships |
| `Character` (Ren'Py) | `char` | Dialogue display object |

---

## 11. Pregnancy & Child Tracking

> **Short answer:** Children are recorded in three complementary places: `person.kids` (total count), `person.sex_record["Children with MC"]` (MC-fathered births), and the module-level `town_relationships` `RelationshipArray` (when a child exists as an actual `Person` instance).  In-game births also create a `Kid` instance stored in `person.kids_list`.

### 11.1 Where each fact is stored

| Fact | Storage location | Set / cleared by |
|---|---|---|
| Total child count (all partners, including pre-game) | `person.kids` (`int`) | `__init__` (initial value), `pregnant_finish_person()` (+1 at birth), `generate_daughter()` (+1 for each real daughter) |
| Children fathered by the MC | `person.sex_record["Children with MC"]` (`int`, key absent = 0) | `pregnant_finish_person()` in `role_pregnant_definition_ren.py` — only incremented when `person.is_mc_father` is `True` at time of birth |
| In-game born children with rich data | `person.kids_list` (`list[Kid]`) | `pregnant_finish_person()` appends a new `Kid` instance at each birth |
| Real `Person` daughter instances | `town_relationships` (`RelationshipArray`) | `generate_daughter()` calls `town_relationships.update_relationship(self, the_daughter, "Daughter", "Mother")` |
| Currently pregnant | `pregnant_role` present in `person.special_role` | `become_pregnant()` adds the role; `pregnant_finish_person()` / `abort_pregnancy()` removes it |
| MC is the father (during pregnancy) | `person.event_triggers_dict["preg_mc_father"]` (`bool`) | Set by `become_pregnant(mc_father=…)` |
| She knows she is pregnant | `person.event_triggers_dict["preg_knows"]` (`bool`) | `knows_pregnant` setter |
| Last birth day | `person.event_triggers_dict["last_birth"]` (`int`) | `person.set_event_day("last_birth")` in `pregnant_finish_person()` |

### 11.2 Convenience properties on `Person`

| Property | Returns | Notes |
|---|---|---|
| `is_pregnant` | `bool` | `True` while `pregnant_role` is in `special_role` |
| `is_mc_father` | `bool` | Reads `event_triggers_dict["preg_mc_father"]`; **only valid while `is_pregnant`** |
| `knows_pregnant` | `bool` (+ setter) | `True` when pregnant *and* `event_triggers_dict["preg_knows"]` is `True` |
| `has_child_with_mc` | `bool` | `sex_record.get("Children with MC", 0) > 0` — `True` after birth, not during pregnancy |
| `number_of_children_with_mc` | `int` | `sex_record.get("Children with MC", 0)` |
| `kids_list` | `list[Kid]` | `Kid` objects created at each in-game birth; empty list for pre-game children and old saves |
| `is_pregnancy_wanted` | `bool` | Pregnant and `baby_desire >= 40` |
| `pregnancy_due_day` | `int` | `event_triggers_dict["preg_start_date"] + 100` (approx.) |
| `pregnancy_is_visible` | `bool` | `day >= pregnancy_show_day` |
| `pregnancy_show_day` | `int` | `event_triggers_dict["preg_transform_day"]` |
| `is_highly_fertile` | `bool` | `fertility_percent >= 25` |
| `is_infertile` | `bool` | `fertility_percent < 0` |
| `effective_fertility` | `float` | Base fertility adjusted for cycle day (modes 2 and 3) |
| `birthcontrol_efficiency` | `int` | 0 if not on BC; else `PERCENTAGES[pregnancy_pref] - bc_penalty` |
| `pregnancy_chance` | `float` | `(effective_fertility / 100) × (100 − birthcontrol_efficiency)` |

### 11.3 Pregnancy lifecycle

Pregnancy is managed entirely by functions in `game/game_roles/role_pregnant_definition_ren.py`.  The `Person` object is the data store; the definition file provides the event orchestration.

```
cum_in_vagina()
  └─ did_she_become_pregnant()
       ├─ rolls effective_fertility
       ├─ rolls birthcontrol_efficiency
       └─ become_pregnant(person, mc_father)  ← sets all preg_* event_triggers_dict keys
            │                                     adds pregnant_role
            │                                     schedules: preg announce, tits grow,
            │                                               body transform, finish announce
            └─ [~100 days later] pregnant_finish_person(person)
                 ├─ restores body_type (pre_preg_body)
                 ├─ person.kids += 1
                 ├─ person.set_event_day("last_birth")
                 ├─ sex_record["Children with MC"] += 1  (if mc_father)
                 ├─ schedules tit-shrink events
                 └─ removes pregnant_role
```

`abort_pregnancy(person)` can short-circuit this at any point, removing the role and restoring appearance without incrementing any child counters.

### 11.4 `event_triggers_dict` keys written during pregnancy

| Key | Type | Meaning |
|---|---|---|
| `"preg_start_date"` | `int` | In-game day pregnancy began |
| `"preg_announce_day"` | `int` | Day the announcement event fires |
| `"preg_tits_date"` | `int` | Day breasts grow |
| `"preg_transform_day"` | `int` | Day belly becomes visible / body type changes |
| `"preg_finish_announce_day"` | `int` | Day the full-term announcement fires |
| `"pre_preg_tits"` | `str` | Cup size before pregnancy (restored after birth) |
| `"pre_preg_body"` | `str` | Body type before transform (restored after birth) |
| `"preg_mc_father"` | `bool` | Whether MC is the biological father |
| `"preg_wanted"` | `bool` | Whether she wanted to be pregnant (baby_desire ≥ 40) |
| `"preg_accident"` | `bool` | `True` if she was on birth control when she conceived |
| `"preg_knows"` | `bool` | She is aware of her pregnancy |
| `"immaculate_conception"` | `bool` | She had the vaginal-sex taboo when she conceived |
| `"last_birth"` | `int` | Day of last birth (guards 21-day re-pregnancy block) |
| `"no_pregnancy"` | `bool` | Special flag to prevent pregnancy during normal sex routines |
| `"birth_control_status"` | `bool` | Cached BC state known to MC |
| `"birth_control_known_day"` | `int` | Day MC learned BC status |

### 11.5 `persistent.pregnancy_pref` settings

| Value | Label | Birth-control effectiveness | Cycle simulation |
|---|---|---|---|
| `0` | No pregnancy content | N/A — pregnancy disabled | None |
| `1` | Predictable | 100 % effective | None (flat fertility) |
| `2` | Semi-Realistic | 90 % effective | Fertility multiplied by cycle position |
| `3` | Realistic | 99 % effective | Narrow fertile window (≤ 3 days); very low base chance |

Default value at game start: `0` (no content).

### 11.6 Querying existing `Person` children

When a daughter is generated as a real `Person` instance (via `generate_daughter()`) she is linked in `town_relationships` with a `"Daughter"` / `"Mother"` pair.  Use the `RelationshipArray` helpers to query this:

| Call | Returns |
|---|---|
| `town_relationships.get_existing_children(person)` | `list[Person]` of her `Person`-instance daughters |
| `town_relationships.get_existing_child_count(person)` | `int` count of those instances |
| `town_relationships.get_existing_parents(person)` | `list[Person]` of her `Person`-instance mothers |

Note that `person.kids` will always be ≥ `town_relationships.get_existing_child_count(person)` because `kids` counts all children (including those who were never instantiated as `Person` objects — e.g. children from before the game started).

### 11.7 The `Kid` class (`Kid_ren.py`)

Every child born during the game is recorded as a `Kid` instance and stored in `mother.kids_list`.  `Kid` lives in `game/major_game_classes/character_related/Kid_ren.py` at `init -2`.

#### Fields

| Field | Type | Description |
|---|---|---|
| `first_name` | `str` | Given name (random female or male name from the standard lists) |
| `last_name` | `str` | Family name inherited from the mother |
| `birthdate` | `int` | In-game day of birth |
| `gender` | `str` | `"female"` or `"male"` (random 50/50 at birth) |
| `mother` | `Person` | Direct reference to the mother |
| `father` | `str` | Acknowledged father's full name, or `"Unknown"` |
| `bio_father` | `str` | Biological father's full name, or `"Unknown"` |

#### Properties

| Property | Returns | Formula |
|---|---|---|
| `age` | `int` | `(day - birthdate) // 360` — one year = 30 days × 12 months = 360 game days |
| `full_name` | `str` | `f"{first_name} {last_name}"` |

#### How a `Kid` is created

`pregnant_finish_person()` in `role_pregnant_definition_ren.py` builds the `Kid` immediately after birth:

```python
kid_gender = renpy.random.choice(("female", "male"))
kid_first_name = Person.get_random_name() if kid_gender == "female" else Person.get_random_male_name()
person.kids_list.append(
    Kid(
        first_name  = kid_first_name,
        last_name   = person.last_name,
        birthdate   = day,
        gender      = kid_gender,
        mother      = person,
        father      = f"{mc.name} {mc.last_name}" if person.is_mc_father else "Unknown",
        bio_father  = f"{mc.name} {mc.last_name}" if person.is_mc_father else "Unknown",
    )
)
```

`father` and `bio_father` are identical at birth.  They can be changed later if story events reveal a discrepancy.  `person.kids_list` is empty for characters whose children were generated before the game started (those are represented only by `person.kids` and `town_relationships`).
