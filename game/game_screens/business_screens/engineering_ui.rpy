init 1 python:
    from game.major_game_classes.business_related.ToyDesign_ren import Printer, normalize_toy_lubricant_traits

    def buy_printer(name, speed, cost):
        mc.business.add_printer(Printer(name, speed_modifier=speed, cost=cost))

    def assign_design_to_printer(printer, design):
        """Assign a toy design to a printer. Clears the target counter."""
        printer.set_product(design)

    def set_printer_items_to_produce(printer, delta):
        """Adjust the printer's items_to_produce target by delta.
        When increasing: minimum is 0 (unlimited sentinel).
        When decreasing: minimum is _items_produced so remaining never slips
        below 0 and the printer doesn't accidentally switch to unlimited mode."""
        if not hasattr(printer, 'items_to_produce'):
            printer.items_to_produce = 0
        if not hasattr(printer, '_items_produced'):
            printer._items_produced = 0
        new_val = printer.items_to_produce + delta
        if delta < 0:
            printer.items_to_produce = max(printer._items_produced, new_val)
        else:
            printer.items_to_produce = max(0, new_val)

    def sell_printer(printer):
        """Sell a printer and remove it from the business."""
        mc.business.remove_printer(printer)

    def add_attribute_to_design(design, attr):
        design.add_attribute(attr)

    def remove_attribute_from_design(design, attr):
        design.remove_attribute(attr)

    def remove_toy_design(design):
        """Remove a completed toy design from the business's design list."""
        designs = getattr(mc.business, 'toy_designs', [])
        if design in designs:
            designs.remove(design)
            # Clear any stuck stock so the shop screen doesn't show an unsellable entry.
            toy_inv = getattr(mc.business, 'toy_inventory', {})
            toy_inv.pop(design.name, None)
            mc.business.toy_inventory = toy_inv
            # Unassign from any printer that was producing this design.
            for _printer in getattr(mc.business, 'printers', []):
                if getattr(_printer, 'selected_design', None) is design:
                    _printer.selected_design = None

    def assign_blueprint_research(bp):
        """Assign a blueprint for research and clear any active attribute research."""
        mc.business.active_toy_research = bp
        mc.business.active_attribute_research = None

    def assign_attribute_research(attr):
        """Assign an attribute for research and clear any active blueprint research."""
        mc.business.active_attribute_research = attr
        mc.business.active_toy_research = None

    def lubricant_trait_allowed(selected_traits, trait):
        # Match the main serum designer's conflict rule: traits conflict when
        # they share any exclude tag.
        return not any(
            tag in getattr(existing, 'exclude_tags', [])
            for existing in selected_traits
            for tag in getattr(trait, 'exclude_tags', [])
        )

    def create_custom_toy_design(blueprint, battery, components, name, lubricant_traits = None):
        """Create a custom ToyDesign from chosen blueprint, battery, components and name."""
        design = ToyDesign(blueprint)
        design.add_attribute(battery)
        for comp in components:
            design.add_attribute(comp)
        design.set_lubricant_formula(lubricant_traits, mc.business.lubricant_duration)
        design.name = name.strip() if name else blueprint.name
        design.identifier = generate_identifier((design.name, "design"))
        if not hasattr(mc.business, 'toy_designs'):
            mc.business.toy_designs = []
        mc.business.toy_designs.append(design)
        mc.business.add_normal_message("New custom design created: " + design.name)

    def can_upgrade_design(design, sel_bp, sel_bat, sel_comps, sel_lubricant_traits = None):
        """Return True if the existing design can be upgraded to the selected blueprint/battery/components/lubricant.
        Requires: same blueprint, at least one different selection, new design at least as valuable."""
        if sel_bp is None or sel_bat is None:
            return False
        if design.blueprint is not sel_bp:
            return False
        attrs = getattr(design, 'attributes', [])
        existing_bat = next((a for a in attrs if getattr(a, 'power_add', 0) > 0), None)
        existing_comps_ids = frozenset(id(a) for a in attrs if getattr(a, 'power_add', 0) <= 0)
        new_comps_ids = frozenset(id(c) for c in sel_comps)
        existing_lube_ids = frozenset(id(s) for s in normalize_toy_lubricant_traits(getattr(design, 'lubricant_traits', [])))
        new_lube_ids = frozenset(id(s) for s in normalize_toy_lubricant_traits(sel_lubricant_traits))
        existing_lube_duration = getattr(design, 'lubricant_duration', mc.business.lubricant_duration)
        new_lube_duration = mc.business.lubricant_duration
        same_bat = existing_bat is sel_bat
        same_comps = existing_comps_ids == new_comps_ids
        same_lubes = existing_lube_ids == new_lube_ids and existing_lube_duration == new_lube_duration
        if same_bat and same_comps and same_lubes:
            return False
        new_val = getattr(sel_bp, 'base_value', 0) + getattr(sel_bat, 'value_add', 0) + sum(getattr(c, 'value_add', 0) for c in sel_comps)
        return new_val >= design.base_value

    def perform_toy_upgrade(design, sel_bat, sel_comps, sel_lubricant_traits, cost):
        """Upgrade an existing toy design's battery/components/lubricant in-place and deduct cost."""
        mc.business.change_funds(-cost, stat="Toy Upgrades")
        design.attributes = []
        design.add_attribute(sel_bat)
        for comp in sel_comps:
            design.add_attribute(comp)
        design.set_lubricant_formula(sel_lubricant_traits, mc.business.lubricant_duration)
        mc.business.add_normal_message(f"Design '{design.name}' has been upgraded!")

