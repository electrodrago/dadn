import tkinter as tk
import time
from click import command
from cv2 import cv2
from PIL import Image, ImageTk
from threading import Thread
from tkinter import LEFT, RIGHT, TOP, Tk, ttk
from need.main import Model, infer
from typing import List
import urllib.request
import numpy as np
import imutils
import os

# Database setup
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from functools import reduce

cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
"""----------------------------------------------------------------------------------------------------"""
# Select teacher, to retrieve answer and store the marking result on database
# Display format: Teacher Name - Teacher ID
# How to select, all teacher ID is store in dictionary: TeacherID - ID on Firestore
# TODO: Code with tktiner client

select_teacher = db.collection('Sample_Teacher')
teachers = select_teacher.stream()

# id_list store id on firebase
# dict_list store dictionary of field of documents

teacher_id = []
teacher_infor = []
for teacher in teachers:
    teacher_id.append(teacher.id)
    teacher_infor.append(teacher.to_dict())

# print("teacher_id: ", teacher_id )
# print("teacher_infor: ", teacher_infor)

concat = []
for i in range(len(teacher_id)):
    concat.append(teacher_id[i] + ' - ' + teacher_infor[i]['T_Name'])
print("teacher_id and teacher_name :", concat)
"""----------------------------------------------------------------------------------------------------"""
# # Global variable
user_to_access_firebase = "1952493"


def getCourses(teacher_id):
    select_course = db.collection(
        'Sample_Teacher').document(
            teacher_id).collection(
                'COURSE')
    courses = select_course.stream()

    course_list = reduce(lambda acc, ele: acc + [ele.id], courses, [])
    # print(course_list)
    return course_list


course_list = getCourses(user_to_access_firebase)


# # Global variable
course_to_access_firebase = course_list[0]

def getClasses(teacher_id, Course_name):
    select_class = db.collection(
        'Sample_Teacher').document(
            teacher_id).collection(
                'COURSE').document(
                    Course_name).collection(
                        'CLASS')
    classes = select_class.stream()
    class_list = reduce(lambda acc, ele: acc + [ele.id], classes, [])
    return class_list

class_list = getClasses(user_to_access_firebase, course_to_access_firebase)

# # Global variable    
class_to_access_firebase = class_list[0]

def getSemester(teacher_id, coure_name, class_id):
    select_semester = db.collection(
        'Sample_Teacher').document(
            teacher_id).collection(
                'COURSE').document(
                    coure_name).collection(
                        'CLASS').document(
                            class_id).collection(
                                "SEMESTER"
                            )
    semesters = select_semester.stream()
    semester_list = reduce(lambda acc, ele: acc + [ele.id], semesters, [])
    return semester_list
semester_list = getSemester(user_to_access_firebase,course_to_access_firebase,class_to_access_firebase)


# # Global variable    
semester_to_access_firebase = semester_list[0]
def getAnswerfile(teacher_id, coure_name, class_id,semester):
    return  db.collection(
        'Sample_Teacher').document(
            teacher_id).collection(
                'COURSE').document(
                    coure_name).collection(
                        'CLASS').document(
                            class_id).collection(
                                "SEMESTER"
                                ).document(
                                    semester
                                )



answer = getAnswerfile(user_to_access_firebase, course_to_access_firebase, class_to_access_firebase,semester_to_access_firebase).get().to_dict()['AnswerFile']



def getStudents(teacher_id, coure_name, class_id, semester_id):
    select_student = db.collection(
        'Sample_Teacher').document(
            teacher_id).collection(
                'COURSE').document(
                    coure_name).collection(
                        'CLASS').document(
                            class_id).collection(
                                "SEMESTER"
                                ).document(
                                    semester_id
                                    ).collection(
                                        "STUDENT"
                                     )
    students = select_student.stream()
    student_ids = reduce(lambda acc, ele: acc + [ele.id], students, [])
    return student_ids
student_list = getStudents(user_to_access_firebase, course_to_access_firebase, class_to_access_firebase, semester_to_access_firebase)
def UpdateStudentMark(teacher_id, coure_name, class_id, semester_id, student_id, mark):
    db.collection(
        'Sample_Teacher').document(
            teacher_id).collection(
                'COURSE').document(
                    coure_name).collection(
                        'CLASS').document(
                            class_id).collection(
                                "SEMESTER"
                                ).document(
                                    semester_id
                                    ).collection(
                                        "STUDENT"
                                     ).document(
                                        student_id
                                     ).update({'S_Point': int(mark)})
    return None
# Upload to server
# Global variable
Student_point = 0

