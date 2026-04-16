screen sex_toy_admin_app():
    modal True
    add paper_background_image
    zorder 100

    $ _entries = get_sex_toy_admin_entries()

    frame:
        xalign 0.5
        yalign 0.5
        xsize 680
        background "#1a45a1aa"
        padding (15, 15)
        vbox:
            spacing 10
            text "Sex Toy Admin" style "serum_text_style_header" xalign 0.5
            if not _entries:
                text "No connected devices found." style "menu_text_style" xalign 0.5
            else:
                viewport:
                    mousewheel True
                    scrollbars "vertical"
                    draggable True
                    ysize 480
                    vbox:
                        spacing 5
                        for _npc, _toy in _entries:
                            $ _adm_dname = _npc.fname if not _npc.is_stranger else _npc.name
                            $ _adm_switched_off = getattr(_toy, 'is_switched_off', False)
                            frame:
                                background "#0a142688"
                                xfill True
                                padding (10, 8)
                                vbox:
                                    spacing 4
                                    hbox:
                                        spacing 10
                                        if _adm_switched_off:
                                            text f"{_adm_dname} — {_toy.name} {{color=#ff6666}}(Switched Off){{/color}}" style "menu_text_style" xsize 490
                                        else:
                                            text f"{'★ ' if _toy.installed else ''}{_adm_dname} — {_toy.name}" style "menu_text_style" xsize 490
                                        if _toy.installed and _toy_has_diagnostics(_toy):
                                            textbutton "Girl View":
                                                style "textbutton_style"
                                                text_style "menu_text_style"
                                                yalign 0.5
                                                action Show("person_info_detailed", None, _npc)
                                    hbox:
                                        spacing 20
                                        text f"  Used: {getattr(_npc, 'toy_use_count', 0)}" style "menu_text_style" size 14
                                        text f"Orgasms: {getattr(_npc, 'toy_orgasm_count', 0)}" style "menu_text_style" size 14
                                        text f"Switched Off: {getattr(_npc, 'toy_switchoff_count', 0)}" style "menu_text_style" size 14
                                    if _toy_has_gps(_toy):
                                        $ _adm_gps_name = _npc.home_hub.formal_name if _npc.location is _npc.home else _npc.location.formal_name
                                        text f"  GPS Location: {_adm_gps_name}" style "menu_text_style" size 14
                                    if _toy_has_diagnostics(_toy) and _toy.installed and _npc.is_pregnant:
                                        text f"  Diagnostics: {{color=#ff88cc}}Pregnancy Detected{{/color}}" style "menu_text_style" size 14
                                    if _toy.installed:
                                        $ _adm_ti = getattr(_toy, 'intensity', 1)
                                        $ _adm_tmax = getattr(_toy, 'max_intensity', 3)
                                        $ _adm_slut = _npc.sluttiness
                                        $ _adm_warn = _adm_ti * 10 > _adm_slut
                                        hbox:
                                            spacing 6
                                            if _adm_warn:
                                                text f"  Intensity: {{color=#ff6666}}{_adm_ti}{{/color}}/{_adm_tmax}" style "menu_text_style" size 14 yalign 0.5
                                            else:
                                                text f"  Intensity: {_adm_ti}/{_adm_tmax}" style "menu_text_style" size 14 yalign 0.5
                                            if _adm_ti > 1:
                                                frame:
                                                    background "#2a3a5a"
                                                    padding (2, 1)
                                                    yalign 0.5
                                                    textbutton "-":
                                                        style "textbutton_style"
                                                        text_size 13
                                                        yalign 0.5
                                                        action [SetField(_toy, 'intensity', _adm_ti - 1), renpy.restart_interaction]
                                            if _adm_ti < _adm_tmax:
                                                frame:
                                                    background "#2a3a5a"
                                                    padding (2, 1)
                                                    yalign 0.5
                                                    textbutton "+":
                                                        style "textbutton_style"
                                                        text_size 13
                                                        yalign 0.5
                                                        action [SetField(_toy, 'intensity', _adm_ti + 1), renpy.restart_interaction]
            null height 5
            frame:
                background "#2a3a5a"
                padding (4, 2)
                xalign 0.5
                textbutton "Close" align (0.5, 0.5) style "return_button_style" action Return()
