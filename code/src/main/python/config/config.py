"""
In this file you can add settings by adding entrys to the dictionary.
If you add Setting here, it's going to show up in the settings window
automatically!
So if you do, be careful to specify all details about your setting.
"Values" contains a list with all possible values for the setting. Depending on
the type it sometimes is just an empty string.
"Current" is the default setting. This will be the changed by the user.

At the moment there are only the types dropdown and checkbox.

If you want to add settings that shouldn't be accessible for the user just put them into the "Invisible" Tab
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
    "Shortcuts": {
        "starter": {
            "name": "Starter",
            "type": "text",
            "values": "",
            "current": "Ctrl"
        },
        "undo": {
            "name": "Rückgängig",
            "type": "text",
            "values": "",
            "current": "z"
        },
        "redo": {
            "name": "Wiederholen",
            "type": "text",
            "values": "",
            "current": "y"
        },
        "export": {
            "name": "Exportieren",
            "type": "text",
            "values": "",
            "current": "e"
        }
    },
    "Invisible": {
        "import_formats": 'Files ( *.png *.jpg *.mp3 *.wav *.mp4);;',
        "project_formats": 'Files ( *.uc);;',
        "filemanager_import_formats": 'Files ( *.png *.jpg *.mp3 *.wav *.mp4 *.pdf);;',
        "autocutvideo_import_formats": 'Files ( *.mp4);;',
        "autocutpdf_import_formats": 'Files ( *.pdf);;',
        "pixels_per_second": 16,
    }
}
