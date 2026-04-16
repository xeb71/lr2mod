#This role is a replacement for Starbuck's Sex Shop Owner inherited class file.
#All functions associated with running the sex shop can now be done via Roles, so lets simplify the code and do it that way.

# Sale price multiplier for toys placed "on special" (20% discount).
# Defined here so it is available in the Ren'Py store for use by screens.
# The matching module-level value in starbuck_role_definition_ren.py lets
# Python (_ren.py) functions access it via the module dict.
default SPECIAL_DISCOUNT = 0.8

# Multiplier converting total_arousal_rating into minimum NPC sluttiness.
# Matching value in starbuck_role_definition_ren.py.
define AROUSAL_TO_SLUT_MULTIPLIER = 5

label sex_shop_invest_basic_label(the_person):
    mc.name "I'd like to invest more in your shop, [the_person.title]."
    the_person "Oh?"
    mc.name "I'd like for you to expand more of your basic inventory."
    the_person "Those do tend to be high margin, profitable items. I supposed I could look around and see if I can expand my inventory some."
    mc.name "Sounds great. Here's a check for $1000."
    $ the_person.change_stats(obedience = 2, love = 1, max_love = 30)
    $ mc.business.change_funds(-1000, stat = "Investments")
    $ the_person.event_triggers_dict["shop_investment_basic_total"] += 1000
    $ the_person.event_triggers_dict["shop_investment_total"] += 1000
    the_person "Wow! I really appreciate this. Is there anything else you need [the_person.mc_title]?"
    the_person "Maybe you could swing by sometime in the evening and help me put up stock?"
    return

label sex_shop_invest_advanced_label(the_person):
    mc.name "I'd like to invest more in your shop, [the_person.title]."
    the_person "Oh?"
    mc.name "I'd like for you to expand more of your advanced inventory."
    the_person "Yeah, having intricate toys and the like can be great for driving foot traffic, even if they don't sell very fast."
    mc.name "Sounds great. Here's a check for $5000."
    $ the_person.change_stats(obedience = 3, love = 2, max_love = 50)
    $ mc.business.change_funds(-5000, stat = "Investments")
    $ the_person.event_triggers_dict["shop_investment_advanced_total"] += 5000
    $ the_person.event_triggers_dict["shop_investment_total"] += 5000
    the_person "Wow! I can't believe you are investing even more! This is really incredible. Is there anything else you need while you're here, [the_person.mc_title]?"
    return

label sex_shop_invest_fetish_label(the_person):
    mc.name "I'd like to invest more in your shop, [the_person.title]."
    the_person "Oh? You've already done so much."
    mc.name "I'd like for you to expand more of your fetish inventory."
    the_person "Fetish inventory moves slowly, but it definitely drives interest and foot traffic."
    mc.name "Sounds great. Here's a check for $15000."
    $ the_person.change_stats(obedience = 5, love = 3, max_love = 70)
    $ mc.business.change_funds(-15000, stat = "Investments")
    $ the_person.event_triggers_dict["shop_investment_fetish_total"] += 15000
    $ the_person.event_triggers_dict["shop_investment_total"] += 15000
    the_person "Holy fuck! You're amazing [the_person.mc_title]! Anything else you need while you are here?"
    return

label sex_shop_cashier_wardrobe_label(the_person):
    mc.name "I'd like to talk to you about your uniforms."
    the_person "Oh?"
    call outfit_master_manager(wardrobe = sex_shop_wardrobe.wardrobe, show_overwear = False, show_underwear = False, start_mannequin = the_person, outfit_validator = sex_shop_owner_outfit_check) from _call_outfit_master_manager_sex_shop_cashier_wardrobe
    return