screen engineering_printers_ui():
    add paper_background_image
    modal True

    # Which printer's design picker is open (None = none)
    default picking_design_for = None

    vbox:
        xalign 0.5
        yalign 0.1
        spacing 10

        frame:
            background "#0a142688"
            xsize 1200
            vbox:
                spacing 5
                xalign 0.5

                frame:
                    background "#000080"
                    xfill True
                    text "3D Printer Management" style "menu_text_title_style" xalign 0.5

                frame:
                    background "#0a142688"
                    xfill True
                    xpadding 10
                    ypadding 10
                    vbox:
                        spacing 10
                        text "Active Printers: [len(mc.business.printers)]" style "menu_text_style"

                        for printer in mc.business.printers:
                            frame:
                                background "#4a7fc1cc"
                                xfill True
                                padding (2, 2)
                                frame:
                                    background "#1a1a2e88"
                                    xfill True
                                    xpadding 10
                                    ypadding 6
                                    vbox:
                                        spacing 4
                                        # Items-to-produce values computed once for use in both rows
                                        $ _itp = getattr(printer, 'items_to_produce', 0)
                                        $ _iproduced = getattr(printer, '_items_produced', 0)
                                        $ _remaining = max(0, _itp - _iproduced)

                                        # Row 1: printer name + current design status + total mfg cost
                                        hbox:
                                            spacing 20
                                            text "[printer.name] (Speed: [printer.speed_modifier]x)" style "menu_text_style" yalign 0.5

                                            if printer.selected_design:
                                                $ _unit_cost = printer.selected_design.production_cost
                                                $ _unit_cost_dollars = _unit_cost * 2
                                                if _itp > 0:
                                                    $ _total_mfg_dollars = _unit_cost_dollars * _remaining
                                                    text "Producing: [printer.selected_design.name]  {size=13}{color=#ffcc66}Total Mfg Cost: $[_total_mfg_dollars] ([_remaining] × $[_unit_cost_dollars]){/color}{/size}" style "menu_text_style" yalign 0.5
                                                else:
                                                    text "Producing: [printer.selected_design.name]  {size=13}{color=#ffcc66}Mfg Cost: $[_unit_cost_dollars]/unit | Sell Value: $[printer.selected_design.base_value]{/color}{/size}" style "menu_text_style" yalign 0.5
                                            else:
                                                text "{color=#ff4444}Idle - no design assigned{/color}" style "menu_text_style" yalign 0.5

                                            $ _sell_refund = int(printer.cost * 0.5)
                                            frame:
                                                background "#4a7fc1cc"
                                                padding (2, 2)
                                                yalign 0.5
                                                textbutton "Sell (refund $[_sell_refund])":
                                                    style "textbutton_style"
                                                    action [Function(sell_printer, printer), SetScreenVariable("picking_design_for", None)]

                                        # Row 2: Assign Design button + items-to-produce controls
                                        hbox:
                                            spacing 12
                                            yalign 0.5
                                            $ _ready_designs = [d for d in getattr(mc.business, 'toy_designs', []) if d.is_ready]

                                            frame:
                                                background "#4a7fc1cc"
                                                padding (2, 2)
                                                yalign 0.5
                                                textbutton "Assign Design":
                                                    style "textbutton_style"
                                                    sensitive (len(_ready_designs) > 0)
                                                    action If(picking_design_for is printer,
                                                        true=SetScreenVariable("picking_design_for", None),
                                                        false=SetScreenVariable("picking_design_for", printer))

                                            if printer.selected_design:
                                                frame:
                                                    background "#4a7fc1cc"
                                                    padding (2, 2)
                                                    yalign 0.5
                                                    textbutton "Clear Design":
                                                        style "textbutton_style"
                                                        action Function(assign_design_to_printer, printer, None)

                                            # Items-to-produce counter (shows remaining items, counts down to 0)
                                            text "Produce:" style "menu_text_style" yalign 0.5
                                            frame:
                                                background "#4a7fc1cc"
                                                padding (2, 2)
                                                yalign 0.5
                                                textbutton "<<":
                                                    style "textbutton_style"
                                                    sensitive (_remaining > 0)
                                                    action Function(set_printer_items_to_produce, printer, -10)
                                            frame:
                                                background "#4a7fc1cc"
                                                padding (2, 2)
                                                yalign 0.5
                                                textbutton "<":
                                                    style "textbutton_style"
                                                    sensitive (_remaining > 0)
                                                    action Function(set_printer_items_to_produce, printer, -1)
                                            text ("[_remaining]" if _itp > 0 else "∞") style "menu_text_style" yalign 0.5
                                            frame:
                                                background "#4a7fc1cc"
                                                padding (2, 2)
                                                yalign 0.5
                                                textbutton ">":
                                                    style "textbutton_style"
                                                    action Function(set_printer_items_to_produce, printer, 1)
                                            frame:
                                                background "#4a7fc1cc"
                                                padding (2, 2)
                                                yalign 0.5
                                                textbutton ">>":
                                                    style "textbutton_style"
                                                    action Function(set_printer_items_to_produce, printer, 10)

                                            # Total cost display to the right of produce controls
                                            if printer.selected_design:
                                                $ _item_value = printer.selected_design.base_value
                                                if _itp > 0:
                                                    $ _total_cost = _item_value * _remaining
                                                    $ _total_profit = _total_cost - (_unit_cost_dollars * _remaining)
                                                    text "{color=#ffcc66}Total value: $[_total_cost], Profit: $[_total_profit]{/color}" style "menu_text_style" yalign 0.5
                                                else:
                                                    $ _profit_per_item = _item_value - _unit_cost_dollars
                                                    text "{color=#ffcc66}$[_item_value]/item, Profit: $[_profit_per_item]/item{/color}" style "menu_text_style" yalign 0.5

                                        # Design picker (shown only when this printer is selected)
                                        if picking_design_for is printer:
                                            frame:
                                                background "#000030aa"
                                                xfill True
                                                xpadding 8
                                                ypadding 6
                                                vbox:
                                                    spacing 4
                                                    text "Select a design to assign:" style "menu_text_style" size 13
                                                    $ _ready_designs2 = [d for d in getattr(mc.business, 'toy_designs', []) if d.is_ready]
                                                    for design in _ready_designs2:
                                                        frame:
                                                            background "#4a7fc1cc"
                                                            padding (2, 2)
                                                            textbutton "[design.name] (Mfg Cost: [design.production_cost] pts | Sell Value: $[design.base_value])":
                                                                style "textbutton_style"
                                                                selected (printer.selected_design == design)
                                                                action [Function(assign_design_to_printer, printer, design), SetScreenVariable("picking_design_for", None)]
                                                    if not _ready_designs2:
                                                        text "No ready designs available. Complete a blueprint and create a design first." style "menu_text_style" size 13

                        null height 10
                        $ _printer_count = len(mc.business.printers)
                        $ _at_max = (_printer_count >= 3)
                        text ("Purchase New Printer: (max 3 owned)" if _at_max else "Purchase New Printer:") style "menu_text_style"
                        hbox:
                            spacing 10
                            frame:
                                background "#4a7fc1cc"
                                padding (2, 2)
                                textbutton "🖨️ Standard Printer ($1000)":
                                    style "textbutton_style"
                                    sensitive (not _at_max and mc.business.has_funds(1000))
                                    action Function(buy_printer, "Standard 3D Printer", 1.0, 1000)

                            frame:
                                background "#4a7fc1cc"
                                padding (2, 2)
                                textbutton "🖨️ High-Speed Printer ($2000)":
                                    style "textbutton_style"
                                    sensitive (not _at_max and mc.business.has_funds(2000))
                                    action Function(buy_printer, "High-Speed 3D Printer", 1.5, 2000)

                            frame:
                                background "#4a7fc1cc"
                                padding (2, 2)
                                textbutton "🖨️ Industrial Printer ($5000)":
                                    style "textbutton_style"
                                    sensitive (not _at_max and mc.business.has_funds(5000))
                                    action Function(buy_printer, "Industrial 3D Printer", 2.0, 5000)

                # Current Stock section
                frame:
                    background "#0a142688"
                    xfill True
                    xpadding 10
                    ypadding 10
                    vbox:
                        spacing 6
                        frame:
                            background "#000080"
                            xfill True
                            text "Current Toy Stock" style "menu_text_style" xalign 0.5
                        $ _toy_inv = getattr(mc.business, 'toy_inventory', {})
                        $ _toy_designs_map = {d.name: d for d in getattr(mc.business, 'toy_designs', [])}
                        if _toy_inv:
                            for _toy_name, _toy_qty in _toy_inv.items():
                                $ _d = _toy_designs_map.get(_toy_name)
                                $ _total_val = _toy_qty * (_d.base_value if _d else 0)
                                text "  [_toy_name]: [_toy_qty]  (total value: $[_total_val])" style "menu_text_style" size 14
                        else:
                            text "  No toys in stock." style "menu_text_style" size 14

        frame:
            xalign 0.5
            background "#4a7fc1cc"
            padding (2, 2)
            textbutton "Return":
                action Return()

