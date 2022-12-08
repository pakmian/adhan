class QuranTask:
  def __init__(self, FileID, Desc, Location, Checked):
    self.FileID = FileID
    self.Desc = Desc
    self.Location = Location
    self.Checked = Checked

  def myfunc(self):
    print(str(self.FileID) + "\n" + self.Desc + "\n" + self.Location + "\n" + self.Checked)