label sex_shop_discuss_selling_label(the_person):
    mc.name "Hey [the_person.title], I wanted to run something by you."
    the_person "Of course, [the_person.mc_title]. What's on your mind?"
    mc.name "You know how we've been investing in your basic inventory? Well, I've been thinking about going further — actually manufacturing the toys myself and having you sell them through the shop."
    the_person "Oh wow... that's a big step. You mean like, your company would produce the toys and I'd handle retail?"
    mc.name "Exactly. You've got the customer base and the storefront. I'd handle design and production."
    the_person "That could actually work really well. I do get customers asking for specific things I can't always source..."
    menu:
        "Tell me more about what you'd need.":
            mc.name "What would we need to make that happen on your end?"
            the_person "From my side, not much — I just need reliable stock. But you'd need a dedicated space to actually make the things. A proper workshop or something."
            mc.name "Like an engineering division."
            the_person "Exactly. If you had the space and equipment set up, I'd be happy to carry your products. I think it could be a real moneymaker for both of us."
            mc.name "Alright. Let me look into getting that space set up at the office. I'll come back to you once things are in place."
            the_person "I'd love that! Come find me whenever you're ready, [the_person.mc_title]."
            $ mc.business.event_triggers_dict["engineering_division_policy_avail"] = True
        "Actually, I'm not ready for that commitment yet.":
            mc.name "Actually, I'm still thinking it through. I'll come back to you once I've worked out the details."
            the_person "No rush, [the_person.mc_title]. The offer stands whenever you're ready."
    return

label sex_shop_check_stock_label():
    python:
        renpy.call_screen("sex_shop_stock_screen")
    return

