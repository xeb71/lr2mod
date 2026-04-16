# Lab Rats 2 – Reformulate: Summary

## Game Overview

**Lab Rats 2 – Reformulate (LR2)** is an adult-oriented visual novel / life-simulation game built with the [Ren'Py](https://www.renpy.org/) engine. The player takes the role of a young entrepreneur (the MC – Main Character) who launches a small pharmaceutical company that specialises in experimental behavioural serums.

### Core Premise
The MC uses start-up capital (a home equity loan from his mother) to found a serum company. By running the business, interacting with characters, and administering experimental serums, the player gradually influences the personalities, relationships, and behaviours of the women around them. The game balances resource management (funds, employees, production) with a social/relationship layer (love, obedience, sluttiness scores, opinions, and story arcs).

### Key Mechanics

| Mechanic | Description |
|---|---|
| **Serum Design & Production** | Research, design, and manufacture serums with tiered traits (T0–T3). Traits can modify character stats, behaviours, and fetishes. Mastery increases serum effectiveness. |
| **Business Management** | Manage five company divisions: Marketing, Production, Research, Supply, and HR. Hire/fire employees, assign roles, issue contracts, and set workplace policies. |
| **Character Stats** | Every NPC tracks: Love, Sluttiness (Lust), Obedience, Suggestibility, Charisma, Intelligence, and more. |
| **Opinions System** | Characters hold individual opinions on topics (e.g. incest, specific sex acts, relationships). Opinions gate content and modify stat thresholds. |
| **Story Arcs** | Each named character has independent Love, Obedience, and Sluttiness arcs with their own event chains and taboo-break quests. |
| **Crises Events** | Random and scheduled "crisis" events fire based on game state and time, requiring player decisions (business crises, personal encounters, workplace incidents). |
| **Scheduling System** | An alpha scheduling system lets the player book future dates, appointments, and repeating events. |
| **Clothing & Wardrobe** | Deep clothing/outfit system with per-character wardrobes, uniform policies per company division, and occasion-based outfit selection. |
| **Dating & Activities** | Bar dates, home dates, various activities (billiards, darts, dancing), and a Sex Mechanic system for sexual encounters with position locking behind story progress. |
| **Pregnancy System** | Optional pregnancy with configurable preferences (off / predictable / realistic). Characters can become pregnant with unique pregnancy routes for some characters. |
| **Perks** | MC gains ability and item perks that modify gameplay and unlock new options. |
| **Fetish System** | Fetish serums unlock specific fetish arcs (Anal, Cum, Breeding, Exhibition) for characters. |
| **Strip Club** | The player can acquire and manage a strip club, assigning characters to roles (dancer, waitress, BDSM performer, manager). |
| **University** | A university setting that unlocks mid-game, with student and professor characters and obedience story arcs. |
| **Sex Toys** | A research-and-manufacture system for sex toys. The player researches `ToyBlueprint` nodes (a tiered tech tree), designs `ToyDesign` objects by adding `ToyAttribute` modules, and prints finished `ToyItem` units using 3D printers managed via an Engineering division. Toys can be installed on NPCs or used manually; attributes add capabilities such as GPS tracking, diagnostics (pregnancy detection), remote intensity control, and vibration. The **Sex Toy Admin** HUD (`sex_toy_admin_app.rpy`) lets the MC monitor all installed devices, adjust intensity, and view NPC statistics (use count, orgasms, switch-off events). |
| **InstaPic & Photo Snapshots** | A social-media photo storyline system. NPCs (initially Lily, then Jennifer) can unlock an **InstaPic** role that lets them post photos, receive comments, and exchange DMs with the MC. The player can request specific outfits (underwear, topless, nude) via DMs, save received photos to a persistent **Photo Album** (accessible from the in-game phone's internet menu), and scroll back through a character's full photo history. An **OnlyFanatics** role extends the system with a subscription-based content tier. |
| **Game Speed** | Four configurable speeds (Quick / Standard / Epic / Marathon) control inter-event timing delays (Tier 0–3). |

### Named Characters (22+)
Alexia, Ashley, Camila, Candace, Christina, Christine, Ellie, Emily, Erica, Gabrielle, Iris, Jennifer, Kaya, Lily, Myrabelle, Naomi, Nora, Ophelia, Penelope, Rebecca, Sakari, Sarah, Starbuck, Stephanie, and various side/generic characters.

---

## Program Structure

The project is a Ren'Py visual novel. Source files are predominantly either **`.rpy`** (Ren'Py script) or **`_ren.py`** (Python modules loaded by Ren'Py at init time). The `game/` directory is the Ren'Py game root.

```
lr2/
├── game/                            # Ren'Py game root
│   ├── script.rpy                   # Engine bootstrap, global imports, init hooks
│   ├── options.rpy                  # Ren'Py engine options (window, transitions, etc.)
│   ├── screens.rpy                  # Core screen definitions
│   ├── gui.rpy                      # GUI style configuration
│   ├── styles_and_transforms.rpy    # Custom ATL transforms and styles
│   ├── 01_image_transforms.rpy      # Image transform definitions
│   ├── 01compiler_flags_ren.py      # Compile-time feature flags
│   ├── _image_definitions_ren.py    # Shared image/composite definitions
│   │
│   ├── major_game_classes/          # Core data-model classes (Python)
│   │   ├── character_related/       # Person, Opinion, Progression, Schedule,
│   │   │                            #   Story_Tracker, Personality, Relationship,
│   │   │                            #   Appointment, ActiveJob, Scene/ProgressionScene
│   │   ├── business_related/        # Business, Contract, ProductionLine,
│   │   │                            #   Policy, Infraction, Punishment,
│   │   │                            #   ToyBlueprint/ToyDesign/ToyAttribute/ToyItem/Printer
│   │   ├── serum_related/           # SerumDesign, SerumTrait, SerumTraitBlueprint,
│   │   │                            #   SerumInventory + individual serum trait files
│   │   ├── clothing_related/        # Clothing, Outfit, Wardrobe, Expression,
│   │   │                            #   UniformOutfit, WardrobeBuilder, WardrobePreference
│   │   └── game_logic/              # Action, ActionList, Duty, Position, Room,
│   │                                #   RoomObject, ListenerManagementSystem
│   │
│   ├── main_character/              # MC class, goals, perks, MC serums, clarity mechanic
│   ├── people/                      # Per-character story files (one sub-folder per NPC)
│   │   └── <Name>/                  # Definition, story events, role definitions, etc.
│   │
│   ├── crises/                      # Random / scheduled event system
│   │   ├── regular_crises/          # Standard repeating crises + definitions
│   │   ├── limited_time_crises/     # One-shot / time-limited events + definitions
│   │   ├── location_events/         # Location-specific room events
│   │   └── settings/                # Crisis chance UI + configuration
│   │
│   ├── game_loops/                  # Core game-loop scripts
│   │   ├── advance_time.rpy         # Day/time-of-day progression, end-of-day logic
│   │   └── sexmechanic*.rpy         # Sex scene state machine and position logic
│   │
│   ├── game_screens/                # Ren'Py screen definitions (UI)
│   │   ├── business_screens/        # Company overview, employee management, policies,
│   │   │                            #   engineering (toy blueprint/design/printer UI)
│   │   ├── character_screens/       # Character info, story progress, relationship views
│   │   ├── clothing_screens/        # Wardrobe and outfit management
│   │   ├── configuration_screens/   # Game settings and preferences
│   │   ├── serum_management_screens/# Serum design, blueprint, and inventory screens
│   │   ├── hud_screens/             # In-game HUD overlays (incl. sex_toy_admin_app)
│   │   ├── hints/                   # Context-sensitive hint system
│   │   ├── subscreens/              # Reusable sub-screen components
│   │   └── tooltip_screens/         # Tooltip definitions
│   │
│   ├── general_actions/             # Shared NPC interaction scripts
│   │   ├── interaction_actions/     # Talk, grope, strip, bar-date, activity actions
│   │   │   └── activities/          # Specific activity sub-scenes
│   │   └── location_actions/        # Location-specific action menus
│   │
│   ├── plotlines/                   # Major standalone story arcs
│   │   ├── StripClub/               # Strip club acquisition and management
│   │   └── SideCharacter/           # Side-character stories (Chemist's daughter, etc.)
│   │
│   ├── map/                         # World map and hub navigation system
│   │   ├── MapHub_ren.py            # Hub definitions (home, office, bar, gym, …)
│   │   ├── HomeHub_ren.py           # Home sub-hub definitions
│   │   └── map_screen.rpy           # Map UI screen
│   │
│   ├── game_roles/                  # Role system (employee, pregnant, strip club, etc.)
│   │   ├── business_roles/          # Employee, intern, secretary, clone roles
│   │   ├── pregnant_roles/          # Pregnancy state roles
│   │   ├── stripclub/               # Strip club performer roles
│   │   └── role_insta_definition_ren.py  # InstaPic / OnlyFanatics role logic,
│   │                                #   DM actions, photo-history management
│   │
│   ├── helper_functions/            # Utility / helper modules
│   │   ├── business_related/        # Business-logic helpers
│   │   ├── character_related/       # Character-logic helpers
│   │   ├── clothing_related/        # Clothing helpers
│   │   ├── game_logic/              # General game-logic helpers
│   │   ├── serum_related/           # Serum helpers
│   │   └── *.py                     # Misc helpers: sounds, formatting, display,
│   │                                #   random generation, web colours, XML wardrobe
│   │
│   ├── business_policies/           # Policy class instances (clothing, org, recruitment)
│   ├── personality_types/           # Personality definitions (relaxed, alpha, etc.)
│   ├── trainables/                  # Trainable stat / behaviour definitions
│   ├── fetish/                      # Fetish arc management
│   ├── sex_positions/               # Sex position definitions and media references
│   ├── wardrobes/                   # Character-specific XML wardrobe data
│   ├── cheats/                      # Cheat / debug menu scripts
│   ├── mods/                        # Modding entry point / example structure
│   ├── templates/                   # Code templates for content creators
│   ├── text_tags/                   # Custom Ren'Py text tag definitions
│   ├── fonts/                       # Bundled font files
│   ├── images/                      # Bundled game images (sprites, backgrounds, UI)
│   ├── bugfix_additions/            # Utility patches and debug helpers
│   ├── python-packages/             # Vendored pure-Python packages (e.g. pylru)
│   ├── saves/                       # Ren'Py save-game directory
│   ├── cache/                       # Ren'Py bytecode / image cache
│   ├── LICENCE.txt                  # Project licence
│   ├── Roadmap.txt                  # Rolling 6-month development roadmap
│   └── character_guide.txt          # Detailed in-game mechanic and character guide
│
├── Release-Notes.md                 # Changelog / patch notes
├── LR2RAiO.ps1                      # PowerShell "All-in-One" installer / launcher script
├── LR2.code-workspace               # VS Code workspace configuration
├── icon.ico / icon.icns             # Application icons
└── .gitignore / .gitattributes      # Git configuration
```

### Architecture Highlights

- **Init order** — Ren'Py's `init` priority system is used deliberately: `-50` imports external libraries, `-5` defines all classes, `-2` instantiates game objects (characters, policies, roles), `0` sets engine options and callbacks.
- **`_ren.py` convention** — Python files that must be accessible at init time (class definitions, constants) use the `_ren.py` suffix so Ren'Py treats them as early-loaded init Python rather than screens.
- **Modular character folders** — Each named character lives in `game/people/<Name>/` and owns her definition file, story event scripts, and any role/duty definitions. This isolates per-character changes.
- **Action / ActionList pattern** — Interactions are modelled as `Action` objects collected into `ActionList`s, enabling dynamic filtering and display without scattering `if` checks across every screen.
- **Story_Tracker / Progression** — Story state is centralised in `Story_Tracker` and `Progression` objects stored on each `Person`, giving a single source of truth for "which events have fired".
- **Crisis system** — Crises are registered at init and evaluated each time step against current game state, keeping event logic decoupled from the main game loop.
- **Role system** — Gameplay states (employee, pregnant, strip-club performer, harem member, …) are represented as `Role` objects attached to `Person` instances, keeping state transitions clean.

---

## Areas That Can Be Improved

### 1. Documentation
- **Missing top-level README** — There is no `README.md` at the repository root. New contributors must read `Roadmap.txt`, `character_guide.txt`, and `Release-Notes.md` separately to get an overview.
- **Inline comments** — Many large `.rpy` story files have sparse comments explaining *why* conditions are required, making it hard to trace intent during review or modding.
- **Class API docs** — Core classes (`Person`, `Business`, `SerumDesign`, etc.) lack docstrings on their public methods and properties.

### 2. Code Structure & Maintainability
- **God-class `Person`** — `Person_ren.py` imports from almost every other module in the project and handles character state, display, wardrobe, scheduling, story tracking, and serum administration in a single class. Extracting focused sub-systems (e.g. a dedicated `CharacterDisplay` or `SerumHandler`) would reduce coupling and import cycles.
- **Duplicated story-event boilerplate** — Many character story files repeat the same time-delay checks, story-flag tests, and "is she available" guard conditions. A shared story-event decorator or base-class helper could eliminate this duplication (the `Story_Tracker` class is a step in this direction but not uniformly adopted).
- **`.rpy.back` files committed** — The `game/plotlines/SideQuests/` directory contains `.rpy.back` backup files. These are editor artefacts and should be removed and added to `.gitignore`.
- **Hard-coded magic numbers** — Stat thresholds (e.g. `sluttiness >= 30`, `love >= 60`, `obedience >= 130`) are scattered across individual story files with no named constants, making balance tweaks fragile and error-prone.
- **`errors.txt` and `log.txt` in the repo root** — Runtime log files are committed to the repository. They should be excluded via `.gitignore`.

### 3. Testing & Quality Assurance
- **No automated tests** — There is no test suite (unit, integration, or otherwise). Ren'Py logic can be unit-tested by importing `_ren.py` files in a standard Python environment; adding even basic tests for helper functions and class invariants would catch regressions.
- **`errors.txt` suggests runtime errors exist** — The committed error log hints at unhandled edge cases in production code that have not yet been addressed.
- **Inconsistent save-game compatibility** — New story-path features explicitly note save-game compatibility as a goal, but there is no migration/versioning layer to guarantee forward compatibility when new attributes are added to persisted classes.

### 4. Performance
- **Image pre-loading** — `config.predict_statements = 32` is set, but high-resolution composite character images can cause hitching when first displayed. A more aggressive pre-load or lazy-load strategy with placeholders would smooth transitions.
- **`config.cache_surfaces = False`** — Disabled surface caching is appropriate for memory-constrained devices but may cause unnecessary re-renders on higher-end hardware; making this a user preference would broaden compatibility.

### 5. Modding & Extensibility
- **Partially adopted Story Path system** — The alpha "Story Paths" feature (for save-game safe modding) exists but only covers a few characters. Completing the migration would make the game significantly more mod-friendly.
- **Mod entry point is underdeveloped** — `game/mods/` exists but contains minimal scaffolding. A documented mod API with example files and a mod-loading manifest would lower the barrier for community contributions.
- **`get_named_label_ren.py` for scene overrides** — This helper is mentioned in the release notes as a way to do character-specific scene overrides for modders, but it is not yet documented in the character guide.

### 6. Player Experience
- **Scheduling system is Alpha** — The scheduling system exists but most story events are not yet wired into it. Completing this integration would improve discoverability of upcoming events.
- **Incomplete arcs** — Several characters (e.g. Jennifer's Personal Secretary arc, Nora's Love arc) have placeholder content. Filling these in would reduce player confusion when a story arc suddenly ends.
- **Pregnant women can drink** — Noted explicitly in the release notes as an unfixed bug. A simple check on pregnancy state in the bar-date drink-serving logic would resolve this.
- **Scene Popups preference** — The preference to show/hide scene popups was added but not all scenes have been retrofitted with popup support; a systematic pass would ensure consistent behaviour.

---

## Clothing Draw Component Image Format

All clothing draw components — including skirts, bracelets, tops, shoes, and every other wearable item — are stored as **PNG image files packed inside ZIP archives**.

### File Locations

ZIP files live under `game/images/character_images/` and are organised **one ZIP per render position**:

```
game/images/character_images/stand2.zip
game/images/character_images/stand3.zip
game/images/character_images/stand4.zip
game/images/character_images/stand5.zip
game/images/character_images/walking_away.zip
game/images/character_images/kissing.zip
game/images/character_images/doggy.zip
game/images/character_images/missionary.zip
game/images/character_images/blowjob.zip
game/images/character_images/against_wall.zip
game/images/character_images/back_peek.zip
game/images/character_images/sitting.zip
game/images/character_images/kneeling1.zip
game/images/character_images/standing_doggy.zip
game/images/character_images/cowgirl.zip
```

A separate `character_images.zip` is used as an override layer for mod-supplied images.

### Image Naming Convention

Every PNG inside a ZIP follows this naming pattern:

```
{proper_name}_{position}_{body_type}_{breast_size}.png
```

| Segment | Values | Notes |
|---|---|---|
| `proper_name` | e.g. `Skirt`, `Copper_Bracelet`, `Mini_Skirt` | The `proper_name` field set when the `Clothing` object is created in `clothing_lists_ren.py`. Uses underscores. |
| `position` | `stand2`, `stand3`, … (see list above) | Matches the ZIP filename (without `.zip`). |
| `body_type` | `standard_body`, `thin_body`, `curvy_body`, `standard_preg_body` | Body-independent items always use `standard_body`. |
| `breast_size` | `AA`, `A`, `B`, `C`, `D`, `DD`, `DDD`, `E`, `F`, `FF` | Non-breast items always use `AA`; breast items include all sizes. |

> **Body & breast variants:** Items that do not vary with body shape (e.g. bracelets, earrings) are created with `body_dependant=False` and only ever use `standard_body`, so a single image covers all body types. Items that do not draw or depend on breast shape (e.g. skirts, shoes) are created with `draws_breasts=False` and only ever use `AA`, so a single image covers all cup sizes. Only tops and bras that set `draws_breasts=True` require a separate image for each of the ten breast sizes across each body type.

**Examples:**

- `Skirt_stand2_standard_body_AA.png` — a basic skirt in the standing pose (skirts are not breast-dependent and not body-shape-dependent).
- `Copper_Bracelet_stand3_standard_body_AA.png` — a copper bracelet in an alternate standing pose.
- `Corset_doggy_curvy_body_DD.png` — a corset in the doggy position for a curvy body with DD cup (corsets draw breasts and vary with body type).

### How the Runtime Uses These Images

At init time, `Clothing_Images` (in `major_game_classes/clothing_related/Clothing_Images_ren.py`) pre-computes the expected filenames for every combination of body type and breast size and caches them as strings. `ZipContainer` (in `zip_manager_ren.py`) resolves the string to actual pixel data on demand via an LRU cache, reading from the appropriate position ZIP file. If the primary ZIP does not contain a file, `character_images.zip` is checked next, which is the intended override point for mods.
