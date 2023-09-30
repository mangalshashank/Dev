import cv2
from deepface import DeepFace

# Load img1
img1_path = 'img1.jpg'  # Replace with the actual path to img1.jpg

# Initialize the webcam capture
cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

# Capture a single frame from the webcam
ret, frame = cap.read()

# Check if the frame was captured successfully
if not ret:
    print("Error capturing frame")
else:
    # Save the captured frame as img2.jpg
    cv2.imwrite('img2.jpg', frame)

    # Perform verification using DeepFace
    result = DeepFace.verify(img1_path, 'img2.jpg')

    # Extract the verification result
    verified = result['verified']

    # Display the verification result
    if verified:
        print("Verification successful: The face in the webcam frame matches img1.jpg.")
    else:
        print("Verification failed: The face in the webcam frame does not match img1.jpg.")

# Release the webcam
cap.release()
