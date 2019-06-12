"""
In this file you can add settings by adding entrys to the dictionary.
If you add Setting here, it's going to show up in the settings window
automatically!
So if you do, be careful to specify all details about your setting.
"Values" contains a list with all possible values for the setting. Depending on
the type it's just an empty string.
"Current" is the default setting. This will be the changed by the user.
"""

default_settings = {
  "general":{
    "framerate":{
      "name":"Framerate",
      "type":"dropdown",
      "values":["30 FPS","60 FPS"],
      "current":0
    },
    "resolution":{
      "name":"Auflösung",
      "type":"dropdown",
      "values":["800 x 600","1366 x 768","1280 x 720","1920 x 1080"],
      "current":2
    },
    "projectname":{
      "name":"Projektname",
      "type":"textwindow",
      "values":"",
      "current":"unbenanntes Projekt"
    },
    "projectlocation":{
      "name":"Projektpfad",
      "type":"textwindow",
      "values":"",
      "current":"Hier Projektpfad eingeben",
    }
  },
  # "dummy1":{
  #   "color_theme":{
  #     "name":"Color Theme",
  #     "type":"dropdown",
  #     "values":["dark", "light"],
  #     "current":0
  #   },
  #   "option2":{
  #     "name":"Option 2",
  #     "type":"checkbox",
  #     "values":"",
  #     "current":False
  #   },
  # },
  # "dummy2":{
  #   "option1":{
  #     "name":"Option 1",
  #     "type":"checkbox",
  #     "values":"",
  #     "current":True
  #   }
  # }
}
