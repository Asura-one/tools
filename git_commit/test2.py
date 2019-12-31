import npyscreen


class App(npyscreen.StandardApp):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Commit 规范工具")


class MainForm(npyscreen.ActionForm):
    # Constructor
    def create(self):
        # Add the TitleText widget to the form
        self.title = self.add(npyscreen.TitleText,
                              name="TitleText",
                              value="Hello World!")

    # Override method that triggers when you click the "ok"
    def on_ok(self):
        self.parentApp.setNextForm(None)

    # Override method that triggers when you click the "cancel"
    def on_cancel(self):
        self.title.value = "Hello World!"


MyApp = App()
MyApp.run()