screen sex_shop_stock_screen():
    modal True
    add paper_background_image
    zorder 100

    python:
        _toy_inv = getattr(mc.business, 'toy_inventory', {})
        _sales_log = getattr(mc.business, 'toy_sales_log', {})
        _active_design_names = [d.name for d in getattr(mc.business, 'toy_designs', [])]
        _active_set = set(_active_design_names)
        _all_historic = set(list(_toy_inv.keys()) + list(_sales_log.keys()))
        # Active designs first (sorted), then retired/removed ones last (sorted).
        _all_names = sorted(_active_set) + sorted(_all_historic - _active_set)
        _specials = getattr(mc.business, 'toy_specials', set())

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        background "#1a45a1aa"
        padding (15, 15)
        vbox:
            spacing 10
            text "Sex Shop Stock" style "serum_text_style_header" xalign 0.5
            text "Buy chance per visitor: [int(get_buy_chance() * 100)]%" style "menu_text_style" xalign 0.5
            if not _all_names:
                text "No stock data available yet." style "menu_text_style" xalign 0.5
            else:
                frame:
                    background "#0a142688"
                    xfill True
                    padding (8, 6)
                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        draggable True
                        ysize 420
                        xfill True
                        vbox:
                            spacing 0
                            xfill True
                            # Header row — inside the viewport so it aligns with data columns
                            hbox:
                                xfill True
                                spacing 0
                                frame:
                                    xsize 190
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Design" style "menu_text_style" size 13 xalign 0.0
                                frame:
                                    xsize 80
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "In Stock" style "menu_text_style" size 13 xalign 0.5
                                frame:
                                    xsize 80
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Sold" style "menu_text_style" size 13 xalign 0.5
                                frame:
                                    xsize 90
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Profit" style "menu_text_style" size 13 xalign 1.0
                                frame:
                                    xsize 80
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Price" style "menu_text_style" size 13 xalign 0.5
                                frame:
                                    xsize 90
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Min {image=gui/heart/gold_heart.png}" style "menu_text_style" size 13 xalign 0.5
                                frame:
                                    xfill True
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Special" style "menu_text_style" size 13 xalign 0.5
                            # Data rows
                            vbox:
                                spacing 4
                                xfill True
                                for _name in _all_names:
                                    $ _stock = _toy_inv.get(_name, 0)
                                    $ _entry = _sales_log.get(_name, [0, 0])
                                    $ _sold = _entry[0]
                                    $ _profit = _entry[1]
                                    $ _is_special = _name in _specials
                                    $ _design_obj = next((d for d in getattr(mc.business, 'toy_designs', []) if d.name == _name), None)
                                    $ _base_price = _design_obj.base_value if _design_obj else 0
                                    $ _special_price = int(_base_price * SPECIAL_DISCOUNT)
                                    $ _min_slut = (getattr(_design_obj, 'total_arousal_rating', 0) * AROUSAL_TO_SLUT_MULTIPLIER) if _design_obj else 0
                                    $ _special_min_slut = int(_min_slut * SPECIAL_DISCOUNT)
                                    frame:
                                        background ("#1a5a1a88" if _is_special else "#0a142655")
                                        xfill True
                                        padding (0, 2)
                                        hbox:
                                            xfill True
                                            spacing 0
                                            yalign 0.5
                                            frame:
                                                xsize 190
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[_name]" style "menu_text_style" xalign 0.0
                                            frame:
                                                xsize 80
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[_stock]" style "menu_text_style" xalign 0.5
                                            frame:
                                                xsize 80
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[_sold]" style "menu_text_style" xalign 0.5
                                            frame:
                                                xsize 90
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "$[_profit]" style "menu_text_style" xalign 1.0
                                            frame:
                                                xsize 80
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                if _is_special and _base_price > 0:
                                                    text "{color=#44ff44}$[_special_price]{/color}" style "menu_text_style" xalign 0.5
                                                elif _base_price > 0:
                                                    text "$[_base_price]" style "menu_text_style" xalign 0.5
                                                else:
                                                    text "{color=#888888}—{/color}" style "menu_text_style" xalign 0.5
                                            frame:
                                                xsize 90
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                if _design_obj is not None:
                                                    if _is_special and _min_slut > 0:
                                                        text "{color=#44ff44}[_special_min_slut]{/color} {image=gui/heart/gold_heart.png}" style "menu_text_style" xalign 0.5
                                                    else:
                                                        text "[_min_slut] {image=gui/heart/gold_heart.png}" style "menu_text_style" xalign 0.5
                                                else:
                                                    text "{color=#888888}—{/color}" style "menu_text_style" xalign 0.5
                                            frame:
                                                xfill True
                                                xpadding 4
                                                ypadding 2
                                                background None
                                                hbox:
                                                    xalign 0.5
                                                    yalign 0.5
                                                    if _design_obj is not None:
                                                        if _is_special:
                                                            frame:
                                                                background "#2a7f2acc"
                                                                padding (2, 2)
                                                                textbutton "★ Cancel" style "sex_shop_button_style" text_style "sex_shop_button_text_style" action Function(toggle_toy_special, _name) tooltip "Remove special discount"
                                                        else:
                                                            frame:
                                                                background "#4a7fc1cc"
                                                                padding (2, 2)
                                                                textbutton "On Special" style "sex_shop_button_style" text_style "sex_shop_button_text_style" action Function(toggle_toy_special, _name) tooltip "Sell at 20% discount"
                                                    else:
                                                        text "{color=#888888}{size=12}(retired){/size}{/color}" style "menu_text_style" xalign 0.5
            null height 5
            hbox:
                xalign 0.5
                spacing 20
                frame:
                    background "#4a7fc1cc"
                    padding (2, 2)
                    textbutton "Client List" style "sex_shop_button_style" text_style "sex_shop_button_text_style" action [Hide("sex_shop_stock_screen"), Show("sex_shop_client_list_screen")]
                frame:
                    background "#4a7fc1cc"
                    padding (2, 2)
                    textbutton "Close" style "sex_shop_button_style" text_style "sex_shop_button_text_style" action Return()

