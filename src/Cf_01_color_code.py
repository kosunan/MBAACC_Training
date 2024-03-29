from utils.common import get_font
import json


def load_color_codes(filename="color_codes.json"):
    default_color_codes = {
        "attack_color": {"text": (255, 255, 255), "bg": (255, 0, 0)},
        "motion_color": {"text": (255, 255, 255), "bg": (65, 200, 0)},
        "guard_stun_color": {"text": (255, 255, 255), "bg": (170, 170, 170)},
        "hit_stun_color": {"text": (255, 255, 255), "bg": (170, 170, 170)},
        "available_action_color": {"text": (92, 92, 92), "bg": (0, 0, 0)},
        "jump_color": {"text": (177, 177, 177), "bg": (241, 224, 132)},
        "shield_color": {"text": (255, 255, 255), "bg": (145, 194, 255)},
        "invincible_color": {"text": (200, 200, 200), "bg": (255, 255, 255)},
        "invincible_attack_color": {"text": (255, 255, 255), "bg": (255, 160, 160)},
        "advantage_color": {"text": (255, 255, 255), "bg": (0, 0, 0)},
        "bunker_color": {"text": (255, 255, 255), "bg": (225, 184, 0)},
        "bunker_attack_color": {"text": (255, 255, 255), "bg": (225, 102, 0)},
        "airborne_color": {"text": (125, 127, 168), "bg": (125, 127, 168)},
        "hitstop_color": {"text": (255, 255, 255), "bg": (59, 69, 129)},
        "wake_up_color": {"text": (255, 255, 255), "bg": (85, 33, 79)},
        "adv_color": {"text": (255, 255, 255), "bg": (25, 25, 25)},
        "motion_color2": {"text": (255, 255, 255), "bg": (35, 158, 0)},
        "free_color": {"text": (0, 0, 0), "bg": (0, 0, 0)},
        "tape_color1": {"text": (155, 155, 155), "bg": (0, 0, 0)},
        "tape_color2": {"text": (255, 255, 255), "bg": (0, 0, 0)},
        "keyDir_color": {"text": [255, 255, 255], "bg": [10, 10, 10]},
    }

    try:
        with open(filename, "r") as file:
            color_codes = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        color_codes = default_color_codes

    return color_codes


def get_color(font_name, color_code):
    text_color = tuple(color_code["text"])
    bg_color = tuple(color_code["bg"])
    return get_font(text_color, bg_color)


color_codes = load_color_codes()

color_dict = {
    font_name: get_color(font_name, color_codes[font_name]) for font_name in color_codes
}
