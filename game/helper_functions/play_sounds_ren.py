from __future__ import annotations
import renpy
"""renpy
IF FLAG_OPT_IN_ANNOTATIONS:
    rpy python annotations
init 10 python:
"""
import re

SOUND_FOLDER = "sounds"

def generate_sound_list(sound_name):
    return [x for x in renpy.list_files() if re.match(rf"{SOUND_FOLDER}\/.*({sound_name}).*", x, re.IGNORECASE)]

moan_sounds = generate_sound_list("Moan")
orgasm_sounds = generate_sound_list("Orgasm")
slap_sounds = generate_sound_list("Slap")
breathing_sounds = generate_sound_list("Breathing")
gag_sounds = generate_sound_list("Gag")
swallow_sounds = generate_sound_list("Swallow")
mouthful_sounds = generate_sound_list("Mouthful")
blowjob_sounds = generate_sound_list("Blowjob")
notification_sounds = generate_sound_list("Notification")
message_sounds = generate_sound_list("Message")
ring_sounds = generate_sound_list("Ring")

def play_moan_sound():
    play_sound(moan_sounds)

def play_female_orgasm():
    play_sound(orgasm_sounds)

def play_spank_sound():
    play_sound(slap_sounds)

def play_breathing_sound():
    play_sound(breathing_sounds)

def play_gag_sound():
    play_sound(gag_sounds)

def play_swallow_sound():
    play_sound(swallow_sounds)

def play_blowjob_sound():
    play_sound(blowjob_sounds)

def play_mouthful_sound():
    play_sound(mouthful_sounds)

def play_notification_sound():
    play_sound(notification_sounds)

def play_message_sound():
    play_sound(message_sounds, "effects")

def play_ring_sound():
    play_sound(ring_sounds, "effects")

def play_sound(sounds_list, channel = "sex"):
    if sounds_list:
        renpy.play(renpy.random.choice(sounds_list), channel)
