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

select_teacher = db.collection('teacher')
teachers = select_teacher.stream()

# id_list store id on firebase
# dict_list store dictionary of field of documents
id_list = []
dict_list = []

for teacher in teachers:
    id_list.append(teacher.id)
    dict_list.append(teacher.to_dict())

# Flatten dictionary to string
concat = []
for i in dict_list:
    concat.append(i['name'] + ' - ' + i['id'])

# Create dictionary of string and id on firebase
# Demo: {'Tien - Teach1': 'KuUgdSdWGpTrVHloCphbw5YA8A62'}
select_firestore = dict(zip(concat, id_list))

"""----------------------------------------------------------------------------------------------------"""
# Select subject, to retrieve the marking result on database
# Display format: Semester - Class - Name of subject
# All the informations are first query from the database and then upload into the client view
# Use dictionary with: Name of subject - answer
# TODO: Code with tktiner client

# Global variable
user_to_access_firebase = "KuUgdSdWGpTrVHloCphbw5YA8A62"

select_course = db.collection('teacher').document(user_to_access_firebase).collection('course')
courses = select_course.stream()
course_list = []
for course in courses:
    course_list.append(course.id)

# Global variable
course_to_access_firebase = course_list[0]

answer_ref = db.collection('teacher').document(user_to_access_firebase).collection('course').document(course_to_access_firebase)

# To check with recognized answer
answer = answer_ref.get().to_dict()['answer']

print(answer)


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



"""----------------------------------------------------------------------------------------------------"""
# # # Get the ID of teacher
# # doc_ref = db.collection('teacher')
# # docs = doc_ref.stream()
# #
# # for doc in docs:
# #     print("{} => {}".format(doc.id, doc.to_dict()))

# id_ref = db.collection('teacher')
# ids = id_ref.stream()

# lst_id = []
# for id in ids:
#     lst_id.append(str(id.id))
#     # print("{} => {}".format(doc.id, doc.to_dict()))
# print(lst_id)

# doc1st_ref = db.collection('teacher').document(lst_id[0])
# # # Set value
# # doc1st_ref.set({
# #     'name': 'Viet'
# # })
# course = doc1st_ref.collection('course')
# courses = course.stream()

# for c in courses:
#     print("{} => {}".format(c.id, c.to_dict()))