screen sex_shop_client_list_screen():
    modal True
    add paper_background_image
    zorder 100

    python:
        _client_log = getattr(mc.business, 'toy_client_log', [])
        # Deduplicate: keep only the latest entry per NPC identifier.
        _seen_ids = set()
        _unique_log = []
        for _e in reversed(_client_log):
            _eid = _e[3] if len(_e) > 3 else None
            if _eid is not None and _eid in _seen_ids:
                continue
            if _eid is not None:
                _seen_ids.add(_eid)
            _unique_log.append(_e)

    frame:
        xalign 0.5
        yalign 0.5
        xsize 800
        background "#1a45a1aa"
        padding (15, 15)
        vbox:
            spacing 10
            text "Client List (Warranty)" style "serum_text_style_header" xalign 0.5
            if not _client_log:
                text "No named clients have purchased toys yet." style "menu_text_style" xalign 0.5
            else:
                frame:
                    background "#0a142688"
                    xfill True
                    padding (8, 6)
                    viewport:
                        mousewheel True
                        scrollbars "vertical"
                        draggable True
                        ysize 420
                        xfill True
                        vbox:
                            spacing 0
                            xfill True
                            # Header row
                            hbox:
                                xfill True
                                spacing 0
                                frame:
                                    xsize 180
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Client" style "menu_text_style" size 13 xalign 0.0
                                frame:
                                    xsize 200
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Toy" style "menu_text_style" size 13 xalign 0.0
                                frame:
                                    xsize 120
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Date (Day)" style "menu_text_style" size 13 xalign 0.5
                                frame:
                                    xfill True
                                    background "#00003088"
                                    xpadding 8
                                    ypadding 6
                                    text "Action" style "menu_text_style" size 13 xalign 0.5
                            # Data rows (most recent purchases first, one row per NPC)
                            vbox:
                                spacing 4
                                xfill True
                                for _entry in _unique_log:
                                    $ _c_name = _entry[0]
                                    $ _c_toy = _entry[1]
                                    $ _c_day = _entry[2]
                                    $ _c_id = _entry[3] if len(_entry) > 3 else None
                                    $ _c_person = Person.get_person_by_identifier(_c_id) if _c_id is not None else None
                                    $ _c_display = _c_person.fname if _c_person is not None and not _c_person.is_stranger else _c_name
                                    $ _c_voucher_used = _c_person is not None and getattr(_c_person, 'voucher_was_used', False)
                                    frame:
                                        background "#0a142655"
                                        xfill True
                                        padding (0, 2)
                                        hbox:
                                            xfill True
                                            spacing 0
                                            yalign 0.5
                                            frame:
                                                xsize 180
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[_c_display]" style "menu_text_style" xalign 0.0
                                            frame:
                                                xsize 200
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "[_c_toy]" style "menu_text_style" xalign 0.0
                                            frame:
                                                xsize 120
                                                xpadding 8
                                                ypadding 4
                                                background None
                                                text "Day [_c_day]" style "menu_text_style" xalign 0.5
                                            frame:
                                                xfill True
                                                xpadding 4
                                                ypadding 2
                                                background None
                                                if _c_voucher_used:
                                                    vbox:
                                                        xalign 0.5
                                                        text "Voucher ✓" style "menu_text_style" size 12 xalign 0.5 color "#ffff00"
                                                        text "[_c_toy]" style "menu_text_style" size 11 xalign 0.5 color "#ffffff"
                                                elif _c_person is not None and not getattr(_c_person, 'has_toy_voucher', False):
                                                    textbutton "Survey" style "sex_shop_button_style" text_style "sex_shop_button_text_style" text_size 12 xalign 0.5 action Function(renpy.call_in_new_context, "toy_survey_call_label", the_person=_c_person)
                                                elif _c_person is not None and getattr(_c_person, 'has_toy_voucher', False):
                                                    text "Voucher ✓" style "menu_text_style" size 12 xalign 0.5 color "#88ff88"
                                                else:
                                                    text "—" style "menu_text_style" size 12 xalign 0.5
            null height 5
            hbox:
                xalign 0.5
                spacing 20
                frame:
                    background "#4a7fc1cc"
                    padding (2, 2)
                    textbutton "Back to Stock" style "sex_shop_button_style" text_style "sex_shop_button_text_style" action [Hide("sex_shop_client_list_screen"), Show("sex_shop_stock_screen")]
                frame:
                    background "#4a7fc1cc"
                    padding (2, 2)
                    textbutton "Close" style "sex_shop_button_style" text_style "sex_shop_button_text_style" action [Hide("sex_shop_client_list_screen"), Return()]

