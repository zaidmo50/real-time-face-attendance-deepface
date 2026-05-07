import cv2
import os
import numpy as np
from PIL import Image
from tkinter import messagebox
from deepface import DeepFace
from mtcnn import MTCNN
from tkinter import *
from tkinter import simpledialog, messagebox,Tk

# Function to create faces folder if it doesn't exist
def create_faces_folder():
    faces_dir = 'faces'
    if not os.path.exists(faces_dir):
        os.makedirs(faces_dir)
    return faces_dir

  

# Function to capture and register a new user's face
def register_user(user_name):
    # Open webcam for face capture
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Initialize Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    faces_dir = create_faces_folder()

    count = 0  # To keep track of number of images captured

    print(f"Starting face registration for {user_name}. Press 's' to save an image or 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Convert frame to grayscale for face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

        # Draw rectangle around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            face_img = frame[y:y + h, x:x + w]
            face_resized = cv2.resize(face_img, (160, 160))  # Resize to 160x160 for Facenet

        # Display the frame with rectangles
        cv2.imshow('Registering - Press "s" to save, "q" to quit', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and len(faces) > 0:
            # Save the captured face image
            count += 1
            file_path = os.path.join(faces_dir, f'{user_name}_{count}.jpg')
            cv2.imwrite(file_path, face_resized)
            print(f"Image saved for {user_name} at {file_path}")
        
            embeddings = recognize_face_cnn(face_resized)

            if embeddings is not None:
                save_embeddings(user_name, embeddings)
                
                messagebox.showinfo("Success", f"Image {count} saved and embeddings stored for {user_name}.")
            else:
                messagebox.showwarning("Error", "Failed to extract embeddings.")

 
            break         

        elif key == ord('q'):
            print("Registration cancelled by user.")
            messagebox.showwarning("Cancelled", "Face registration cancelled.")
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

#embeddings
def recognize_face_cnn(face_img):
    try:
        # Convert face image to grayscale and apply FFT preprocessing
        gray_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        f_transform = np.fft.fft2(gray_img)
        f_transform = np.fft.fftshift(f_transform)
        
        # Apply a low pass filter for smoothing
        rows, cols = gray_img.shape
        crow, ccol = rows // 2, cols // 2
        radius = 30
        mask = np.zeros((rows, cols), np.uint8)
        cv2.circle(mask, (ccol, crow), radius, 1, thickness=-1)
        f_transform *= mask
        
        # Inverse FFT to reconstruct filtered image
        f_ishift = np.fft.ifftshift(f_transform)
        filtered_img = np.abs(np.fft.ifft2(f_ishift)).astype(np.uint8)
        
        # Save processed face image temporarily to disk for DeepFace
        temp_face_path = 'temp_filtered_face.jpg'
        cv2.imwrite(temp_face_path, filtered_img)

        # Get face embeddings from the processed image path
        embedding_obj = DeepFace.represent(
            img_path=temp_face_path,
            model_name="Facenet",
            enforce_detection=False,
            detector_backend='mtcnn'
        )

        # Remove the temporary image file
        os.remove(temp_face_path)

        # Extract embedding if available
        if embedding_obj and isinstance(embedding_obj, list):
            input_embedding = embedding_obj[0]['embedding']
            return np.array(input_embedding)
        
        return None
    except Exception as e:
        print(f"Error in recognize_face_cnn: {e}")
        return None

def save_embeddings(user_name, embeddings):
    embeddings_file = 'embeddings.csv'
    with open(embeddings_file, 'a') as f:
        f.write(f"{user_name},{','.join(map(str, embeddings))}\n")





# Function to capture user name and initiate registration
def capture_user_name():
   
    root = Tk()
    root.withdraw()  # Hide the main window

    # Ask the user for their name using a dialog box
    user_name = simpledialog.askstring("Input", "Enter your name:", parent=root)

    if user_name:
        # Start the face registration process
        register_user(user_name)
    else:
        messagebox.showwarning("Input Error", "Name cannot be empty.")
    root.quit()
    root.destroy()


capture_user_name()


