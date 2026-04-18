screen queen_toggle_button(person):
    if person.can_be_queen:
        imagebutton:
            offset (10, 5)
            if person.is_queen:
                idle "gui/extra_images/queen_crown_filled.png"
                hover "gui/extra_images/queen_crown_remove.png"
            else:
                idle "gui/extra_images/queen_crown_empty.png"
                hover "gui/extra_images/queen_crown_add.png"
            action [person.toggle_queen, renpy.restart_interaction]
            tooltip "Toggle Queen\nMarks this harem girl as one of your queens. Only harem girls who love taking control can be queens.\nYou can also command another harem member to serve her as her servant."
