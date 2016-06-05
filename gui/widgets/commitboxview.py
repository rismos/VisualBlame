from collections import namedtuple

from kivy.uix.boxlayout import BoxLayout

from gui.eventwidget import EventWidget
from gui.widgets.recolorablebg import WidgetRecolorableBorder


class CommitBox(BoxLayout, WidgetRecolorableBorder):
  def __init__(self, commit_hex="", commit_date="", commit_message="",
               **kwargs):
    super(CommitBox, self).__init__(**kwargs)
    self.commit_hex = commit_hex
    self.ids["commit_hex"].text = commit_hex[:5]
    self.ids["commit_date"].text = commit_date[:8]
    self.ids["commit_message"].text = commit_message


class CommitBoxView(BoxLayout, EventWidget):
  active_commits = {}

  def init_event_call(self, event_config, function):
    super(CommitBoxView, self).init_event_call(event_config, function)
    self.event_call("HEAD", 10)

  def event_call(self, commit_id, amount):
    args = {"commit_id": commit_id}
    super(CommitBoxView, self).event_call(args)

  def process_event_result(self, data, **kwargs):
    # Commit context result
    if type(data) is list:
      self.clear_widgets()
      for commit_data in data:
        self.add_widget(CommitBox(commit_hex=commit_data["id"], commit_date=commit_data["date"],
                                  commit_message=commit_data["message"]))
        self._update_active_commits()
    # Log result
    else:
      args = {"commit_id": data.commit_ids}
      super(CommitBoxView, self).event_call(args, 1)

  def update_viewed_commit(self, active_commit, commit_id, color):
    ActiveCommit = namedtuple('ActiveCommit', ['commit_id', 'color'])
    self.active_commits[active_commit] = ActiveCommit(commit_id, color)
    self._update_active_commits()

  def _update_active_commits(self):
    for commit_box in self.children:
      for key, active_commit in self.active_commits.iteritems():
        if commit_box.commit_hex == active_commit.commit_id:
          commit_box.border_color = active_commit.color
          break
