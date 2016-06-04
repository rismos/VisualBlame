from collections import namedtuple

from kivy.uix.stacklayout import StackLayout
from kivy.effects.scroll import ScrollEffect
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button

from gui.eventwidget import EventWidget


class TabButton(Button):
  is_selected = False

  def __init__(self, callback, **kwargs):
    self.callback = callback
    super(TabButton, self).__init__(**kwargs)

  def on_press(self):
    if not self.is_selected:
      self.callback(self.text)
      self.select()

  def select(self):
    self.is_selected = True
    self.background_color = self.selected_background_color

  def deselect(self):
    self.is_selected = False
    self.background_color = self.deselected_background_color


class TabPanel(StackLayout):
  def __init__(self, select_callback, **kwargs):
    self.select_callback = select_callback
    super(TabPanel, self).__init__(**kwargs)

  def add_buttons(self, button_names):
    for name in button_names:
      self.add_widget(TabButton(text=name, callback=self.item_select_callback))

  def item_select_callback(self, text):
    self.deselect_buttons()
    self.select_callback(text)

  def select_button(self, index):
    self.children[index].on_press()

  def select_button_by_name(self, name):
    names = [child.text for child in self.children]
    try:
      self.select_button(names.index(name))
    # This can happen when the log results come in before the blame
    # results in the GUI, meaning that the argument name could
    # not have a corresponding child here (can happen if they both are
    # finished so quickly that they are scheduled for the same frame)
    except ValueError:
      pass

  def deselect_buttons(self):
    for button in self.children:
      button.deselect()


class ButtonTabPanel(ScrollView, EventWidget):
  effect_cls = ScrollEffect
  view_to_update = None
  active_file = ""

  def __init__(self, **kwargs):
    super(ButtonTabPanel, self).__init__(**kwargs)
    self._init_tab_panel()

  def _init_tab_panel(self):
    self._remove_tab_buttons()
    self.button_container = TabPanel(select_callback=self.update_list)
    self.add_widget(self.button_container)

  def _remove_tab_buttons(self):
    try:
      self.remove_widget(self.button_container)
    # The first time time there is no button container, catch the error
    except AttributeError:
      pass

  def process_event_result(self, data=[], **kwargs):
    # TODO find another way to do this, this data is most likely also in the cache..
    self.data = data
    # print self.view_to_update
    file_names = [file_name for file_name in data]

    self._init_tab_panel()

    self.button_container.add_buttons(file_names)
    self.select_actile_file()

  def select_actile_file(self):
    self.button_container.select_button_by_name(self.active_file)

  def update_active_file(self, active_file):
    self.active_file = active_file
    self.select_actile_file()

  def update_list(self, file_name):
    if self.view_to_update and file_name in self.data:
      self.view_to_update.init_code_view(data=self.data[file_name])
      self.selected_file = file_name
