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
  "Allgemein":{
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
  "ToBeAdded":{
    "random_setting":{
      "name":"Aha",
      "type":"dropdown",
      "values":["option1", "option2", "option3"],
      "current":0
    },
    "random_setting2":{
      "name":"Interessant",
      "type":"checkbox",
      "values":"",
      "current":False
    },
  },
  "ToBeAdded2":{
    "random_setting":{
      "name":"Hallo",
      "type":"checkbox",
      "values":"",
      "current":True
    }
  }
}