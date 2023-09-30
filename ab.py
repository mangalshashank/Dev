import face_recognition
import os

def face_encoding(image_path):
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    if len(face_encoding) == 0:
        return None
    return face_encoding

registered_faces = []

for filename in os.listdir('registered_users'):
    image_path = f"registered_users/{filename}"
    registered_faces.append(face_encoding(image_path))

x = face_encoding("img2.jpg")
result = face_recognition.compare_faces(registered_faces, x, tolerance=0.6)  # Adjust tolerance as needed

print(result)