import tkinter as tk
import time
from click import command
from cv2 import cv2
from PIL import Image, ImageTk
from threading import Thread
from tkinter import LEFT, RIGHT, TOP, ttk
from need.main import Model, infer
from typing import List
import urllib.request
import numpy as np
import imutils

url = ""

url = "http://192.168.1.5:8080/video"
def char_list_from_file() -> List[str]:
    with open('model/charList.txt') as f:
        return list(f.read())

model = Model(char_list_from_file())

# Variable for test application
concat = ['101 - Nguyen Quoc Viet', '102 - Bang Ngoc Bao Tam', "103 - Trinh Manh Hung"]
course_list = ['Calculus 1', 'Calculus 2', "as"]
class_list = ['CC01']
# Global variable that change when click button of tkinter
user_to_access_firebase = ""
course_to_access_firebase = ""
class_to_access_firebase = ""
path_to_img = ""
done = False
answer = ["check", "check", "Check"]
answer_marking = []

# Get id on firestore
def query_id(name_id):
    global user_to_access_firebase
    user_to_access_firebase = name_id.split(" ")[0]

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (chooseTeacherPage, chooseCoursePage, chooseClassPage, chooseMarkingPage, chooseCameraPage, chooseCapturePage, chooseDisplayPointPage):
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
        if page_name == "chooseDisplayPointPage":
            frame.t1.start()
        frame.tkraise()


class chooseTeacherPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('User Selection')

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
            query_id(name_id)
            controller.show_frame('chooseCoursePage')

        if len(concat) > 2:
            canvas = tk.Canvas(self, bg='#00CC99')
            scroll_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg='#00CC99', background='#00CC99')
            
            frame = tk.Frame(canvas, bg='#00CC99')
            # Add buttons
            lst_btn = []
            for i in range(len(concat)):
                text_display = concat[i]
                teacher_button = tk.Button(frame,
                    text=text_display,
                    command=lambda j=text_display: assign_and_next_frame(j),
                    relief='raised',
                    borderwidth = 1,
                    width=25,
                    height=1,
                    font=('orbitron',15, 'bold'),
                    fg="#6666CC"
                )
                lst_btn.append(teacher_button)
            for i in lst_btn:
                i.pack(pady=20, padx=75)
            
            # Create canvas for scrolling
            canvas.create_window(0, 0, window=frame)
            canvas.update_idletasks()

            canvas.configure(scrollregion=canvas.bbox('all'), 
                            yscrollcommand=scroll_y.set)
                            
            canvas.pack(fill='both', expand=True, side='left')
            scroll_y.pack(fill='y', side='right')
        elif len(concat) == 2:
            teacher1_button = tk.Button(self,
                text=concat[0],
                command=lambda:assign_and_next_frame(concat[0]),
                relief='raised',
                borderwidth = 1,
                width=25,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
            )
            teacher1_button.pack(pady=10)

            teacher2_button = tk.Button(self,
                text=concat[1],
                command=lambda:assign_and_next_frame(concat[1]),
                relief='raised',
                borderwidth = 1,
                width=25,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
                
            )
            teacher2_button.pack(pady=10)
        else:
            teacher1_button = tk.Button(self,
                text=concat[0],
                command=lambda:assign_and_next_frame(concat[0]),
                relief='raised',
                borderwidth = 1,
                width=25,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
            )
            teacher1_button.pack(pady=10)


class chooseCoursePage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Course Selection')

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
            global course_to_access_firebase
            course_to_access_firebase = course_id
            controller.show_frame('chooseClassPage')

        if len(course_list) > 2:
            canvas = tk.Canvas(self, bg='#00CC99')
            scroll_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg='#00CC99', background='#00CC99')
            
            frame = tk.Frame(canvas, bg='#00CC99')
            # Add buttons
            lst_btn = []
            for i in range(len(course_list)):
                text_display = course_list[i]
                course_button = tk.Button(frame,
                    text=text_display,
                    command=lambda j=text_display: assign_and_next_frame(j),
                    relief='raised',
                    borderwidth = 1,
                    width=25,
                    height=1,
                    font=('orbitron',15, 'bold'),
                    fg="#6666CC"
                )
                lst_btn.append(course_button)
            for i in lst_btn:
                i.pack(pady=20, padx=75)
            
            # Create canvas for scrolling
            canvas.create_window(0, 0, window=frame)
            canvas.update_idletasks()

            canvas.configure(scrollregion=canvas.bbox('all'), 
                            yscrollcommand=scroll_y.set)
                            
            canvas.pack(fill='both', expand=True, side='left')
            scroll_y.pack(fill='y', side='right')
        elif len(course_list) == 2:
            course1_button = tk.Button(self,
                text="Course name: " + course_list[0],
                command=lambda:assign_and_next_frame(course_list[0]),
                relief='raised',
                borderwidth = 1,
                width=20,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
            )
            course1_button.pack(pady=10)

            course2_button = tk.Button(self,
                text="Course name: " + course_list[1],
                command=lambda:assign_and_next_frame(course_list[1]),
                relief='raised',
                borderwidth = 1,
                width=20,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
                
            )
            course2_button.pack(pady=10)
        else:
            course1_button = tk.Button(self,
                text="Course name: " + course_list[0],
                command=lambda:assign_and_next_frame(course_list[0]),
                relief='raised',
                borderwidth = 1,
                width=20,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
            )
            course1_button.pack(pady=10)



class chooseClassPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Class Selection')

        heading_label = tk.Label(self,
            text='Which class \n Your marks belong to?',
            font=('orbitron',20,'bold'),
            foreground='#ffffff',
            background='#00CC99'
        )
        heading_label.pack(pady=10)

        space_label = tk.Label(self,height=1,bg='#00CC99')
        space_label.pack()

        def assign_and_next_frame(class_id):
            global class_to_access_firebase
            class_to_access_firebase = class_id
            controller.show_frame('chooseMarkingPage')

        if len(class_list) > 2:
            canvas = tk.Canvas(self, bg='#00CC99')
            scroll_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg='#00CC99', background='#00CC99')
            
            frame = tk.Frame(canvas, bg='#00CC99')
            # Add buttons
            lst_btn = []
            for i in range(len(concat)):
                text_display = "Class " + class_list[i]
                teacher_button = tk.Button(frame,
                    text=text_display,
                    command=lambda j=class_list[i]: assign_and_next_frame(j),
                    relief='raised',
                    borderwidth = 1,
                    width=25,
                    height=1,
                    font=('orbitron',15, 'bold'),
                    fg="#6666CC"
                )
                lst_btn.append(teacher_button)
            for i in lst_btn:
                i.pack(pady=20, padx=75)
            
            # Create canvas for scrolling
            canvas.create_window(0, 0, window=frame)
            canvas.update_idletasks()

            canvas.configure(scrollregion=canvas.bbox('all'), 
                            yscrollcommand=scroll_y.set)
                            
            canvas.pack(fill='both', expand=True, side='left')
            scroll_y.pack(fill='y', side='right')
        elif len(class_list) == 2:
            teacher1_button = tk.Button(self,
                text="Class " + class_list[0],
                command=lambda:assign_and_next_frame(class_list[0]),
                relief='raised',
                borderwidth = 1,
                width=25,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
            )
            teacher1_button.pack(pady=10)

            teacher2_button = tk.Button(self,
                text="Class " + class_list[1],
                command=lambda:assign_and_next_frame(class_list[1]),
                relief='raised',
                borderwidth = 1,
                width=25,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
                
            )
            teacher2_button.pack(pady=10)
        else:
            teacher1_button = tk.Button(self,
                text="Class " + class_list[0],
                command=lambda:assign_and_next_frame(class_list[0]),
                relief='raised',
                borderwidth = 1,
                width=25,
                height=1,
                font=('orbitron',15, 'bold'),
                fg="#6666CC"
            )
            teacher1_button.pack(pady=10)


class chooseMarkingPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Option Selection')

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


class chooseCameraPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Webcam view')

        label = tk.Label(self)#, width=145, height=200)
        label.pack(pady=2)
        global url
        cap = cv2.VideoCapture(url)

        def video_stream():
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # cv2image = cv2.rotate(cv2image, cv2.ROTATE_90_CLOCKWISE)
            cv2image = cv2.resize(cv2image, (268, 201)) # (200, 150))
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            label.after(1000, video_stream)
        
        video_stream()

        def assign_and_next_frame():
            global path_to_img
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
        marking_button.pack(pady=10)


class chooseCapturePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Capture view')

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
            
            self.text.set(text)
            image = Image.open("capture/capture.png")
            image = image.resize((268, 201))
            test = ImageTk.PhotoImage(image)
            label.image = test
            label.configure(image=test)
            label.after(1000, image_change)
                    
        image_change()

        def assign_and_next_frame(blurry, threshold=300):
            global answer_marking
            global done
            if blurry >= threshold:
                controller.show_frame('chooseDisplayPointPage') # Next frame
                ls = ['cropped/0.jpg', 'data/word1.png', 'data/word2.png']
                answer_marking = infer(model, ls)
                done = True
                print(answer_marking)
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
        marking_button.pack(pady=10)


class chooseDisplayPointPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='#00CC99')
        self.controller = controller

        self.controller.title('Point Display')

        self.points = tk.StringVar()
        self.points.set("Marking\n Please wait")
        self.points_num = 0
        space_label1 = tk.Label(self,height=1,bg='#00CC99')
        space_label1.pack()

        heading_label = tk.Label(self,
            # text='Marking',
            textvariable=self.points,
            font=('orbitron', 30,'bold'),
            foreground='#ffffff',
            background='#00CC99'
        )
        heading_label.pack(pady=10)

        space_label = tk.Label(self,height=1,bg='#00CC99')
        space_label.pack()

        def func():
            global done
            while True:
                time.sleep(1)
                if done == True:
                    for i in range(min(len(answer), len(answer_marking))):
                        if answer[i] == answer_marking[i]:
                            self.points_num += 1
                    self.points.set('Result:\n' + str(self.points_num) + ' / ' + str(len(answer)))
                    done = False
                    print("end")
                    break
        
        self.t1 = Thread(target=func)
        # self.t1.start()

        def assign_and_next_frame():
            # self.t1.join()
            controller.show_frame('chooseTeacherPage') # Next frame
        
        def camera_frame():
            # self.t1.join()
            controller.show_frame('chooseCameraPage') # Next frame

                
        marking_button = tk.Button(self,
            text="Upload to Server",
            command=lambda:assign_and_next_frame(),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
        )
        marking_button.pack(pady=10)

        mark_another_button = tk.Button(self,
            text="Mark another",
            command=lambda:camera_frame(),
            relief='raised',
            borderwidth = 1,
            width=20,
            height=1,
            font=('orbitron',15, 'bold'),
            fg="#6666CC"
        )
        mark_another_button.pack(pady=10)

if __name__ == "__main__":
    app = App()
    app.geometry('480x280')
    app.mainloop()
    print(user_to_access_firebase, path_to_img, answer_marking, done)
