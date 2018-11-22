from GUI import Window, Frame
from GUI import Button, Label, ListButton, Slider, TextField, CheckBox
from GUI import application
from GriddedWindow import GriddedWindow


w = GriddedWindow(size=(401,301), style='modal_dialog', title='DemoGui')

theme_list_button = ListButton(width=150, titles=['Standard', 'Dark'])
theme_list_button = ListButton(width=150, titles=['Standard', 'Dark'])
text_label_slider = Slider(orient='h', width=150)
volume_text_field = TextField(text='70', width=150)
fps_list_button   = ListButton(width=150, titles=['29.97', '60.0'])
sound_checkbox    = CheckBox(title='Sound')
save_button       = Button('Save', width=80)
cancel_button     = Button('Cancel', width=80)

w.set_inner_sep(10)
w.set_col_seps([80])
w.set_row_seps([10,10,10,10,30])
w.place_item(Label('Theme:'),    0, 0)
w.place_item(Label('TextLabel'), 1, 0)
w.place_item(Label('Volume:'),   2, 0)
w.place_item(Label('FPS:'),      3, 0)
w.place_item(theme_list_button,  0, 1)
w.place_item(text_label_slider,  1, 1)
w.place_item(volume_text_field,  2, 1)
w.place_item(fps_list_button,    3, 1)
w.place_item(sound_checkbox,     4, 1)
w.place_item(save_button,        5, 0)
w.place_item(cancel_button,      5, 1)


w.show()
application().run()
