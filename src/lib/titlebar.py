import customtkinter as tki

tkfont = tki.CTkFont
tkframe = tki.CTkFrame
tkbutton = tki.CTkButton
tklabel = tki.CTkLabel
tkscrollbar = tki.CTkScrollbar
tkProgressbar = tki.CTkProgressBar
tkOptionMenu = tki.CTkOptionMenu
tkCanvas = tki.CTkCanvas

def goto(x,y):
    root.geometry(f'+{x}+{y}')

def get_pos(event):
    global xwin,ywin
    xwin = root.winfo_x()
    ywin = root.winfo_y()
    startx = event.x_root
    starty = event.y_root
    ywin = ywin - starty
    xwin = xwin - startx

def move_window(event):
    root.geometry(f"+{event.x_root + xwin}+{event.y_root + ywin}")

class CustomTitleBar():
    def __init__(self,main,resizable=True):
        self.resizable = resizable
        
        # Setup root for functions
        global root
        root = main
        
        # Custom title bar
        self.titleBar = tkframe(master=main)
        self.titleBar.pack()
        
        self.menubar = tkframe(master=self.titleBar)
        self.menubar.pack(side='left')
        
        a = main.winfo_width()*4-40*3
        self.title_ = tklabel(master=self.menubar,width=a,text='')
        self.title_.grid(row=0,column=1)
        
        self.close = tkbutton(master=self.titleBar,command=self.close,text='X',
            bg_color='transparent', fg_color='transparent',width=40)
        
        self.close.pack(side='right')
        
        
        self.maximize = tkbutton(master=self.titleBar,command=self.maximize,text='□',
            bg_color='transparent',fg_color='transparent',width=40)
        
        self.maximize.pack(side='right')
        
        
        self.minimize = tkbutton(master=self.titleBar,command=self.minimize,text='-',
            bg_color='transparent',fg_color='transparent',width=40)
        
        self.minimize.pack(side='right')
        
        
        self.title_.bind('<B1-Motion>', move_window)
        self.title_.bind('<Button-1>', get_pos)
        
        main.bind('<Configure>',self.resize)
        root.bind("<Map>", self.unminimize)
        
        
    # Actions
    def close(self):
        root.destroy()
        
    def maximize(self):
        if self.resizable:
            root.state('zoomed')

    def resize(self,event):
        a = root.winfo_width()*0.8-40*3
        self.title_.configure(width=a)
        
    def minimize(self):
        root.state('withdrawn')
        root.overrideredirect(False)
        root.state('iconic')
        
    def unminimize(self,event):
        root.overrideredirect(True)
        
    def title(self,title,size=None):
        self.title_.configure(text=title,font=tkfont(size=size))
        
