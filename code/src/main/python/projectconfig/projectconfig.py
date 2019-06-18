"""
In this file you can add settings by adding entrys to the dictionary.
If you add Settings here, it's going to show up in the PROJECTsettings window
automatically!
So if you do, be careful to specify all details about your setting.
"Values" contains a list with all possible values for the setting. Depending on
the type it's just an empty string.
"Current" is the default setting. This will be the changed by the user.
"""

default_settings = {
  "general":{
    "framerate":{
      # "name":"Framerate",
      "type":"dropdown",
      "values":["30 FPS","60 FPS"],
      "current":0
    },
    "resolution":{
      # "name":"Auflösung",
      "type":"dropdown",
      "values":["800 x 600","1366 x 768","1280 x 720","1920 x 1080"],
      "current":2
    },
  },
}