# Import database module.
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
"""----------------------------------------------------------------------------------------------------"""
# Select teacher, to retrieve answer and store the marking result on database
# Display format: Teacher Name - Teacher ID
# How to select, all teacher ID is store in dictionary: TeacherID - ID on Firestore
# TODO: Code with tktiner client

select_teacher = db.collection('TEACHER')
teachers = select_teacher.stream()

# id_list store id on firebase
# dict_list store dictionary of field of documents
id_list = []
dict_list = []

for teacher in teachers:
    id_list.append(teacher.id)
    dict_list.append(teacher.to_dict())

concat = []
for i in range(len(id_list)):
    concat.append(id_list[i] + ' - ' + dict_list[i]['T_Name'])
print(concat)
"""----------------------------------------------------------------------------------------------------"""
# Select subject, to retrieve the marking result on database
# Display format: Semester - Class - Name of subject
# All the informations are first query from the database and then upload into the client view
# Use dictionary with: Name of subject - answer
# TODO: Code with tktiner client

# Global variable
user_to_access_firebase = "101"

select_course = db.collection(
    'TEACHER').document(
        user_to_access_firebase).collection(
            'COURSE')
courses = select_course.stream()
course_list = []
for course in courses:
    course_list.append(course.id)
print(course_list)

# Global variable
course_to_access_firebase = course_list[0]

select_class = db.collection(
    'TEACHER').document(
        user_to_access_firebase).collection(
            'COURSE').document(
                course_to_access_firebase).collection(
                    'CLASS')
classes = select_class.stream()
class_list = []
for class_ in classes:
    class_list.append(class_.id)

# Global variable    
class_to_access_firebase = class_list[0]

answer_ref = db.collection(
    'TEACHER').document(
        user_to_access_firebase).collection(
            'COURSE').document(
                course_to_access_firebase).collection(
                    'CLASS').document(
                        class_to_access_firebase)




answer = answer_ref.get().to_dict()['AnswerFile']
print(answer)

# Upload to server
# Global variable
student_id = 'AAA'
point = 8

answer_ref.collection('STUDENT').document(student_id).set({'S_Point': point})
"""----------------------------------------------------------------------------------------------------"""
# Button start marking or cancel, start making will display a client with camera view
# TODO: Check how to apply hardware
# Display format: 2 button cancel and marking - hardware button or software
# TODO: Code with tktiner client

"""-------------------------------------------------HERE---------------------------------------------------""" 
# Camera view the paper # TODO check if can use cv2.blurry recognition - and setup the light for clearer view
# Display format: camera view the paper + button start (hardware or software)
# TODO: Code with tktiner client

"""----------------------------------------------------------------------------------------------------"""
# Crop the image into specific region, use model for each image region, the text get from the model
# will be append to a list a compare with the answer that is retrieve from database
# Display format: Text - loading - marking ...
# TODO: Code with tktiner client

"""----------------------------------------------------------------------------------------------------"""
# Display the marking result
# Display format: The numeric result of how many point that paper get. Button upload to server
# TODO: Code with tktiner client

"""----------------------------------------------------------------------------------------------------"""
# Button upload to server
# Display format: Loading ... --> new button, 
# mark next exam or quit, if marknext, return to the camera view for next marking event
# if quit, cancel client
# Create new document of the ID from recognition, upload with 10 answers of the student getting mark to the
# firebase server.
# TODO: Code with tktiner client - # TODO: Check coding a retrieve format, python query from firebase and export excel.