screen engineering_blueprints_ui():
    add paper_background_image
    modal True

    default selected_design = None

    vbox:
        xalign 0.5
        yalign 0.0
        xsize 1200
        ysize 1.0
        spacing 0

        frame:
            background "#000080"
            xfill True
            text "Toy Research" style "menu_text_title_style" xalign 0.5

        # Shared current research status line
        frame:
            background "#0a142688"
            xfill True
            xpadding 10
            ypadding 6
            vbox:
                xfill True
                spacing 4
                if mc.business.active_toy_research:
                    $ _cur = mc.business.active_toy_research
                    text "Current Research: {color=#ffd700}[_cur.name]{/color} ([int(_cur.research_percentage * 100)]%) — Blueprint" style "menu_text_style" xalign 0.5
                elif getattr(mc.business, 'active_attribute_research', None):
                    $ _cur = mc.business.active_attribute_research
                    text "Current Research: {color=#ffd700}[_cur.name]{/color} ([int(_cur.research_percentage * 100)]%) — Attribute" style "menu_text_style" xalign 0.5
                else:
                    text "Current Research: None" style "menu_text_style" xalign 0.5
                text "Lubricant formula: {color=#ffd700}[mc.business.lubricant_trait_capacity]{/color} trait(s), {color=#ffd700}[mc.business.lubricant_duration]{/color} turn(s)" style "menu_text_style" xalign 0.5

        viewport:
            xfill True
            ysize 820
            draggable True
            mousewheel True
            scrollbars "vertical"
            vbox:
                spacing 0
                xfill True

                # Blueprint Research section
                frame:
                    background "#0a142688"
                    xfill True
                    padding (10, 10, 10, 0)
                    vbox:
                        spacing 10

                        frame:
                            background "#000080"
                            xfill True
                            text "Blueprint Research" style "menu_text_style" xalign 0.5

                        # Column headers
                        hbox:
                            xfill True
                            spacing 0
                            frame:
                                xsize 200
                                background "#00003088"
                                text "Name" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xsize 280
                                background "#00003088"
                                text "Description" style "menu_text_style" size 13 xalign 0.0
                            frame:
                                xsize 200
                                background "#00003088"
                                text "Research Cost" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xsize 100
                                background "#00003088"
                                text "Power" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xsize 100
                                background "#00003088"
                                text "Mod. Space" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xsize 100
                                background "#00003088"
                                text "Arousal" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xfill True
                                background "#00003088"
                                text "Assign" style "menu_text_style" size 13 xalign 0.5

                        $ _visible_bps = sorted(
                            [bp for bp in mc.business.toy_blueprints if bp.is_unlockable and not bp.researched],
                            key=lambda bp: bp.tier
                        )
                        vbox:
                            spacing 5
                            for bp in _visible_bps:
                                frame:
                                    background "#1a1a2e88"
                                    xfill True
                                    xpadding 0
                                    ypadding 3
                                    hbox:
                                            xfill True
                                            spacing 0
                                            yalign 0.5
                                            # Name column
                                            frame:
                                                xsize 200
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[bp.name]" style "menu_text_style" size 14 yalign 0.5
                                            # Description column
                                            frame:
                                                xsize 280
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[bp.desc]" style "menu_text_style" size 13 yalign 0.5
                                            # Research Cost column
                                            frame:
                                                xsize 200
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                if bp.researched:
                                                    text "{color=#24ed27}Researched{/color}" style "menu_text_style" size 13 yalign 0.5
                                                elif bp.current_research > 0:
                                                    text "[bp.research_needed] pts ([int(bp.research_percentage * 100)]%)" style "menu_text_style" size 13 yalign 0.5
                                                else:
                                                    text "[bp.research_needed] pts" style "menu_text_style" size 13 yalign 0.5
                                            # Power column
                                            frame:
                                                xsize 100
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                $ _bp_pwr = getattr(bp, 'power', -1)
                                                text "{color=#ff4444}[_bp_pwr]{/color}" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                            # Module Space column
                                            frame:
                                                xsize 100
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                $ _bp_mod_space = getattr(bp, 'module_space', 0)
                                                text "[_bp_mod_space]" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                            # Arousal column
                                            frame:
                                                xsize 100
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                $ _bp_arousal = getattr(bp, 'arousal_rating', 0)
                                                if _bp_arousal > 0:
                                                    text "{color=#24ed27}+[_bp_arousal]{/color}" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                                elif _bp_arousal < 0:
                                                    text "{color=#ff4444}[_bp_arousal]{/color}" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                                else:
                                                    text "0" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                            # Assign Research button column
                                            frame:
                                                xfill True
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                if not bp.researched and bp.is_unlockable:
                                                    textbutton "Assign Research":
                                                        style "textbutton_style"
                                                        xalign 1.0
                                                        yalign 0.5
                                                        selected (mc.business.active_toy_research == bp)
                                                        action Function(assign_blueprint_research, bp)

                        if not mc.business.toy_blueprints:
                            text "No toy blueprints available yet." style "menu_text_style"

                # Component Research section
                frame:
                    background "#0a142688"
                    xfill True
                    padding (10, 0, 10, 10)
                    vbox:
                        spacing 10

                        frame:
                            background "#000080"
                            xfill True
                            text "Attribute Research" style "menu_text_style" xalign 0.5

                        # Column headers
                        hbox:
                            xfill True
                            spacing 0
                            frame:
                                xsize 200
                                background "#00003088"
                                text "Name" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xsize 280
                                background "#00003088"
                                text "Description" style "menu_text_style" size 13 xalign 0.0
                            frame:
                                xsize 280
                                background "#00003088"
                                text "Research Cost" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xsize 100
                                background "#00003088"
                                text "Power" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xsize 100
                                background "#00003088"
                                text "Arousal" style "menu_text_style" size 13 xalign 0.5
                            frame:
                                xfill True
                                background "#00003088"
                                text "Assign" style "menu_text_style" size 13 xalign 0.5

                        $ _visible_attrs = sorted(
                            [attr for attr in getattr(mc.business, 'toy_attributes', []) if attr.is_unlockable and not attr.researched],
                            key=lambda attr: attr.name
                        )
                        vbox:
                            spacing 5
                            for attr in _visible_attrs:
                                frame:
                                    background "#1a1a2e88"
                                    xfill True
                                    xpadding 0
                                    ypadding 3
                                    hbox:
                                            xfill True
                                            spacing 0
                                            yalign 0.5
                                            # Name column
                                            frame:
                                                xsize 200
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[attr.name]" style "menu_text_style" size 14 yalign 0.5
                                            # Description column
                                            frame:
                                                xsize 280
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[attr.desc]" style "menu_text_style" size 13 yalign 0.5
                                            # Research Cost column
                                            frame:
                                                xsize 280
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                vbox:
                                                    spacing 2
                                                    yalign 0.5
                                                    if attr.researched:
                                                        text "{color=#24ed27}Researched{/color}" style "menu_text_style" size 13
                                                    elif attr.current_research > 0:
                                                        text "[attr.research_needed] pts ([int(attr.research_percentage * 100)]%)" style "menu_text_style" size 13
                                                    else:
                                                        text "[attr.research_needed] pts" style "menu_text_style" size 13
                                                    if getattr(attr, 'lubricant_trait_add', 0) > 0 or getattr(attr, 'lubricant_duration_add', 0) > 0:
                                                        text "Effect: +[attr.lubricant_trait_add] lubricant trait slot, +[attr.lubricant_duration_add] turn" style "menu_text_style" size 11
                                                    else:
                                                        text "Effect: +[attr.production_cost_add] cost, +$[attr.value_add] value" style "menu_text_style" size 11
                                            # Power column
                                            frame:
                                                xsize 100
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                $ _attr_pwr = getattr(attr, 'power_add', -1)
                                                if _attr_pwr >= 0:
                                                    text "{color=#24ed27}+[_attr_pwr]{/color}" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                                else:
                                                    text "{color=#ff4444}[_attr_pwr]{/color}" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                            # Arousal column
                                            frame:
                                                xsize 100
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                $ _attr_arousal = getattr(attr, 'arousal_rating_add', 0)
                                                if _attr_arousal > 0:
                                                    text "{color=#24ed27}+[_attr_arousal]{/color}" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                                elif _attr_arousal < 0:
                                                    text "{color=#ff4444}[_attr_arousal]{/color}" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                                else:
                                                    text "0" style "menu_text_style" size 13 xalign 0.5 yalign 0.5
                                            # Assign Research button column
                                            frame:
                                                xfill True
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                if not attr.researched and attr.is_unlockable:
                                                    textbutton "Assign Research":
                                                        style "textbutton_style"
                                                        xalign 1.0
                                                        yalign 0.5
                                                        selected (getattr(mc.business, 'active_attribute_research', None) == attr)
                                                        action Function(assign_attribute_research, attr)

                # Completed Research and component assignment section
                frame:
                    background "#0a142688"
                    xfill True
                    xpadding 10
                    ypadding 10
                    vbox:
                        spacing 10

                        frame:
                            background "#000080"
                            xfill True
                            text "Completed Research" style "menu_text_style" xalign 0.5

                        # Completed Blueprints table
                        $ _completed_bps = [bp for bp in mc.business.toy_blueprints if bp.researched]
                        if _completed_bps:
                            vbox:
                                spacing 0
                                frame:
                                    background "#001a4488"
                                    xfill True
                                    xpadding 6
                                    ypadding 4
                                    text "Completed Blueprints" style "menu_text_style" size 14 xalign 0.5
                                hbox:
                                    xfill True
                                    spacing 0
                                    frame:
                                        xsize 200
                                        background "#00003088"
                                        text "Name" style "menu_text_style" size 13 xalign 0.5
                                    frame:
                                        xsize 660
                                        background "#00003088"
                                        text "Description" style "menu_text_style" size 13 xalign 0.0
                                    frame:
                                        xsize 100
                                        background "#00003088"
                                        text "Mod. Space" style "menu_text_style" size 13 xalign 0.5
                                    frame:
                                        xsize 100
                                        background "#00003088"
                                        text "Power" style "menu_text_style" size 13 xalign 0.5
                                    frame:
                                        xsize 100
                                        background "#00003088"
                                        text "Arousal" style "menu_text_style" size 13 xalign 0.5
                                vbox:
                                    spacing 5
                                    for bp in _completed_bps:
                                        hbox:
                                            xfill True
                                            spacing 0
                                            frame:
                                                xsize 200
                                                text "[bp.name]" style "menu_text_style" size 13
                                            frame:
                                                xsize 660
                                                text "[bp.desc]" style "menu_text_style" size 13
                                            frame:
                                                xsize 100
                                                $ _bp_mod_space = getattr(bp, 'module_space', 0)
                                                text "[_bp_mod_space]" style "menu_text_style" size 13 xalign 0.5
                                            frame:
                                                xsize 100
                                                $ _bp_pwr = getattr(bp, 'power', -1)
                                                text "[_bp_pwr]" style "menu_text_style" size 13 xalign 0.5
                                            frame:
                                                xsize 100
                                                $ _bp_arousal = getattr(bp, 'arousal_rating', 0)
                                                if _bp_arousal > 0:
                                                    text "{color=#24ed27}+[_bp_arousal]{/color}" style "menu_text_style" size 13 xalign 0.5
                                                elif _bp_arousal < 0:
                                                    text "{color=#ff4444}[_bp_arousal]{/color}" style "menu_text_style" size 13 xalign 0.5
                                                else:
                                                    text "0" style "menu_text_style" size 13 xalign 0.5

                        # Completed Components table
                        $ _completed_attrs = [a for a in getattr(mc.business, 'toy_attributes', []) if a.researched]
                        if _completed_attrs:
                            vbox:
                                spacing 0
                                frame:
                                    background "#001a4488"
                                    xfill True
                                    xpadding 6
                                    ypadding 4
                                    text "Completed Components" style "menu_text_style" size 14 xalign 0.5
                                hbox:
                                    xfill True
                                    spacing 0
                                    frame:
                                        xsize 200
                                        background "#00003088"
                                        text "Name" style "menu_text_style" size 13 xalign 0.5
                                    frame:
                                        xsize 760
                                        background "#00003088"
                                        text "Description" style "menu_text_style" size 13 xalign 0.0
                                    frame:
                                        xsize 100
                                        background "#00003088"
                                        text "Power" style "menu_text_style" size 13 xalign 0.5
                                    frame:
                                        xsize 100
                                        background "#00003088"
                                        text "Arousal" style "menu_text_style" size 13 xalign 0.5
                                vbox:
                                    spacing 5
                                    for attr in _completed_attrs:
                                        hbox:
                                            xfill True
                                            spacing 0
                                            frame:
                                                xsize 200
                                                text "[attr.name]" style "menu_text_style" size 13
                                            frame:
                                                xsize 760
                                                text "[attr.desc]" style "menu_text_style" size 13
                                            frame:
                                                xsize 100
                                                text "[attr.power_add]" style "menu_text_style" size 13 xalign 0.5
                                            frame:
                                                xsize 100
                                                $ _attr_arousal = getattr(attr, 'arousal_rating_add', 0)
                                                if _attr_arousal > 0:
                                                    text "{color=#24ed27}+[_attr_arousal]{/color}" style "menu_text_style" size 13 xalign 0.5
                                                elif _attr_arousal < 0:
                                                    text "{color=#ff4444}[_attr_arousal]{/color}" style "menu_text_style" size 13 xalign 0.5
                                                else:
                                                    text "0" style "menu_text_style" size 13 xalign 0.5

                        if not _completed_bps and not _completed_attrs:
                            text "No research completed yet." style "menu_text_style"

        textbutton "Return":
            xalign 0.5
            action Return()

