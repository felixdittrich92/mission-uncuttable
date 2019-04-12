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
  "Allgemein":{
    "language":{
      "name":"Language",
      "type":"dropdown",
      "values":["English","German","Esperanto"],
      "current":"english"
    },
  },
  "Design":{
    "color_theme":{
      "name":"Color Theme",
      "type":"dropdown",
      "values":["dark", "light"],
      "current":"dark"
    },
    "option2":{
      "name":"Option 2",
      "type":"checkbox",
      "values":"",
      "current":"false"
    },
    "option1":{
      "name":"Option 1",
      "type":"button",
      "values":"",
      "current":"true"
    },
  },
  "ShortCuts":{
    "option1":{
      "name":"Option 1",
      "type":"checkbox",
      "values":"",
      "current":"true"    }
  }
}