screen floating_notifications():
    layer "hud"
    style_prefix "notify"
    zorder 400

    default _hovered = False

    frame:
        style_suffix "empty"
        background None
        padding (0, 0)
        xsize 400
        xanchor 1.0
        xpos 1.0
        ypos 0
        at Transform(alpha=(0.9 if _hovered else 0.5))

        fixed:
            fit_first True

            vbox:
                spacing 1

                hbox:
                    xfill True
                    textbutton ("Fade" if persistent.stat_change_fade else "Log"):
                        xalign 0.0
                        style "textbutton_no_padding"
                        text_style "textbutton_text_style"
                        text_size 14
                        action [ToggleField(persistent, "stat_change_fade", True, False), renpy.restart_interaction]
                        tooltip ("Switch to log mode: keep last 100 messages" if persistent.stat_change_fade else "Switch to fade mode: messages disappear automatically")

                if persistent.stat_change_fade:
                    for notification in active_notifications:
                        frame:
                            background "#00000055"
                            padding (2, 2)
                            text notification.text style notification.text_style size 18 xsize 390
                else:
                    $ _notifs = list(reversed(active_notifications))
                    viewport:
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        yinitial 0.0
                        ymaximum 180
                        vbox:
                            spacing 2
                            for notification in _notifs:
                                frame:
                                    background "#00000055"
                                    padding (2, 2)
                                    ypos 0
                                    text notification.text style notification.text_style size 18 xsize 378

            mousearea:
                hovered SetScreenVariable("_hovered", True)
                unhovered SetScreenVariable("_hovered", False)
