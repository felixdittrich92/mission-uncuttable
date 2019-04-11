"""
In this file you can add settings by adding entrys to the dictionary.
If you do so be careful to specify all details about your setting.
category means in wich tab in the settings window your setting will be displayed.
"""

default_settings = {
  "Allgemein":{
    "language":{
      "name":"Language",
      "type":"dropdown",
      "value":"english"
    },
  },
  "Design":{
    "color_theme":{
      "name":"Color Theme",
      "type":"checkbox",
      "value":"dark"
    },
    "option2":{
      "name":"Option 2",
      "type":"checkbox",
      "value":"false"
    },
    "option1":{
      "name":"Option 1",
      "type":"checkbox",
      "value":"true"
    },
  },
  "ShortCuts":{
    "option1":{
      "name":"Option 1",
      "type":"checkbox",
      "value":"true"
    }
  }
}