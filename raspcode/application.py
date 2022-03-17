import tkinter as tk
import time
from cv2 import cv2
from PIL import Image, ImageTk
from threading import Thread

# Variable for test application
concat = ['Tien - Teach1', 'Viet - Teach2']
select_firestore = {'Tien - Teach1': 'KuUgdSdWGpTrVHloCphbw5YA8A62', 'Viet - Teach2': 'P4NjjiLZo6hT60YkVy55Ti4duVX2'}
course_lst = ['IELTS', 'cal1']

# Global variable that change when click button of tkinter
user_to_access_firebase = ""
course_to_access_firebase = ""
path_to_img = ""

# Get id on firestore
def query_id(name_id ,sf):
    user_to_access_firebase = sf[name_id]
    print(user_to_access_firebase + " - " + name_id)

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (chooseTeacherPage, chooseCoursePage, chooseMarkingPage, chooseCameraPage, chooseCapturePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
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
        # self.controller.state('zoomed')
        #self.controller.iconphoto(False,tk.PhotoImage(file='C:/Users/urban boutique/Documents/atm tutorial/atm.png'))

        heading_label = tk.Label(self,
            text='Teacher \n Who are you?',
            font=('orbitron',20,'bold'),
            foreground='#ffffff',
            background='#00CC99'
        )
        heading_label.pack(pady=10)

        space_label = tk.Label(self,height=1,bg='#00CC99')
        space_label.pack()

        def assign_and_next_frame(name_id):
            query_id(name_id, select_firestore)
            controller.show_frame('chooseCoursePage')
                
        teacher1_button = tk.Button(self,
            text="I am " + concat[0],
            command=lambda:assign_and_next_frame(concat[0]),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
        )
        teacher1_button.pack(pady=10)

        teacher2_button = tk.Button(self,
            text="I am " + concat[1],
            command=lambda:assign_and_next_frame(concat[1]),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
            
        )
        teacher2_button.pack(pady=10)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        # # TODO: Add later
        # cse_photo = tk.PhotoImage(file='image/cse_r.png')
        # cse_label = tk.Label(bottom_frame,image=cse_photo)
        # cse_label.pack(side='left')
        # cse_label.image = cse_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

class chooseCoursePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Course Selection')
        # self.controller.state('zoomed')
        #self.controller.iconphoto(False,tk.PhotoImage(file='C:/Users/urban boutique/Documents/atm tutorial/atm.png'))

        heading_label = tk.Label(self,
            text='Course \n Which one are you?',
            font=('orbitron',20,'bold'),
            foreground='#ffffff',
            background='#00CC99'
        )
        heading_label.pack(pady=10)

        space_label = tk.Label(self,height=1,bg='#00CC99')
        space_label.pack()

        def assign_and_next_frame(course_id):
            course_to_access_firebase = course_id
            print(course_to_access_firebase)
            controller.show_frame('chooseMarkingPage')
                
        course1_button = tk.Button(self,
            text="Course name: " + course_lst[0],
            command=lambda:assign_and_next_frame(course_lst[0]),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
        )
        course1_button.pack(pady=10)

        course2_button = tk.Button(self,
            text="Course name: " + course_lst[1],
            command=lambda:assign_and_next_frame(course_lst[1]),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
            
        )
        course2_button.pack(pady=10)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        # # TODO: Add later
        # cse_photo = tk.PhotoImage(file='image/cse_r.png')
        # cse_label = tk.Label(bottom_frame,image=cse_photo)
        # cse_label.pack(side='left')
        # cse_label.image = cse_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

class chooseMarkingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Option Selection')
        # self.controller.state('zoomed')
        #self.controller.iconphoto(False,tk.PhotoImage(file='C:/Users/urban boutique/Documents/atm tutorial/atm.png'))

        heading_label = tk.Label(self,
            text='Option \n Which one you choose?',
            font=('orbitron',20,'bold'),
            foreground='#ffffff',
            background='#00CC99'
        )
        heading_label.pack(pady=10)

        space_label = tk.Label(self,height=1,bg='#00CC99')
        space_label.pack()

        def assign_and_next_frame():
            controller.show_frame('chooseCameraPage')
                
        marking_button = tk.Button(self,
            text="Marking",
            command=lambda:assign_and_next_frame(),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
        )
        marking_button.pack(pady=10)

        cancel_button = tk.Button(self,
            text="Cancel",
            command=self.controller.destroy,
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
            
        )
        cancel_button.pack(pady=10)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        # # TODO: Add later
        # cse_photo = tk.PhotoImage(file='image/cse_r.png')
        # cse_label = tk.Label(bottom_frame,image=cse_photo)
        # cse_label.pack(side='left')
        # cse_label.image = cse_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()

class chooseCameraPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Webcam view')
        # self.controller.state('zoomed')
        #self.controller.iconphoto(False,tk.PhotoImage(file='C:/Users/urban boutique/Documents/atm tutorial/atm.png'))

        label = tk.Label(self)#, width=145, height=200)
        label.pack(pady=2)
        cap = cv2.VideoCapture(0)

        def video_stream():
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # cv2image = cv2.rotate(cv2image, cv2.ROTATE_90_CLOCKWISE)
            cv2image = cv2.resize(cv2image, (268, 201)) # (200, 150))
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            label.after(1, video_stream)
        
        video_stream()

        def assign_and_next_frame():
            _, img = cap.read()
            cv2.imwrite('capture/capture.png', img)
            path_to_img = "capture/capture.png"
            
            controller.show_frame('chooseCapturePage')
                
        marking_button = tk.Button(self,
            text="Capture",
            command=lambda:assign_and_next_frame(),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
        )
        marking_button.pack(pady=1)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        # # TODO: Add later
        # cse_photo = tk.PhotoImage(file='image/cse_r.png')
        # cse_label = tk.Label(bottom_frame,image=cse_photo)
        # cse_label.pack(side='left')
        # cse_label.image = cse_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()


class chooseCapturePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Capture view')
        # self.controller.state('zoomed')
        #self.controller.iconphoto(False,tk.PhotoImage(file='C:/Users/urban boutique/Documents/atm tutorial/atm.png'))

        label = tk.Label(self) #, width=145, height=200)
        label.pack(pady=2)
        self.blurry = 100
        self.text = tk.StringVar()
        
        def image_change():
            image_cv2 = cv2.imread("capture/capture.png")
            gray = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2GRAY)
            self.blurry = cv2.Laplacian(gray, cv2.CV_64F).var()
            if self.blurry >= 300:
                text = "{} - Not blur - Continue".format(int(self.blurry))
            else:
                text = "{} - Blur - Recapture".format(int(self.blurry))
            # print(self.blurry)
            
            self.text.set(text)
            image = Image.open("capture/capture.png")
            image = image.resize((268, 201))
            test = ImageTk.PhotoImage(image)
            label.image = test
            label.configure(image=test)
            label.after(1000, image_change)
                    
        image_change()

        def assign_and_next_frame(blurry, threshold=300):
            
            if blurry >= threshold:
                controller.show_frame('chooseTeacherPage') # Next frame
            else:
                controller.show_frame('chooseCameraPage') # Capture frame

                
        marking_button = tk.Button(self,
            textvariable=self.text,
            command=lambda:assign_and_next_frame(self.blurry),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
        )
        marking_button.pack(pady=1)

        bottom_frame = tk.Frame(self,relief='raised',borderwidth=3)
        bottom_frame.pack(fill='x',side='bottom')

        # # TODO: Add later
        # cse_photo = tk.PhotoImage(file='image/cse_r.png')
        # cse_label = tk.Label(bottom_frame,image=cse_photo)
        # cse_label.pack(side='left')
        # cse_label.image = cse_photo

        def tick():
            current_time = time.strftime('%I:%M %p').lstrip('0').replace(' 0',' ')
            time_label.config(text=current_time)
            time_label.after(200,tick)
            
        time_label = tk.Label(bottom_frame,font=('orbitron',12))
        time_label.pack(side='right')

        tick()


if __name__ == "__main__":
    app = App()
    app.geometry('480x280')
    app.mainloop()