label toy_survey_call_label(the_person):
    # Phone call survey: ask for feedback in exchange for a discount voucher
    mc.name "Let me give [the_person.name] a call about her recent purchase..."
    "You dial [the_person.name]'s number."
    the_person "Hello?"
    mc.name "Hi [the_person.name], this is [mc.name] from the sex shop. I was wondering if you'd be willing to do a quick feedback survey? We're offering a discount voucher in return."

    if getattr(the_person, 'toy_use_count', 0) >= 2 and getattr(the_person, 'toy_orgasm_count', 0) > 0:
        # Used 2+ times AND orgasmed — interested in voucher
        the_person "Oh, yes! I've been really enjoying my toy, it's been... {i}very{/i} satisfying."
        mc.name "That's wonderful to hear! So, what would you say is the best thing about it?"
        the_person "Honestly? It just hits all the right spots. I'd definitely recommend it."
        mc.name "Perfect! As a thank you for the feedback, here's a $5 discount voucher for your next purchase."
        the_person "Oh, that's so sweet! I might just have to come browse again soon..."
        $ the_person.has_toy_voucher = True
    elif getattr(the_person, 'toy_use_count', 0) < 3:
        # Used it less than 3 times — she declines
        the_person "Oh... I appreciate the call, but I haven't really had a chance to use it much yet. Maybe another time?"
        mc.name "No problem at all. Enjoy your purchase!"
        the_person "Thanks, bye!"
    else:
        # Used 3+ times but never orgasmed — liked it but not interested in voucher
        the_person "It's been nice, I do like it! But I'm not really looking for another one right now, so the voucher wouldn't help me."
        mc.name "That's great to hear you're enjoying it. Thanks for the feedback!"
        the_person "No problem. Bye!"
    return

label toy_replacement_call_label(the_person, the_toy):
    # The girl calls after switching off her toy 3 times due to over-stimulation
    "Your phone rings — it's [the_person.name]."
    the_person "Hi [mc.name], it's [the_person.name]. I've been having trouble with my [the_toy.name] — it keeps being too intense for me. Could I get a replacement?"

    python:
        _toy_name = the_toy.design.name
        _toy_inv = getattr(mc.business, 'toy_inventory', {})
        _has_replacement = _toy_inv.get(_toy_name, 0) > 0

        # Find upgrade candidates: same toy_type, higher arousal, in stock
        _toy_type = getattr(the_toy.design.blueprint, 'toy_type', 'vaginal')
        _current_arousal = getattr(the_toy.design, 'total_arousal_rating', 0)
        _designs = getattr(mc.business, 'toy_designs', [])
        _best_upgrade = None
        _best_arousal = _current_arousal
        for _d in _designs:
            if getattr(_d.blueprint, 'toy_type', 'vaginal') == _toy_type:
                _d_arousal = getattr(_d, 'total_arousal_rating', 0)
                if _d_arousal > _best_arousal:
                    if _toy_inv.get(_d.name, 0) > 0:
                        _best_upgrade = _d
                        _best_arousal = _d_arousal

    if not _has_replacement and _best_upgrade is None:
        mc.name "I'm sorry [the_person.name], we're out of stock right now. I'll see what I can do."
        the_person "Oh... okay. I hope you can sort something out soon."
        $ the_person.toy_switchoff_count = 0
        return

    menu:
        "Send her a replacement [_toy_name] (1 stock)" if _has_replacement:
            mc.name "No problem, [the_person.name]. I'll send you a replacement right away."
            the_person "Oh thank you! That's great service."
            python:
                _new_toy = mc.business.withdraw_toy(_toy_name)
                if _new_toy is not None:
                    the_person.take_toy(the_toy)
                    the_person.give_toy(_new_toy)
                    if "installed" in _new_toy.valid_usages:
                        the_person.install_toy(_new_toy)
                the_person.toy_switchoff_count = 0

        "Offer her a free upgrade to [_best_upgrade.name]" if _best_upgrade is not None:
            mc.name "Actually [the_person.name], I'd like to offer you a free upgrade to our [_best_upgrade.name]. It's a better model."
            the_person "Really? That's so generous! I'd love that, thank you!"
            python:
                _new_toy = mc.business.withdraw_toy(_best_upgrade.name)
                if _new_toy is not None:
                    the_person.take_toy(the_toy)
                    the_person.give_toy(_new_toy)
                    if "installed" in _new_toy.valid_usages:
                        the_person.install_toy(_new_toy)
                the_person.toy_switchoff_count = 0

        "Decline the request":
            mc.name "I'm sorry [the_person.name], we can't do replacements at this time."
            the_person "Oh... that's disappointing. Alright then."
            $ the_person.toy_switchoff_count = 0
    return
