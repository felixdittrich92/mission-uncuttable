"""
In this file you can add settings by adding entrys to the dictionary.
If you add Setting here, it's going to show up in the settings window
automatically!
So if you do, be careful to specify all details about your setting.
"Values" contains a list with all possible values for the setting. Depending on
the type it sometimes is just an empty string.
"Current" is the default setting. This will be the changed by the user.

At the moment there are only the types dropdown and checkbox.
"""

default_settings = {
    "Allgemein": {
        "language": {
            "name": "Language",
            "type": "dropdown",
            "values": ["English", "German", "Esperanto"],
            "current": 0
        },
    },
    "Design": {
        "color_theme": {
            "name": "Color Theme",
            "type": "dropdown",
            "values": ["dark", "light"],
            "current": 0
        },
        "option2": {
            "name": "Option 2",
            "type": "checkbox",
            "values": "",
            "current": False
        },
        "option1": {
            "name": "Option 1",
            "type": "button",
            "values": "",
            "current": True
        },
    },
    "ShortCuts": {
        "option1": {
            "name": "Option 1",
            "type": "checkbox",
            "values": "",
            "current": True}
    },
    "Filemanager": {
        "import_formats": 'Files ( *.png *.jpg *.mp3 *.wav *.mp4);;'
    },
    "AutoCutVideo": {
        "import_formats": 'Files ( *.mp4);;'
    },
    "AutoCutPDF": {
        "import_formats": 'Files ( *.pdf);;'
    }
}
