import npyscreen
import os
import getpass
import subprocess


class mainform(npyscreen.ActionForm):
    def create(self):
        self.OSPath = "/SYS64 3.7/"
        self.full_path = os.getcwd()
        self.CurrentPath = ""
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        opt_values = ["jdos", "jdos.fboot", "jdos.admin", "jdos.exp"]
        welcome_box = self.add(npyscreen.BoxTitle,
                               max_height=2,
                               editable=False,
                               value="Welcome. Select BOOT PARAMETER")
        self.answer = self.add(npyscreen.TitleSelectOne,
                               max_height=4,
                               name="Selections:",
                               values=opt_values,
                               scroll_exit=True)

    def on_ok(self):
        if self.answer.value[0] == 0:
            subprocess.call(
                ["python3", self.dir_path + self.OSPath + "bootthingy.py"])
            subprocess.call(
                ["python3", self.dir_path + self.OSPath + "jdosos.py"])
        elif self.answer.value[0] == 1:
            subprocess.call(
                ["python3", self.full_path + self.OSPath + "jdosos.py"])
        elif self.answer.value[0] == 2:
            user = getpass.getpass("username: ")
            password = getpass.getpass("password: ")
            bootcheck = 0
            with open('userpass.txt', 'r') as file:
                for line in file:
                    line = line.strip('\n')
                    login = line.split(',')
                    if login[0] == user and login[1] == password:
                        subprocess.call([
                            "python3",
                            self.full_path + self.OSPath + "jdososadmin.py"
                        ])
                        bootcheck = 1
                if bootcheck == 0:
                    print("Incorrect user or password.")
        elif self.answer.value[0] == 3:
            subprocess.call([
                "python3",
                self.full_path + self.OSPath + "jdosexperimentail.py"
            ])
        self.parentApp.setNextForm(None)

    def on_cancel(self):
        self.parentApp.setNextForm(None)


#Application starts here
class App(npyscreen.NPSAppManaged):
    #Defining forms.
    def onStart(self):
        self.addForm('MAIN', mainform, name="name_here")


if __name__ == "__main__":
    app = App().run()