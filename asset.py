import os
import sys

this_path = os.path.dirname(sys.argv[0])

background = {
    "Lobby": f"{this_path}\\asset\\background\\Lobby.png",
    "Start": f"{this_path}\\asset\\background\\StartX20_700.png",
    "End": f"{this_path}\\asset\\background\\End.png"
}

sprite = {
    "apple": f"{this_path}\\asset\\sprite\\apple.png",
    "snake": {
        "body": f"{this_path}\\asset\\sprite\\snake_body.png",
        "curve_west": f"{this_path}\\asset\\sprite\\snake_curve_west.png",
        "curve": f"{this_path}\\asset\\sprite\\snake_curve.png",
        "head": f"{this_path}\\asset\\sprite\\snake_head.png",
        "tail": f"{this_path}\\asset\\sprite\\snake_tail.png"
    }
}

font = {
    "NeoDunggeunmo": f"{this_path}\\asset\\font\\NeoDunggeunmoPro-Regular.ttf"
}

sound = {
    "background": {
        "Start": f"{this_path}\\asset\\sound\\background\\Start.mp3"
    },
    "sfx": {
        "apple_bite": [
            f"{this_path}\\asset\\sound\\sfx\\apple_bite1.mp3",
            f"{this_path}\\asset\\sound\\sfx\\apple_bite2.mp3",
            f"{this_path}\\asset\\sound\\sfx\\apple_bite3.mp3"
        ],
        "hurt": f"{this_path}\\asset\\sound\\sfx\\hurt.mp3"
    }
}