screen engineering_design_new_toy_ui():
    add paper_background_image
    modal True

    default sel_bp = None
    default sel_bat = None
    default sel_comps = []
    default sel_lubricant_traits = []

    $ _bps = [bp for bp in getattr(mc.business, 'toy_blueprints', []) if bp.researched]
    $ _bats = [a for a in getattr(mc.business, 'toy_attributes', []) if a.researched and getattr(a, 'design_component', True) and getattr(a, 'power_add', 0) > 0]
    $ _comps = [a for a in getattr(mc.business, 'toy_attributes', []) if a.researched and getattr(a, 'design_component', True) and getattr(a, 'power_add', 0) <= 0]
    $ _lube_traits = sorted(
        [
            t for t in list_of_traits + getattr(mc.business, 'blueprinted_traits', [])
            if getattr(t, 'researched', False)
            and not getattr(t, 'is_side_effect', False)
            and "Production" not in getattr(t, 'exclude_tags', [])
            and getattr(t, 'name', '') != "Antidote"
        ],
        key=lambda t: (-t.tier, t.name)
    )
    $ _lube_capacity = mc.business.lubricant_trait_capacity
    $ _lube_duration = mc.business.lubricant_duration

    $ _INTERNET_COMP_NAME = "Internet Connection, with Bluetooth"
    $ _BLUETOOTH_COMP_NAME = "Bluetooth Module"

    $ _bp_pwr = getattr(sel_bp, 'power', 0) if sel_bp else 0
    $ _bat_pwr = getattr(sel_bat, 'power_add', 0) if sel_bat else 0
    $ _comp_pwr = sum(getattr(c, 'power_add', 0) for c in sel_comps)
    $ _remaining = _bp_pwr + _bat_pwr + _comp_pwr
    $ _can_confirm = sel_bp is not None and sel_bat is not None and _remaining >= 0
    $ _module_space = getattr(sel_bp, 'module_space', 2) if sel_bp else 0
    $ _comp_slots = _module_space + sum(getattr(c, 'module_space_add', 0) for c in sel_comps)
    $ _comp_slots_used = len(sel_comps)

    vbox:
        xalign 0.5
        yalign 0.02
        xsize 1200
        spacing 8

        frame:
            background "#000080"
            xfill True
            text "Design New Toy" style "menu_text_title_style" xalign 0.5

        viewport:
            xfill True
            ysize 830
            draggable True
            mousewheel True
            scrollbars "vertical"
            vbox:
                spacing 8
                xfill True

                # 1. Blueprint selection
                frame:
                    background "#0a142688"
                    xfill True
                    xpadding 10
                    ypadding 10
                    vbox:
                        spacing 6
                        frame:
                            background "#000080"
                            xfill True
                            text "1. Choose Blueprint" style "menu_text_style" xalign 0.5
                        if _bps:
                            vbox:
                                spacing 4
                                for bp in _bps:
                                    hbox:
                                        xfill True
                                        spacing 8
                                        yalign 0.5
                                        textbutton "[bp.name]  {size=12}(draw: [bp.power] | [bp.module_space] slots | arousal: [bp.arousal_rating] | max intensity: [bp.max_intensity]){/size}":
                                            style "textbutton_style"
                                            xsize 600
                                            action SetScreenVariable("sel_bp", bp)
                                            selected (sel_bp == bp)
                                        text "[bp.desc]" style "menu_text_style" size 12 yalign 0.5
                        else:
                            text "No blueprints researched yet — research a blueprint first." style "menu_text_style"

                # 2. Battery selection
                frame:
                    background "#0a142688"
                    xfill True
                    xpadding 10
                    ypadding 10
                    vbox:
                        spacing 6
                        frame:
                            background "#000080"
                            xfill True
                            text "2. Choose Battery" style "menu_text_style" xalign 0.5
                        if _bats:
                            vbox:
                                spacing 4
                                for bat in _bats:
                                    hbox:
                                        xfill True
                                        spacing 8
                                        yalign 0.5
                                        textbutton "[bat.name]  {size=12}(+[bat.power_add] power){/size}":
                                            style "textbutton_style"
                                            xsize 600
                                            action SetScreenVariable("sel_bat", bat)
                                            selected (sel_bat == bat)
                                        text "[bat.desc]" style "menu_text_style" size 12 yalign 0.5
                        else:
                            text "No batteries researched yet — research a battery component first." style "menu_text_style"

                # Power budget indicator
                if sel_bp and sel_bat:
                    frame:
                        background "#0a142688"
                        xfill True
                        xpadding 10
                        ypadding 6
                        vbox:
                            spacing 4
                            if _remaining >= 0:
                                text "Power: +[_bat_pwr] (battery) [_bp_pwr] (blueprint) [_comp_pwr] (components) = {color=#24ed27}[_remaining] remaining{/color}" style "menu_text_style" xalign 0.5
                            else:
                                text "Power: +[_bat_pwr] (battery) [_bp_pwr] (blueprint) [_comp_pwr] (components) = {color=#ff4444}[_remaining] overloaded!{/color}" style "menu_text_style" xalign 0.5
                            text "Module slots: [_comp_slots_used]/[_comp_slots] component slots used" style "menu_text_style" xalign 0.5 size 14

                # 3. Component selection
                frame:
                    background "#0a142688"
                    xfill True
                    xpadding 10
                    ypadding 10
                    vbox:
                        spacing 6
                        frame:
                            background "#000080"
                            xfill True
                            text "3. Add Components (optional — within power budget and module slots)" style "menu_text_style" xalign 0.5
                        if sel_bp and sel_bat:
                            if _comps:
                                $ _internet_selected = any(getattr(c, 'name', '') == _INTERNET_COMP_NAME for c in sel_comps)
                                vbox:
                                    spacing 4
                                    for comp in _comps:
                                        $ _in = comp in sel_comps
                                        $ _after = _remaining + (0 if _in else getattr(comp, 'power_add', 0))
                                        $ _after_slots = _comp_slots + (0 if _in else getattr(comp, 'module_space_add', 0))
                                        $ _after_slots_used = _comp_slots_used + (0 if _in else 1)
                                        $ _blocked_by_internet = _internet_selected and getattr(comp, 'name', '') == _BLUETOOTH_COMP_NAME
                                        hbox:
                                            xfill True
                                            spacing 8
                                            yalign 0.5
                                            textbutton "[comp.name]  {size=12}([comp.power_add] pwr | +$[comp.value_add] | arousal: [comp.arousal_rating_add]){/size}":
                                                style "textbutton_style"
                                                xsize 600
                                                sensitive (not _blocked_by_internet and (_in or (_after >= 0 and _after_slots_used <= _after_slots)))
                                                action If(comp in sel_comps,
                                                    true=SetScreenVariable("sel_comps", [c for c in sel_comps if c != comp]),
                                                    false=If(getattr(comp, 'name', '') == _INTERNET_COMP_NAME,
                                                        true=SetScreenVariable("sel_comps", [c for c in sel_comps if getattr(c, 'name', '') != _BLUETOOTH_COMP_NAME] + [comp]),
                                                        false=SetScreenVariable("sel_comps", sel_comps + [comp])))
                                                selected _in
                                            if _blocked_by_internet:
                                                text "{i}Included in Internet Connection{/i}" style "menu_text_style" size 12 yalign 0.5
                                            else:
                                                text "[comp.desc]" style "menu_text_style" size 12 yalign 0.5
                            else:
                                text "No components researched yet." style "menu_text_style"
                        else:
                            text "Select a blueprint and battery first." style "menu_text_style" size 14

                # 4. Lubricant selection
                frame:
                    background "#0a142688"
                    xfill True
                    xpadding 10
                    ypadding 10
                    vbox:
                        spacing 6
                        frame:
                            background "#000080"
                            xfill True
                            text "4. Choose Additional Lubricant Traits (optional)" style "menu_text_style" xalign 0.5
                        if _lube_capacity <= 0:
                            text "Antidote is included automatically and does not use space. Research Lubricant Infusion to add extra lubricant traits for toy designs." style "menu_text_style"
                        elif _lube_traits:
                            text "Mandatory: Antidote | Extra selected: [len(sel_lubricant_traits)]/[_lube_capacity] trait(s) | Duration: [_lube_duration] turn(s)" style "menu_text_style" xalign 0.5 size 14
                            vbox:
                                spacing 4
                                for trait in _lube_traits:
                                    $ _has_trait = trait in sel_lubricant_traits
                                    $ _allowed = _has_trait or lubricant_trait_allowed(sel_lubricant_traits, trait)
                                    hbox:
                                        xfill True
                                        spacing 8
                                        yalign 0.5
                                        textbutton "[trait.name]  {size=12}(Tier [trait.tier]){/size}":
                                            style "textbutton_style"
                                            xsize 600
                                            sensitive (_has_trait or (_allowed and len(sel_lubricant_traits) < _lube_capacity))
                                            action If(_has_trait,
                                                true=SetScreenVariable("sel_lubricant_traits", [t for t in sel_lubricant_traits if t != trait]),
                                                false=SetScreenVariable("sel_lubricant_traits", sel_lubricant_traits + [trait]))
                                            selected _has_trait
                                        if not _allowed:
                                            text "{i}Conflicts with a selected trait{/i}" style "menu_text_style" size 12 yalign 0.5
                                        else:
                                            text "[trait.positive_slug if trait.positive_slug else trait.desc]" style "menu_text_style" size 12 yalign 0.5
                        else:
                            text "No researched serum traits available yet." style "menu_text_style"

                # Completed Designs section
                frame:
                    background "#0a142688"
                    xfill True
                    xpadding 10
                    ypadding 10
                    vbox:
                        spacing 6

                        frame:
                            background "#000080"
                            xfill True
                            text "Completed Designs" style "menu_text_style" xalign 0.5

                        if mc.business.toy_designs:
                            vbox:
                                spacing 4
                                for design in mc.business.toy_designs:
                                    vbox:
                                        spacing 2
                                        $ _d_attrs = getattr(design, 'attributes', [])
                                        $ _d_lube_traits = getattr(design, 'lubricant_traits', [])
                                        $ _d_lube_duration = getattr(design, 'lubricant_duration', 0)
                                        $ _d_arousal = design.total_arousal_rating
                                        $ _d_slut_req = _d_arousal * 5
                                        $ _d_is_plug = "plug" in getattr(design.blueprint, 'name', '').lower()
                                        $ _d_pref_label = "Anal comfort" if _d_is_plug else "Vaginal comfort"
                                        hbox:
                                            spacing 10
                                            yalign 0.5
                                            text "[design.name]  {size=13}(Mfg Cost: [design.production_cost] pts | Sell Value: $[design.base_value] | Components: [len(_d_attrs)] | Arousal: [_d_arousal]){/size}" style "menu_text_style" yalign 0.5
                                            $ _can_upg = can_upgrade_design(design, sel_bp, sel_bat, sel_comps, sel_lubricant_traits)
                                            textbutton ("{color=#66aaff}Upgrade{/color}" if _can_upg else "{color=#888888}Upgrade{/color}"):
                                                style "textbutton_style"
                                                text_size 13
                                                sensitive _can_upg
                                                action Call("toy_upgrade_confirm_label", design, sel_bat, sel_comps, sel_lubricant_traits)
                                                tooltip "Upgrade this design to the battery, components, and lubricant traits selected above"
                                            textbutton "{color=#ff6666}Remove{/color}":
                                                style "textbutton_style"
                                                text_size 13
                                                action Function(remove_toy_design, design)
                                                tooltip "Permanently remove this design"
                                        if _d_attrs:
                                            hbox:
                                                spacing 4
                                                xoffset 16
                                                text "{size=12}{color=#aaaaaa}Components:{/color}{/size}" style "menu_text_style"
                                                for _attr in _d_attrs:
                                                    text "{size=12}{color=#cccccc}[_attr.name]{/color}{/size}" style "menu_text_style"
                                        if _d_lube_traits:
                                            hbox:
                                                spacing 4
                                                xoffset 16
                                                text "{size=12}{color=#aaaaaa}Lubricant ([_d_lube_duration] turn(s)):{/color}{/size}" style "menu_text_style"
                                                for _trait in _d_lube_traits:
                                                    text "{size=12}{color=#cccccc}[_trait.name]{/color}{/size}" style "menu_text_style"
                                        # Requirements row (generic — not tied to any specific person)
                                        hbox:
                                            spacing 12
                                            xoffset 16
                                            text "{size=12}{color=#aaddff}Slut level required: [_d_slut_req]{/color}{/size}" style "menu_text_style"
                                            text "{size=12}{color=#aaddff}[_d_pref_label] required: >[_d_arousal] (less with higher obedience){/color}{/size}" style "menu_text_style"
                        else:
                            text "No completed toy designs yet. Design one using blueprint and battery above." style "menu_text_style"

        hbox:
            xalign 0.5
            spacing 20
            frame:
                background "#4a7fc1cc"
                padding (4, 4)
                textbutton "Create Design":
                    style "textbutton_style"
                    sensitive _can_confirm
                    action Return((sel_bp, sel_bat, list(sel_comps), list(sel_lubricant_traits)))
            frame:
                background "#7f2020cc"
                padding (4, 4)
                textbutton "Cancel":
                    style "textbutton_style"
                    action Return(None)


## Popup shown at end-of-day when a blueprint or attribute research is completed.
screen research_complete_popup(name, desc):
    modal True
    zorder 200

    frame:
        background "#0a1426ee"
        xalign 0.5
        yalign 0.5
        xsize 700
        padding (30, 30)

        vbox:
            spacing 20
            xfill True

            frame:
                background "#000080"
                xfill True
                padding (10, 8)
                text "Research Complete!" style "menu_text_title_style" xalign 0.5

            text "[name]" style "textbutton_text_style" size 26 xalign 0.5

            frame:
                background "#0a142688"
                xfill True
                padding (14, 12)
                text "[desc]" style "textbutton_text_style" size 20 xalign 0.0

            textbutton "OK":
                style "textbutton_style"
                xalign 0.5
                action Return()
