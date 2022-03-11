import tkinter as tk
import time

# Variable for test application
concat = ['Tien - Teach1', 'Viet - Teach2']
select_firestore = {'Tien - Teach1': 'KuUgdSdWGpTrVHloCphbw5YA8A62', 'Viet - Teach2': 'P4NjjiLZo6hT60YkVy55Ti4duVX2'}

# Global variable that change when click button of tkinter
user_to_access_firebase = ""

# Get id on firestore
def query_id(name_id ,sf):
    user_to_access_firebase = sf[name_id]
    print(user_to_access_firebase + " - " + name_id)

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (chooseTeacherPage, chooseTeacherPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("chooseTeacherPage")
    
    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class chooseTeacherPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('User Selection')
        self.controller.state('zoomed')
        #self.controller.iconphoto(False,tk.PhotoImage(file='C:/Users/urban boutique/Documents/atm tutorial/atm.png'))

        heading_label = tk.Label(self,
            text='Teacher \n Who are you?',
            font=('orbitron',45,'bold'),
            foreground='#ffffff',
            background='#00CC99'
        )
        heading_label.pack(pady=25)

        space_label = tk.Label(self,height=4,bg='#00CC99')
        space_label.pack()

        def check_password():
            controller.show_frame('MenuPage')
                
        enter_button = tk.Button(self,
            text='Enter',
            command=check_password,
            relief='raised',
            borderwidth = 3,
            width=40,
            height=3
        )
        enter_button.pack(pady=10)

        incorrect_password_label = tk.Label(self,
                                                                        text='',
                                                                        font=('orbitron',13),
                                                                        fg='white',
                                                                        bg='#00CCFF',
                                                                        anchor='n')
        incorrect_password_label.pack(fill='both',expand=True)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        cse_photo = tk.PhotoImage(file='image/cse_r.png')
        cse_label = tk.Label(bottom_frame,image=cse_photo)
        cse_label.pack(side='left')
        cse_label.image = cse_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

if __name__ == "__main__":
    app = App()
    app.mainloop()