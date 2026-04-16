from __future__ import annotations
import builtins
from game.bugfix_additions.mapped_list_ren import generate_identifier
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init -2 python:
"""

# Location IDs that require the "Extra Robust" attribute to use a toy there.
# Covers gym, all sports-centre areas, and shower locations.
ACTIVE_LOCATIONS = frozenset([
    "gym",
    "gym_shower",
    "sports_center_pool",
    "sports_center_reception",
    "sports_center_tennis_courts",
    "home_shower",
])

# Name of the ToyAttribute that makes a toy safe to use at active locations.
EXTRA_ROBUST_ATTR = "Extra Robust"


class ToyBlueprint():
    """A node in the sex toy research tree. Must be researched before ToyDesigns using it can be manufactured."""
    def __init__(self, name: str, desc: str, research_needed: int = 50,
            requires: list[ToyBlueprint] | ToyBlueprint | None = None,
            tier: int = 0, start_researched: bool = False,
            production_cost: int = 5, base_value: int = 20,
            power: int = -1, arousal_rating: int = 0,
            usage: tuple[str, ...] = ("installed", "manual"),
            toy_type: str = "vaginal",
            min_sluttiness: int = 0):
        self.name = name
        self.desc = desc
        self.research_needed = research_needed
        self.current_research = 0.0
        self.researched = start_researched

        if requires is None:
            self.requires = []
        elif isinstance(requires, (list, tuple)):
            self.requires = list(requires)
        else:
            self.requires = [requires]

        self.tier = tier
        self.production_cost = production_cost  # supplies consumed per unit
        self.base_value = base_value  # base sale value per unit
        self.power = power  # base power draw of the design (negative = consumes power)
        self.arousal_rating = max(-5, min(5, arousal_rating))  # base arousal added when using the toy (-5 to 5)
        self.usage = tuple(usage)  # allowed usage modes: any subset of ("installed", "manual")
        self.toy_type = toy_type  # "anal" or "vaginal" — determines upgrade/ownership slot
        self.min_sluttiness = max(0, min(100, min_sluttiness))  # NPC must have at least this sluttiness to purchase

        self.identifier = generate_identifier((self.name,))

    def __eq__(self, other: ToyBlueprint) -> bool:
        if not isinstance(other, ToyBlueprint):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return self.identifier

    @property
    def is_unlockable(self) -> bool:
        """True when all prerequisite blueprints have been researched."""
        if self.requires and any(not r.researched for r in self.requires):
            return False
        return True

    @property
    def module_space(self) -> int:
        """Number of attribute slots available for toy designs using this blueprint.
        Tier 1 = 2 slots, with one additional slot per tier above 1."""
        return getattr(self, 'tier', 1) + 1

    @property
    def max_intensity(self) -> int:
        """Maximum intensity setting for toys built from this blueprint.
        Tier 1 = 3, tier 2 = 6, tier 3 = 10."""
        t = getattr(self, 'tier', 1)
        if t <= 1:
            return 3
        if t == 2:
            return 6
        return 10

    def add_research(self, amount: float) -> bool:
        """Add research points. Returns True when research is completed."""
        self.current_research += amount
        if self.current_research >= self.research_needed:
            self.current_research = self.research_needed
            self.researched = True
            return True
        return False

    @property
    def research_percentage(self) -> float:
        if self.research_needed <= 0:
            return 1.0
        return self.current_research / self.research_needed


class ToyAttribute():
    """A researchable add-on feature for toy designs (e.g. GPS, electro stimulator, diagnostics)."""
    def __init__(self, name: str, desc: str, research_needed: int = 50,
            requires: list[ToyAttribute] | ToyAttribute | None = None,
            production_cost_add: int = 2, value_add: int = 10,
            power_add: int = -1, arousal_rating_add: int = 0,
            module_space_add: int = 0):
        self.name = name
        self.desc = desc
        self.research_needed = research_needed
        self.current_research = 0.0
        self.researched = False

        if requires is None:
            self.requires = []
        elif isinstance(requires, (list, tuple)):
            self.requires = list(requires)
        else:
            self.requires = [requires]

        self.production_cost_add = production_cost_add  # extra production cost when added to a design
        self.value_add = value_add  # extra sale value when added to a design
        self.power_add = power_add  # power budget change (positive = provides power, negative = draws power)
        self.arousal_rating_add = max(-5, min(5, arousal_rating_add))  # arousal contribution when added to a design (-5 to 5)
        self.module_space_add = module_space_add  # bonus module slots granted to the design when this attribute is installed

        self.identifier = generate_identifier((self.name, "attribute"))

    def __eq__(self, other: ToyAttribute) -> bool:
        if not isinstance(other, ToyAttribute):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return self.identifier

    @property
    def is_unlockable(self) -> bool:
        """True when all prerequisite attributes have been researched."""
        if self.requires and any(not r.researched for r in self.requires):
            return False
        return True

    def add_research(self, amount: float) -> bool:
        """Add research points. Returns True when research is completed."""
        self.current_research += amount
        if self.current_research >= self.research_needed:
            self.current_research = self.research_needed
            self.researched = True
            return True
        return False

    @property
    def research_percentage(self) -> float:
        if self.research_needed <= 0:
            return 1.0
        return self.current_research / self.research_needed


class ToyDesign():
    """A sex toy design that can be manufactured once its blueprint is researched.
    Attributes can be added to increase its value and production cost."""
    def __init__(self, blueprint: ToyBlueprint):
        self.blueprint = blueprint
        self.name = blueprint.name
        self._base_production_cost = blueprint.production_cost
        self._base_value = blueprint.base_value
        self.attributes: list[ToyAttribute] = []
        self.identifier = generate_identifier((self.name, "design"))

    def __eq__(self, other: ToyDesign) -> bool:
        if not isinstance(other, ToyDesign):
            return NotImplemented
        return self.identifier == other.identifier

    def __hash__(self) -> int:
        return self.identifier

    @property
    def is_ready(self) -> bool:
        return self.blueprint.researched

    @property
    def production_cost(self) -> int:
        attrs = getattr(self, 'attributes', [])
        return self._base_production_cost + sum(a.production_cost_add for a in attrs)

    @property
    def base_value(self) -> int:
        attrs = getattr(self, 'attributes', [])
        return self._base_value + sum(a.value_add for a in attrs)

    @property
    def total_power(self) -> int:
        """Net power budget: blueprint base draw plus all component adjustments."""
        attrs = getattr(self, 'attributes', [])
        return getattr(self.blueprint, 'power', -1) + sum(getattr(a, 'power_add', -1) for a in attrs)

    @property
    def total_arousal_rating(self) -> int:
        """Net arousal rating: blueprint base arousal plus all component contributions (clamped to -5..5)."""
        attrs = getattr(self, 'attributes', [])
        raw = getattr(self.blueprint, 'arousal_rating', 0) + sum(getattr(a, 'arousal_rating_add', 0) for a in attrs)
        return max(-5, min(5, raw))

    def can_add_attribute(self, attr: ToyAttribute) -> bool:
        """Check if an attribute can be added to this design.
        Batteries (power_add > 0) are exempt from module space limits."""
        if not attr.researched:
            return False
        attrs = getattr(self, 'attributes', [])
        if attr in attrs:
            return False
        if getattr(attr, 'power_add', -1) <= 0:
            non_battery_count = sum(1 for a in attrs if getattr(a, 'power_add', -1) <= 0)
            bp_module_space = getattr(self.blueprint, 'module_space', 2)
            added_space = sum(getattr(a, 'module_space_add', 0) for a in attrs)
            if non_battery_count >= bp_module_space + added_space:
                return False
        return True

    def add_attribute(self, attr: ToyAttribute) -> bool:
        """Add a researched attribute to this design. Returns True on success."""
        if not self.can_add_attribute(attr):
            return False
        if not hasattr(self, 'attributes'):
            self.attributes = []
        self.attributes.append(attr)
        return True

    def remove_attribute(self, attr: ToyAttribute):
        """Remove an attribute from this design."""
        attrs = getattr(self, 'attributes', [])
        if attr in attrs:
            attrs.remove(attr)


class ToyItem():
    """A single manufactured toy instance that can be carried and installed on an NPC."""
    def __init__(self, design: ToyDesign):
        self.design = design
        self.name = design.name
        self.installed = False  # True when actively in use (e.g. a butt plug being worn)
        self.intensity = 0     # Current intensity level (0 when not installed, 1..max when installed)
        self.switched_off_until = 0  # Day number until which the toy is switched off (0 = not on cooldown)

    def __eq__(self, other: ToyItem) -> bool:
        if not isinstance(other, ToyItem):
            return NotImplemented
        return self is other  # each physical item is unique

    def __hash__(self) -> int:
        return id(self)

    def install(self):
        """Mark this toy as installed / actively in use."""
        self.installed = True
        self.intensity = 1

    def uninstall(self):
        """Mark this toy as no longer installed."""
        self.installed = False
        self.intensity = 0

    @property
    def is_switched_off(self) -> bool:
        """True when the toy was auto-uninstalled and is still in its cooldown period."""
        return getattr(self, 'switched_off_until', 0) > day

    @property
    def max_intensity(self) -> int:
        """Maximum intensity this toy supports, based on blueprint tier."""
        return getattr(self.design.blueprint, 'max_intensity', 3)

    @property
    def valid_usages(self) -> tuple[str, ...]:
        """Allowed usage modes for this toy type: any subset of ('installed', 'manual').

        Falls back to both modes for ToyItem objects loaded from saves created before the
        usage attribute was added to ToyBlueprint.
        """
        return getattr(self.design.blueprint, 'usage', ("installed", "manual"))

    @property
    def toy_type(self) -> str:
        """Toy category: 'anal' for butt plugs, 'vaginal' for all other toys.

        Falls back to 'vaginal' for items loaded from saves created before toy_type was added.
        """
        return getattr(self.design.blueprint, 'toy_type', 'vaginal')

    def is_valid_for_location(self, location_id: str) -> bool:
        """Return True if this toy can remain installed at the given location.

        Active locations (gym, sports centre, pool, showers) require the toy to
        have the EXTRA_ROBUST_ATTR attribute applied to the design.
        """
        if location_id not in ACTIVE_LOCATIONS:
            return True
        attrs = getattr(self.design, 'attributes', [])
        return any(getattr(a, 'name', '') == EXTRA_ROBUST_ATTR for a in attrs)


class Printer():
    """A 3D printer that manufactures sex toys. Similar to ProductionLine for serums."""
    def __init__(self, name: str = "Basic 3D Printer", speed_modifier: float = 1.0, cost: int = 0):
        self.name = name
        self.speed_modifier = speed_modifier  # multiplier on manufacture output
        self.cost = cost  # purchase cost
        self.selected_design: ToyDesign | None = None
        self.spare_production_points: int = 0
        self.items_to_produce: int = 0  # 0 = unlimited; positive = stop after this many
        self._items_produced: int = 0  # running count toward items_to_produce target

    def set_product(self, design: ToyDesign | None):
        if self.selected_design == design:
            return
        self.spare_production_points = 0
        self._items_produced = 0
        self.selected_design = design

    def add_production(self, production_points: int) -> int:
        """Add production points and return number of toys produced.

        If items_to_produce > 0, stops producing once that many have been made
        (across all calls; reset by set_product() or clear_product()).
        """
        if not self.selected_design or not self.selected_design.is_ready:
            return 0

        # Defensive init for save-game objects created before these attrs existed.
        if not hasattr(self, 'items_to_produce'):
            self.items_to_produce = 0
        if not hasattr(self, '_items_produced'):
            self._items_produced = 0

        target = self.items_to_produce
        if target > 0 and self._items_produced >= target:
            return 0

        effective = builtins.int(production_points * self.speed_modifier)
        self.spare_production_points += effective
        toys_produced = 0

        cost = max(self.selected_design.production_cost, 1)
        while self.spare_production_points >= cost:
            if target > 0 and self._items_produced + toys_produced >= target:
                break
            self.spare_production_points -= cost
            toys_produced += 1

        self._items_produced += toys_produced
        return toys_produced

    def clear_product(self):
        self.spare_production_points = 0
        self._items_produced = 0
        self.selected_design = None

    @property
    def progress_percentage(self) -> float:
        if not self.selected_design:
            return 0.0
        cost = max(self.selected_design.production_cost, 1)
        return self.spare_production_points / cost


def init_toy_blueprints(business):
    """Initialize the sex toy design research tree and add blueprints to the business.

    Power convention: tier 1 = -4, tier 2 = -3, tier 3 = -2.
    Higher-tier blueprints are more efficient and draw less power.

    Usage convention:
      "manual"    - hand-operated; cannot be left installed unattended
      "installed" - worn/inserted; can remain in place while the bearer moves around
    Some types support both modes.
    """
    # Tier 1 - Basic designs (no prerequisites) — 250 pts (5 sessions × 50 pts/session)
    basic_vibrator = ToyBlueprint("Basic Vibrator",
        "A simple vibrating toy. The entry-level product for any adult toy line.",
        research_needed=250, tier=1, production_cost=3, base_value=15, power=-4, arousal_rating=2,
        usage=("installed", "manual"))

    basic_dildo = ToyBlueprint("Basic Dildo",
        "A straightforward silicone dildo. A timeless classic.",
        research_needed=250, tier=1, production_cost=3, base_value=15, power=-4, arousal_rating=2,
        usage=("manual",))

    basic_plug = ToyBlueprint("Basic Plug",
        "A simple butt plug design. Small but popular.",
        research_needed=250, tier=1, production_cost=3, base_value=15, power=-4, arousal_rating=1,
        usage=("installed",), toy_type="anal")

    # Tier 2 - Advanced designs (require tier 1) — 500 pts (10 sessions × 50 pts/session)
    remote_vibrator = ToyBlueprint("Intensity Control Vibrator",
        "Multi intensity settings on vibrator with possible remote control if module is installed.",
        research_needed=500, tier=2, requires=basic_vibrator,
        production_cost=5, base_value=30, power=-3, arousal_rating=3,
        usage=("installed", "manual"))

    # tier=3 gives module_space = tier+1 = 4 (one extra slot over the Intensity Control
    # Vibrator's 3); research cost is kept at 500 to match Intensity Control Vibrator.
    egg_vibrator = ToyBlueprint("Egg Vibrator",
        "A small, discreet insertable vibrating egg. Designed to be worn throughout the day.",
        research_needed=500, tier=3, requires=basic_vibrator,
        production_cost=5, base_value=30, power=-3, arousal_rating=3,
        usage=("installed",))

    realistic_dildo = ToyBlueprint("Realistic Dildo",
        "A lifelike dildo with detailed texture and suction cup base.",
        research_needed=500, tier=2, requires=basic_dildo,
        production_cost=5, base_value=30, power=-3, arousal_rating=3,
        usage=("manual",))

    vibrating_plug = ToyBlueprint("Vibrating Plug",
        "A butt plug with built-in vibration motor.",
        research_needed=500, tier=2, requires=[basic_plug, basic_vibrator],
        production_cost=5, base_value=30, power=-3, arousal_rating=3,
        usage=("installed",), toy_type="anal")

    # Tier 3 - Premium designs (require tier 2) — 750 pts (15 sessions × 50 pts/session)
    luxury_wand = ToyBlueprint("Luxury Wand Massager",
        "A powerful wand-style massager with whisper-quiet motor.",
        research_needed=750, tier=3, requires=remote_vibrator,
        production_cost=8, base_value=60, power=-2, arousal_rating=4,
        usage=("manual",))

    couples_set = ToyBlueprint("Couples Toy Set",
        "A matching set of complementary toys designed for partners.",
        research_needed=750, tier=3, requires=[realistic_dildo, remote_vibrator],
        production_cost=10, base_value=60, power=-2, arousal_rating=4,
        usage=("installed",))

    vibrating_plug_xl = ToyBlueprint("Vibrating Plug XL",
        "An oversized vibrating plug with a powerful motor and extra-wide base for secure wear.",
        research_needed=750, tier=3, requires=vibrating_plug,
        production_cost=9, base_value=55, power=-2, arousal_rating=4,
        usage=("installed",), toy_type="anal")

    business.toy_blueprints = [
        basic_vibrator, basic_dildo, basic_plug,
        remote_vibrator, egg_vibrator, realistic_dildo, vibrating_plug,
        luxury_wand, couples_set, vibrating_plug_xl
    ]


def init_toy_attributes(business):
    """Initialize the toy attribute research tree and add attributes to the business.

    Power convention: batteries have positive power_add; all other components draw power
    (negative power_add).  Higher-tier components draw progressively more power.
    Tier 1 draw: 0 to -2.  Tier 2 draw: -3 to -4.  Tier 3 draw: -4 to -6.
    """
    # --- Battery components (positive power_add, no prerequisites) ---
    basic_battery = ToyAttribute("Basic Battery",
        "A compact rechargeable cell providing reliable power for entry-level designs.",
        research_needed=150, production_cost_add=1, value_add=5, power_add=5, arousal_rating_add=0)

    enhanced_battery = ToyAttribute("Enhanced Battery",
        "High-capacity lithium pack with extended runtime and faster charging.",
        research_needed=400, requires=basic_battery,
        production_cost_add=2, value_add=10, power_add=10, arousal_rating_add=0)

    power_cell = ToyAttribute("Power Cell",
        "Advanced solid-state cell delivering sustained high-output power for premium components.",
        research_needed=750, requires=enhanced_battery,
        production_cost_add=4, value_add=18, power_add=15, arousal_rating_add=0)

    # --- Tier 1 components (no prerequisites, draw 0 to -2 power) ---
    bluetooth_module = ToyAttribute("Bluetooth Module",
        "Adds short-range wireless connectivity for device-to-device control.",
        research_needed=100, production_cost_add=1, value_add=6, power_add=-1, arousal_rating_add=0)

    cellular_module = ToyAttribute("Internet Connection, with Bluetooth",
        "Adds internet connectivity and Bluetooth for app-based remote control from anywhere.",
        research_needed=250, production_cost_add=2, value_add=10, power_add=-2, arousal_rating_add=0)

    led_lighting = ToyAttribute("LED Lighting",
        "Ambient LED lighting with multiple color modes.",
        research_needed=150, production_cost_add=1, value_add=5, power_add=-1, arousal_rating_add=0)

    extra_robust = ToyAttribute("Extra Robust",
        "Rated to 100 meters water depth and shock proof — ideal for more active users.",
        research_needed=200, production_cost_add=2, value_add=8, power_add=0, arousal_rating_add=0)

    electro_heat_transfer = ToyAttribute("Electro Heat Transfer",
        "A thermoelectric module that harvests heat from operation and feeds it back as charge, adding +5 to the power budget.",
        research_needed=300, production_cost_add=2, value_add=10, power_add=5, arousal_rating_add=0)

    pressure_sensors = ToyAttribute("Pressure Sensors",
        "Internal pressure sensors that adjust intensity based on grip strength.",
        research_needed=250, production_cost_add=2, value_add=12, power_add=-1, arousal_rating_add=1)

    # --- Tier 2 components (require tier 1, draw -3 to -4 power) ---
    gps_tracker = ToyAttribute("GPS Tracker",
        "Built-in GPS module for location tracking and anti-theft features.",
        research_needed=450, requires=cellular_module,
        production_cost_add=3, value_add=15, power_add=-3, arousal_rating_add=0)

    electro_stimulator = ToyAttribute("Electro Stimulator",
        "E-stim pads that deliver adjustable electrical pulses for enhanced stimulation.",
        research_needed=600, requires=cellular_module,
        production_cost_add=4, value_add=20, power_add=-4, arousal_rating_add=5)

    electro_shocker = ToyAttribute("Electro Shocker",
        "High-voltage shock pads that deliver sharp, punishing electrical bursts — deeply unpleasant and highly effective.",
        research_needed=750, requires=electro_stimulator,
        production_cost_add=5, value_add=22, power_add=-4, arousal_rating_add=-5)

    temperature_control = ToyAttribute("Temperature Control",
        "Heating and cooling elements for adjustable temperature play.",
        research_needed=400, requires=extra_robust,
        production_cost_add=3, value_add=15, power_add=-3, arousal_rating_add=2)

    # --- Tier 3 components (require tier 2, draw -4 to -6 power) ---
    diagnostics_module = ToyAttribute("Diagnostics Module",
        "Health monitoring sensors that track heart rate, body temperature, and usage analytics.",
        research_needed=700, requires=[pressure_sensors, cellular_module],
        production_cost_add=5, value_add=25, power_add=-3, arousal_rating_add=0)

    ai_adaptive = ToyAttribute("AI-Adaptive Patterns",
        "Machine learning algorithm that adapts stimulation patterns to user preferences over time.",
        research_needed=1000, requires=[diagnostics_module, electro_stimulator],
        production_cost_add=6, value_add=35, power_add=-6, arousal_rating_add=3)

    haptic_feedback = ToyAttribute("Haptic Feedback",
        "Advanced haptic motors for realistic touch feedback and long-distance partner sync.",
        research_needed=750, requires=[pressure_sensors, cellular_module],
        production_cost_add=4, value_add=20, power_add=-4, arousal_rating_add=2)

    pressure_point_stimulator = ToyAttribute("Pressure Point Stimulator",
        "Targeted micro-actuators that apply precise pressure to nerve clusters for deep tissue stimulation.",
        research_needed=800, requires=[electro_stimulator, haptic_feedback],
        production_cost_add=5, value_add=28, power_add=-5, arousal_rating_add=3)

    extension_module = ToyAttribute("Extension Module",
        "A modular chassis expansion that adds two additional component slots at the cost of one. Requires a robust casing to support the extra hardware.",
        research_needed=350, requires=extra_robust,
        production_cost_add=3, value_add=12, power_add=-1, arousal_rating_add=0,
        module_space_add=2)

    business.toy_attributes = [
        basic_battery, enhanced_battery, power_cell,
        bluetooth_module, cellular_module, led_lighting, extra_robust, electro_heat_transfer, pressure_sensors,
        gps_tracker, electro_stimulator, electro_shocker, temperature_control,
        diagnostics_module, ai_adaptive, haptic_feedback, pressure_point_stimulator,
        extension_module
    ]
