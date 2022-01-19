from . import WidgetBase
import os

class _Button(WidgetBase):
    def __init__(self, master, label, **options):
        super().__init__(master)
        from tkinter.ttk import Button
        if not "command" in options:
            from tkinter import IntVar
            self.var=IntVar(master=self.master, value=0)
            options["command"]=lambda: self.var.set(self.var.get()+1)
            self.widget=Button(self.master, text=label, **options)
        else:
            self.var=None
            self.widget=Button(self.master, text=label, **options)
    def wait(self):
        if self.var is None:
            return
        self.widget.wait_variable(self.var)
    def release(self):
        if self.var is None:
            return
        self.var.set(self.var.get()+1)
class _Form(WidgetBase):
    def __init__(self, master, parent, type="text", **options):
        from tkinter.ttk import Entry
        from tkinter import StringVar
        super().__init__(master, parent=parent)
        self.type=type
        self.var=StringVar(self.master)
        self.value=""
        self.var.trace("w",self.callback)
        if type=="password":
            options.update(show="●")
            self.widget=Entry(self.master, textvariable=self.var, **options)
        elif type=="text":
            self.widget=Entry(self.master, textvariable=self.var, **options)
        elif "file" in type:
            def on_press(event=None):
                if event is None:
                    if "save" in self.type:
                        file=self.parent.Dialog.askfile(save=True)
                    elif "open" in self.type:
                        file=self.parent.Dialog.askfile()
                        if not os.path.exists(file):
                            return
                    elif "openmulti" in self.type:
                        file=self.parent.Dialog.askfile(multi=True)
                        if not os.path.exists(file):
                            return
                    else:
                        file=self.parent.Dialog.askfile(multi=True)
                        if not os.path.exists(file):
                            return
                else:
                    file=event.data
                self.widget.form.delete(0,"end")
                self.widget.form.insert("end", file)
            self.widget=parent.Frame()
            self.widget.setup_dnd(on_press, "file")
            self.widget.form=Entry(self.widget.root, textvariable=self.var, **options)
            self.widget.form.pack(fill="both", side="left", expand=True)
            from tkinter.ttk import Button
            self.widget.button=Button(self.widget.root, text="Select...", command=on_press)
            self.widget.button.pack(side="right")
    def callback(self, *args):
        self.value=self.var.get()
    def set(self, value):
        self.var.set(value)
class _Text(WidgetBase):
    def __init__(self, master, parent, scroll=True, command=None, readonly=False, **options):
        from tkinter import Text
        super().__init__(master, parent=parent)
        self.type=type
        if scroll:
            try:
                from tkinter.scrolledtext import ScrolledText as Text
            except:
                from .scrolledtext import ScrolledText as Text
        self.readonly=readonly
        self.widget=Text(self.master, state=("disabled" if self.readonly else "normal"),**options)
        if not command is None:
            self.widget.bind("<<Modified>>", lambda event: command())
    def insert(self, *args, **options):
        if self.readonly:
            self.configure(state="normal")
        self.widget.insert(*args, **options)
        if self.readonly:
            self.configure(state="disabled")
    def get(self, *args, **options):
        self.widget.get(*args, **options)
    def delete(self, *args, **options):
        self.widget.delete(*args, **options)
    def undo(self):
        self.widget.edit_undo()
    def redo(self):
        self.widget.edit_redo()
class _List(WidgetBase):
    def __init__(self, master, **options):
        super().__init__(master)
        from tkinter.ttk import Treeview
        self.widget=Treeview(self.master, show="tree", **options)
        self.widget.bind("<<TreeviewSelect>>", self.callback)
        self.value=()
    def set_header(self, column, text):
        self.widget.heading("#"+str(column), text=text)
    def add_item(self, parent="", index=0, id=None, label="", values=None, **options):
        if not id is None:
            options.update(iid=id)
        if not values is None:
            options.update(values=values)
        self.widget.insert(parent=parent, index=index, text=label, **options)
    def callback(self, event):
        self.value=self.widget.selection()
    def set_selection(self, items):
        self.value=items
        self.widget.selection_set(items)
    def exist_item(self, id):
        return self.widget.exists(id)
class Input(WidgetBase):
    def Button(self, **options):
        return _Button(self.master, **options)
    def List(self, **options):
        return _List(self.master, **options)
    def Form(self, **options):
        return _Form(self.master, self.parent, **options)
    def Text(self, **options):
        return _Text(self.master, self.parent, **options)