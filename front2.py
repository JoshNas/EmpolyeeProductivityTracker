import tkinter as tk
from tkinter import font as tkfont
import pandas as pd
from tkinter import messagebox
import time


employee_list = pd.read_csv('employees')
user_id = 0
current_password = ''
sec = 0
run_timer = False


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
        for F in (StartPage, LogInPage, PageTwo, StopWatch):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def select_user(self, user):
        global user_id
        user_id = user
        self.show_frame('LogInPage')

    def get_password(self, pin):
        global current_password
        current_password += pin
        if len(current_password) == 4:
            if employee_list['password'][user_id] == int(current_password):
                self.show_frame("StopWatch")
                current_password = ''
            else:
                messagebox.showinfo("Error", "Invalid PIN")
                current_password = ''

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Log in Page", font=controller.title_font)
        label.grid(row=0, column=0)

        employee_window = tk.Frame(self)
        employee_window.grid(row=1, column=0)
        button1 = tk.Button(employee_window, text=employee_list['name'][0],
                            command=lambda: controller.select_user(0))
        button1.grid(row=0, column=0)
        button2 = tk.Button(employee_window, text=employee_list['name'][1],
                            command=lambda: controller.select_user(1))
        button2.grid(row=0, column=1)
        # tk.Button(employee_window, text='Employee 2').grid(row=0, column=1)
        # tk.Button(employee_window, text='Employee 3').grid(row=1, column=0)
        # tk.Button(employee_window, text='Employee 4').grid(row=1, column=1)
        #
        # button1 = tk.Button(self, text="Log in",
        #                     command=lambda: controller.show_frame("LogInPage"))
        # button1.grid(row=2, column=0)


class LogInPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text='Enter PIN', font=controller.title_font)
        label.grid(row=0, column=0)
        button_window = tk.Canvas(self)
        button_window.grid(row=1, column=0)
        button1 = tk.Button(button_window, text='1', command=lambda: controller.get_password('1'))
        button1.grid(row=1, column=0, sticky='nsew')
        button2 = tk.Button(button_window, text='2', command=lambda: controller.get_password('2'))
        button2.grid(row=1, column=1, sticky='nsew')
        button3 = tk.Button(button_window, text='3', command=lambda: controller.get_password('3'))
        button3.grid(row=2, column=0, sticky='nsew')
        button4 = tk.Button(button_window, text='4', command=lambda: controller.get_password('4'))
        button4.grid(row=2, column=1, sticky='nsew')

        button = tk.Button(self, text="Return to Log In Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3, column=0)


class StopWatch(tk.Frame):
    """ Implements a stop watch frame widget. """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = tk.StringVar()
        self.makeWidgets()
        label = tk.Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        label.grid(row=0, column=0)

        tk.Button(self, text='Start', command=self.Start).grid(row=1, column=0)
        tk.Button(self, text='Stop', command=self.Stop).grid(row=2, column=0)
        tk.Button(self, text='Reset', command=self.Reset).grid(row=3, column=0)

    def makeWidgets(self):
        """ Make the time label. """
        label = tk.Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        label.grid(row=0, column=0)

    def _update(self):
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(50, self._update)

    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 - seconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))

    def Start(self):
        """ Start the stopwatch, ignore if running. """
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1

    def Stop(self):
        """ Stop the stopwatch, ignore if stopped. """
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):
        """ Reset the stopwatch. """
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)




class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        welcome_label = tk.Label(self, text=f'Choose you task {employee_list["name"][user_id]}',
                                 font=controller.title_font)
        welcome_label.grid(row=0, column=0)

        logout = tk.Button(self, text="Log Out", command=lambda: controller.show_frame("StartPage"))
        logout.grid(row=3, column=0)





if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()