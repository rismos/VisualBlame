from kivy.uix.gridlayout import GridLayout
from kivy.app import App

from gui.eventwidget import EventWidget


class CommitContextView(GridLayout, EventWidget):
  head = False
  def __init__(self, **kwargs):
    super(CommitContextView, self).__init__(**kwargs)

  def receive_event_result(self, **kwargs):
    if (kwargs["data"]["id"] == "HEAD") == self.head:
      for widget_id, text in kwargs["data"].iteritems():
        if widget_id in self.ids:
          self.ids[widget_id].text = text

  def getCommitId(self):
    return self.ids["id"].text

  def emptyCommitContext(self):
    for widget_id in self.ids:
      self.ids[widget_id].text = ""
