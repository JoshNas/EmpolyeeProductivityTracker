import tkinter as tk
from tkinter import font as tkfont
import pandas as pd






class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.grid(row=0, column=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.employee = None
        self.show_frame("StartPage", self.employee)

    def show_frame(self, page_name, current_employee):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        self.employee = current_employee


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Log in Page", font=controller.title_font)
        label.grid(row=0, column=0)

        employee_window = tk.Frame()
        employee_window.grid(row=1, column=0)
        button1 = tk.Button(employee_window, text='Employee 1',
                            command=lambda: controller.show_frame("PageOne", current_employee='Employee1'))
        button1.grid(row=0, column=0)
        button2 = tk.Button(employee_window, text='Employee 2',
                            command=lambda: controller.show_frame("PageOne", current_employee='Employee2'))
        button2.grid(row=0, column=1)
        # tk.Button(employee_window, text='Employee 2').grid(row=0, column=1)
        # tk.Button(employee_window, text='Employee 3').grid(row=1, column=0)
        # tk.Button(employee_window, text='Employee 4').grid(row=1, column=1)
        #
        # button1 = tk.Button(self, text="Log in",
        #                     command=lambda: controller.show_frame("PageOne"))
        # button1.grid(row=2, column=0)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.grid(row=0, column=0)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage", None))
        button.grid(row=1, column=0)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()