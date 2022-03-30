# Import database module.
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
# # Select subject, to retrieve the marking result on database
# # Display format: Semester - Class - Name of subject
# # All the informations are first query from the database and then upload into the client view
# # Use dictionary with: Name of subject - answer
# # TODO: Code with tktiner client

# # Global variable
user_to_access_firebase = "2053373"


def getCourses(teacher_id):
    select_course = db.collection(
        'Sample_Teacher').document(
            teacher_id).collection(
                'COURSE')
    courses = select_course.stream()

    course_list = reduce(lambda acc, ele: acc + [ele.id], courses, [])
    # print(course_list)
    return course_list


course_list = getCourses(user_to_access_firebase);
print(course_list)


# # Global variable
course_to_access_firebase = course_list[1]

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

class_list = getClasses(user_to_access_firebase, course_to_access_firebase);

print(class_list)

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
print(semester_list)


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
print(answer)

# # Upload to server
# # Global variable
# student_id = 'AAA'
# point = 8

# answer_ref.collection('STUDENT').document(student_id).set({'S_Point': point})
# """----------------------------------------------------------------------------------------------------"""
# # Button start marking or cancel, start making will display a client with camera view
# # TODO: Check how to apply hardware
# # Display format: 2 button cancel and marking - hardware button or software
# # TODO: Code with tktiner client

# """-------------------------------------------------HERE---------------------------------------------------""" 
# # Camera view the paper # TODO check if can use cv2.blurry recognition - and setup the light for clearer view
# # Display format: camera view the paper + button start (hardware or software)
# # TODO: Code with tktiner client

# """----------------------------------------------------------------------------------------------------"""
# # Crop the image into specific region, use model for each image region, the text get from the model
# # will be append to a list a compare with the answer that is retrieve from database
# # Display format: Text - loading - marking ...
# # TODO: Code with tktiner client

# """----------------------------------------------------------------------------------------------------"""
# # Display the marking result
# # Display format: The numeric result of how many point that paper get. Button upload to server
# # TODO: Code with tktiner client

# """----------------------------------------------------------------------------------------------------"""
# # Button upload to server
# # Display format: Loading ... --> new button, 
# # mark next exam or quit, if marknext, return to the camera view for next marking event
# # if quit, cancel client
# # Create new document of the ID from recognition, upload with 10 answers of the student getting mark to the
# # firebase server.
# # TODO: Code with tktiner client - # TODO: Check coding a retrieve format, python query from firebase and export excel.
