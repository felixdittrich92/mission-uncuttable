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
    "general": {
        "language": {
            "type": "dropdown",
            "values": ["English", "Deutsch"],
            "current": 0
        },
        "history_limit": {
            "type": "spinbox",
            "values": [1, 100],  # min and max history size
            "current": 30
        },
        "projects_path": {
            "name": "Projects Path",
            "type": "text",
            "values": "",
            "current": "~/ubicut/"
        }
    },
    "design": {
        "color_theme": {
            "type": "dropdown",
            "values": ["dark", "light"],
            "current": 0
        },
    },
    "shortcuts": {
        "starter": {
            "type": "text",
            "values": "",
            "current": "Ctrl"
        },
        "undo": {
            "type": "text",
            "values": "",
            "current": "z"
        },
        "redo": {
            "type": "text",
            "values": "",
            "current": "y"
        },
        "save": {
            "type": "text",
            "values": "",
            "current": "s"
        },
        "saveas": {
            "type": "text",
            "values": "",
            "current": "Shift+s"
        },
        "export": {
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
