# IDE stubs for the Ren'Py store variables that control inter-event timing delays.
#
# The real values are Ren'Py `default` variables defined in script.rpy and updated
# at runtime by update_game_speed() whenever the player changes the game speed setting.
# These module-level stubs only exist so that IDEs can type-check code that references
# the store variables before the Ren'Py store has been fully initialized.
#
# Usage in _ren.py files: import these names to avoid redefining them locally.
#   from game.helper_functions.game_speed_constants_ren import TIER_1_TIME_DELAY, TIER_2_TIME_DELAY, TIER_3_TIME_DELAY
#
# Game-speed values per update_game_speed() in script.rpy:
#   Speed         TIER_0  TIER_1  TIER_2  TIER_3
#   Quick  (0)      -1      1       3       5   (TIER_0 fires every day)
#   Standard (1)     1      3       7      10   ← default gameplay
#   Epic   (2)       1      5      11      15
#   Marathon (3)     2      7      15      20
#
# NOTE: script.rpy also sets `default TIER_3_TIME_DELAY = 14` as a Ren'Py store
# initialisation value used before any game starts (i.e. on the title screen).
# Once a save is loaded or a new game starts, update_game_speed() is called and
# overwrites that value.  Standard gameplay therefore uses TIER_3 = 10.
# The stubs below reflect the Standard (speed=1) gameplay values.
#
# For events that should fire every day with no delay, pass 0 directly to
# has_event_delay() rather than through a TIER constant.

TIER_0_TIME_DELAY: int = 1   # Standard speed default (~daily)
TIER_1_TIME_DELAY: int = 3   # Standard speed default (~twice a week)
TIER_2_TIME_DELAY: int = 7   # Standard speed default (~once a week)
TIER_3_TIME_DELAY: int = 10  # Standard speed default (~every 10 days)

"""renpy
init -50 python:
"""
TIER_0_TIME_DELAY = 1
TIER_1_TIME_DELAY = 3
TIER_2_TIME_DELAY = 7
TIER_3_TIME_DELAY = 14  # title-screen / pre-game default; overwritten to 10 by update_game_speed(speed=1)