# is_exist = check(getAnswerfile(user_to_access_firebase, course_to_access_firebase, class_to_access_firebase,semester_to_access_firebase).collection('STUDENT'))


url = "http://10.127.32.234:4747/video"
def char_list_from_file() -> List[str]:
    with open('model/charList.txt') as f:
        return list(f.read())

model = Model(char_list_from_file())


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
        for F in (chooseTeacherPage, chooseCoursePage, chooseClassPage, chooseSemesterPage, chooseMarkingPage, chooseCameraPage, chooseCapturePage, chooseDisplayPointPage, chooseStudentIDPage):
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
        if page_name == 'chooseCoursePage':
            self.frames[page_name] = chooseCoursePage(parent=self.container, controller=self)
        elif(page_name == 'chooseClassPage'):
            self.frames[page_name] = chooseClassPage(parent=self.container, controller=self)
        elif(page_name == 'chooseSemesterPage'):
            self.frames[page_name] = chooseSemesterPage(parent=self.container, controller=self)
        elif(page_name == 'chooseStudentIDPage'):
            self.frames[page_name] = chooseStudentIDPage(parent=self.container, controller=self)
        
        self.frames[page_name].grid(row=0, column=0, sticky="nsew")
        frame = self.frames[page_name]        
        if page_name == "chooseDisplayPointPage":
            frame.trigger()
        
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
            global course_list
            course_list = getCourses(user_to_access_firebase)
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
            global class_list
            class_list = getClasses(user_to_access_firebase, course_to_access_firebase)
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
            global semester_list
            semester_list = getSemester(user_to_access_firebase, course_to_access_firebase, class_id)
            controller.show_frame('chooseSemesterPage')
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

class chooseSemesterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#00CC99')
        self.controller = controller

        self.controller.title('Semester Selection')

        heading_label = tk.Label(self,
                                 text='Which Semester \n Your marks belong to?',
                                 font=('orbitron', 20, 'bold'),
                                 foreground='#ffffff',
                                 background='#00CC99'
                                 )
        heading_label.pack(pady=10)

        space_label = tk.Label(self, height=1, bg='#00CC99')
        space_label.pack()

        def assign_and_next_frame(semester_id):
            global semester_to_access_firebase
            semester_to_access_firebase = semester_id
            global answer
            print(user_to_access_firebase, course_to_access_firebase, class_to_access_firebase, semester_to_access_firebase)
            answer = getAnswerfile(user_to_access_firebase, course_to_access_firebase, class_to_access_firebase,semester_to_access_firebase).get().to_dict()['AnswerFile']
            controller.show_frame('chooseMarkingPage')

        if len(semester_list) > 2:
            canvas = tk.Canvas(self, bg='#00CC99')
            scroll_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg='#00CC99', background='#00CC99')

            frame = tk.Frame(canvas, bg='#00CC99')
            # Add buttons
            lst_btn = []
            for i in range(len(concat)):
                text_display = "Semester " + semester_list[i]
                teacher_button = tk.Button(frame,
                                           text=text_display,
                                           command=lambda j=semester_list[i]: assign_and_next_frame(j),
                                           relief='raised',
                                           borderwidth=1,
                                           width=25,
                                           height=1,
                                           font=('orbitron', 15, 'bold'),
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
        elif len(semester_list) == 2:
            teacher1_button = tk.Button(self,
                                        text="Semester " + semester_list[0],
                                        command=lambda: assign_and_next_frame(semester_list[0]),
                                        relief='raised',
                                        borderwidth=1,
                                        width=25,
                                        height=1,
                                        font=('orbitron', 15, 'bold'),
                                        fg="#6666CC"
                                        )
            teacher1_button.pack(pady=10)

            teacher2_button = tk.Button(self,
                                        text="Semester " + semester_list[1],
                                        command=lambda: assign_and_next_frame(semester_list[1]),
                                        relief='raised',
                                        borderwidth=1,
                                        width=25,
                                        height=1,
                                        font=('orbitron', 15, 'bold'),
                                        fg="#6666CC"

                                        )
            teacher2_button.pack(pady=10)
        else:
            teacher1_button = tk.Button(self,
                                        text="Semester " + semester_list[0],
                                        command=lambda: assign_and_next_frame(semester_list[0]),
                                        relief='raised',
                                        borderwidth=1,
                                        width=25,
                                        height=1,
                                        font=('orbitron', 15, 'bold'),
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

        def get_image(url):
            imgPath = urllib.request.urlopen(url)
            imgNp = np.array(bytearray(imgPath.read()), dtype=np.uint8)
            img = cv2.imdecode(imgNp, -1)
            #img = imutils.resize(img, 400, 200)
            # img = cv2.resize(img, (268, 201))
            return img

        # un-comment if you use webcam
        #cap = cv2.VideoCapture(0)#url)

        #un-comment if you use android camera 
        cap = cv2.VideoCapture(url)

        def video_stream():
            _, frame = cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            # cv2image = cv2.rotate(cv2image, cv2.ROTATE_90_CLOCKWISE)
            # cv2image = get_image(url)
            cv2image = cv2.resize(cv2image, (268, 201)) # (200, 150))
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            label.imgtk = imgtk
            label.configure(image=imgtk)
            label.after(10, video_stream)
        
        video_stream()

        def assign_and_next_frame():
            global path_to_img
            img = cap.read()[1]
            cv2.imwrite('capture/capture.png', img)
            path_to_img = "capture/capture.png"
            os.system('python sys.py')
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
                ls = []
                for i in range(10):
                    ls.append(os.path.join("cropped", str(i) + '.jpg'))
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
        
        self.t1 = Thread(target=self.func)
        # self.t1.start()

        def assign_and_next_frame():
            global student_list
            student_list = getStudents(user_to_access_firebase, course_to_access_firebase, class_to_access_firebase, semester_to_access_firebase)
            print("hello")
            controller.show_frame('chooseStudentIDPage') # Next frame
        
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
    
    def func(self):
        global done
        while True:
            print(1)
            time.sleep(1)
            if done == True:
                for i in range(min(len(answer), len(answer_marking))):
                    if answer[i] == answer_marking[i]:
                        self.points_num += 1
                self.points.set('Result:\n' + str(self.points_num) + ' / ' + str(len(answer)))
                done = False
                global Student_point 
                Student_point = self.points_num
                print("end")
                # self.t1.join(2)
                break

    def trigger(self):
        self.t1 = Thread(target=self.func)
        self.points_num = 0
        self.t1.start()


class chooseStudentIDPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#00CC99')
        self.controller = controller

        self.controller.title('StudentID Selection')

        heading_label = tk.Label(self,
                                 text='Which Student \n You want to update?',
                                 font=('orbitron', 20, 'bold'),
                                 foreground='#ffffff',
                                 background='#00CC99'
                                 )
        heading_label.pack(pady=10)

        space_label = tk.Label(self, height=1, bg='#00CC99')
        space_label.pack()

        def assign_and_next_frame(student_id):
            UpdateStudentMark(user_to_access_firebase, course_to_access_firebase, class_to_access_firebase, semester_to_access_firebase, student_id, Student_point)
            controller.show_frame('chooseTeacherPage') 

        if len(student_list) > 2:
            canvas = tk.Canvas(self, bg='#00CC99')
            scroll_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview, bg='#00CC99', background='#00CC99')

            frame = tk.Frame(canvas, bg='#00CC99')
            # Add buttons
            lst_btn = []
            for i in range(len(student_list)):
                text_display = "Student " + student_list[i]
                teacher_button = tk.Button(frame,
                                           text=text_display,
                                           command=lambda j=student_list[i]: assign_and_next_frame(j),
                                           relief='raised',
                                           borderwidth=1,
                                           width=25,
                                           height=1,
                                           font=('orbitron', 15, 'bold'),
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
        elif len(student_list) == 2:
            teacher1_button = tk.Button(self,
                                        text="Student " + student_list[0],
                                        command=lambda: assign_and_next_frame(student_list[0]),
                                        relief='raised',
                                        borderwidth=1,
                                        width=25,
                                        height=1,
                                        font=('orbitron', 15, 'bold'),
                                        fg="#6666CC"
                                        )
            teacher1_button.pack(pady=10)

            teacher2_button = tk.Button(self,
                                        text="Student " + student_list[1],
                                        command=lambda: assign_and_next_frame(student_list[1]),
                                        relief='raised',
                                        borderwidth=1,
                                        width=25,
                                        height=1,
                                        font=('orbitron', 15, 'bold'),
                                        fg="#6666CC"

                                        )
            teacher2_button.pack(pady=10)
        else:
            teacher1_button = tk.Button(self,
                                        text="Student " + student_list[0],
                                        command=lambda: assign_and_next_frame(student_list[0]),
                                        relief='raised',
                                        borderwidth=1,
                                        width=25,
                                        height=1,
                                        font=('orbitron', 15, 'bold'),
                                        fg="#6666CC"
                                        )
            teacher1_button.pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.geometry('480x280')
    app.mainloop()
    print(user_to_access_firebase, path_to_img, answer_marking, done)
