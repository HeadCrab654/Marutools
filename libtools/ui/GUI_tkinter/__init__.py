import os
from libtools.exception import UIError
from libtools.ui.GUI_tkinter.menu import Menu as _Menu

class TKINTER():
    def __init__(self, config, logger, type="main", master=None):
        self.master=master
        self.logger=logger
        self.config=config
        self.type=type
        self.conf=config.conf
        self.appinfo=config.appinfo
        self.backend="tkinter"
        if type=="main":
            try:
                import tkinter
            except:
                raise UIError("GUI is not supported")
            os.environ['TKDND_LIBRARY'] = os.path.join(self.appinfo["share_os"],"tkdnd")
            try:
                from .tkdnd import Tk
            except Exception as e:
                self.logger.exception(e)
                from tkinter import Tk
                self.dnd = False
            else:
                self.dnd = True
            self._root=Tk(className=self.appinfo["appname"])
            #ttkthemes
            try:
                from ttkthemes import ThemedStyle as Style
                self._root.style = Style()
            except:
                from tkinter.ttk import Style
                self._root.style = Style()
            self._root.report_callback_exception=self.tkerror
            self.changeTitle(self.appinfo["appname"])
            if "theme" in self.conf:
                self.changeStyle(self.conf["theme"])
        elif type=="sub":
            from tkinter import Toplevel
            self._root=Toplevel()
            self.master
        self.aqua=(self.appinfo["os"] == "Darwin" and self._root.tk.call('tk', 'windowingsystem') == "aqua")
        import tkinter.ttk as ttk
        self.root=ttk.Frame(self._root)
        self.root.pack(fill="both", expand=True)
        from .dialog import Dialog
        self.Dialog=Dialog()
    def changeTitle(self, title):
        self._root.title(title)
    def changeStyle(self, name):
        self._root.style.theme_use(name)
        self.logger.info("Theme:"+self.conf["theme"])
    def changeIcon(self, icon_path):
        from PIL import Image, ImageTk
        icon=ImageTk.PhotoImage(Image.open(icon_path))
        self._root.iconphoto(True, icon)
    def fullscreen(self, tf=None):
        if tf is None:
            tf = not self._root.attributes("-fullscreen")
        self._root.attributes("-fullscreen", tf)
    def tkerror(self, exception, value, t):
        import tkinter
        sorry = tkinter.Toplevel()
        sorry.title("Marueditor - Error")
        tkinter.Label(sorry,text="We're sorry.\n\nError is happen.").pack()
        t = tkinter.Text(sorry)
        t.pack()
        t.insert("end","Error report=========\n")
        t.insert("end",str(exception)+"\n")
        t.insert("end",str(value)+"\n")
        t.insert("end",str(t)+"\n")
        tkinter.Button(sorry, text="EXIT", command=sorry.destroy).pack()
        #sorry.protocol("WM_DELETE_WINDOW",sorry.destroy)
    def changeSize(self, size):
        self._root.geometry(size)
    def main(self):
        try:
            from tkinter.scrolledtext import ScrolledText
        except:
            from .scrolledtext import ScrolledText
    def setcallback(self, name, callback):
        if name=="close":
            self._root.protocol("WM_DELETE_WINDOW", callback)
            if self.aqua:
                self._root.createcommand('tk::mac::Quit', callback)
        elif name=="macos_help" and self.aqua:
            self._root.createcommand('tk::mac::ShowHelp', callback)
        elif name=="macos_settings" and self.aqua:
            self._root.createcommand('tk::mac::ShowPreferences')
    def Menu(self, **options):
        return _Menu(self._root, **options)
    def Notebook(self, close=None, command=None, **options):
        if close is None:
            from tkinter.ttk import Notebook
            note=Notebook(self.root)
        else:
            from .widgets import CustomNotebook
            note=CustomNotebook(self.root)
        note.enable_traversal()
        if not command is None:
            note.bind("<<NotebookTabClosed>>",lambda null: command)
        note.pack(fill="both", expand=True)
        return note
    def mainloop(self):
        self._root.mainloop()

class WidgetBase():
    def __init__(self, master):
        self.backend="tkinter"
        self.master=master