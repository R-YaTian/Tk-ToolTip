# ToolTip widget for Python Tkinter V1.2

from tkinter import *
from time import time

class ToolTip(Toplevel):
    # Provides a ToolTip widget for Tkinter
    # To apply a ToolTip to any Tkinter widget, simply pass the widget to the ToolTip constructor
    def __init__(self, wdgt, msg=None, msgFunc=None, delay=1, follow=True, bgColor='#FFFFFF', font=("Microsoft YaHei UI", "9", "normal"), stime=0):
        """
        Arguments:
          wdgt:    The widget this ToolTip is assigned to
          msg:     A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   Eg: 'delay = 2' means delayed for 3s
          follow:  If True, the ToolTip follows motion, otherwise hides
          bgColor: ToolTip background color
          font:    Eg: font=('Microsoft YaHei UI', size=8)
          stime:   Eg: 'stime = 3' means hide the tip after 4s
        """
        self.wdgt = wdgt
        self.parent = self.wdgt.master                                          # The parent of the ToolTip is the parent of the ToolTips widget
        Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        self.withdraw()                                                         # Hide initially
        self.overrideredirect(True)                                             # The ToolTip Toplevel should have no frame or title bar
        self.msgVar = StringVar()                                               # The msgVar will contain the text displayed by the ToolTip
        if msg == None:
            self.msgVar.set('None')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.stime = stime
        self.timer_id = None
        self.visible = 0
        self.lastMotion = 0
        Message(self, textvariable=self.msgVar, bg=bgColor, aspect=1000, font=font, bd=-1).grid() # The text of the ToolTip is displayed in a Message widget
        self.wdgt.bind('<Enter>', self.spawn, '+')                                                # Add bindings to the widget.This will NOT override bindings that the widget already has
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Button-1>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        #Spawn the ToolTip.This simply makes the ToolTip eligible for display
        #Usually this is caused by entering the widget
        """
        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        if self.delay == 0:
            self.show()
        elif self.timer_id is None:
            self.timer_id = self.after(int((self.delay + 1) * 1000), self.show) # The after function takes a time argument in miliseconds

    def show(self):
        #Displays the ToolTip if the time delay has been long enough
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()
        if self.stime != 0:
            self.timer_id = self.after(int((self.stime + 1) * 1000), self.hide)

    def move(self, event):
        #Processes motion within the widget
        """
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        if self.follow == False and self.delay != 0 and self.stime == 0:        # If the follow flag is not set, motion within the widget will make the ToolTip disappear(Unless delay set to 0 or stime not 0)
            self.withdraw()
            self.visible = 1
        self.geometry('+%i+%i' % (event.x_root, event.y_root+20))               # Offset the ToolTip 20 pixes south of the pointer
        try:
            if self.msgFunc is not None:
                self.msgVar.set(eval(self.msgFunc))                             # Try to call the message function.Will not change the message if the message function is None or the message function fails
        except:
            pass
        if self.delay != 0 and self.stime == 0:
            self.after(int((self.delay + 1) * 1000), self.show)

    def hide(self, event=None):
        #Hide the ToolTip.Usually this is caused by leaving the widget
        """
        Arguments:
          event: The event that called this function
        """
        if self.timer_id is not None:
            tid = self.timer_id
            self.timer_id = None
            self.after_cancel(tid)
        self.withdraw()
        self.visible = 0


def xrange2d(n, m):
    """
    Returns a generator of values in a 2d range
    Arguments:
      n: The number of rows in the 2d range
      m: The number of columns in the 2d range
    Returns:
      A generator of values in a 2d range
    """
    return ((i,j) for i in xrange(n) for j in xrange(m))

def range2d(n, m):
    """
    Returns a list of values in a 2d range
    Arguments:
      n: The number of rows in the 2d range
      m: The number of columns in the 2d range
    Returns:
      A list of values in a 2d range
    """
    return [(i,j) for i in range(n) for j in range(m)]

def example():
    root = Tk()
    root.resizable(0, 0)
    btnList = []
    for (i,j) in range2d(6,4):
        text = 'delay=%i\n' % i
        delay = i
        if j >= 2:
            follow = True
            text += '+follow\n'
        else:
            follow = False
            text += '-follow\n'
        if j % 2 == 0:
            msg = None
            msgFunc = 'time()'
            text += 'Message Function\n'
            stime = 0
            text += 'stime=0'
        else:
            msg = 'Button at %s' % str((i,j))
            msgFunc = None
            text += 'Static Message\n'
            stime = 2
            text += 'stime=2'
        btnList.append(Button(root, text=text))
        ToolTip(btnList[-1], msg=msg, msgFunc=msgFunc, follow=follow, delay=delay, stime=stime)
        btnList[-1].grid(row=i, column=j, sticky=N+S+E+W)
    root.mainloop()

if __name__ == '__main__':
    example()
