Reference video from 5th semester:

https://drive.google.com/file/d/1T9HixSUqCOv9UxJ9Ebt6YHaziS6sLzT-/view?usp=sharing

Final year Thesis Demo Video Link:

https://drive.google.com/file/d/1qXZYouS2zKmjx7nNb0kZugDblmP5ELJw/view?usp=sharing

Medical Waste Classification Using Computer Vision

This project uses Convolutional Neural Networks (CNN) to classify waste into two categories: Medical and Non-Medical. The AI-driven system, leveraging image processing techniques, is designed to improve hospital waste management efficiency. The solution has been tailored for low-resource environments like Nepal, where proper medical waste segregation is critical for public health and environmental sustainability.

Project Overview

The project automates waste classification using a CNN model to analyze images captured from a webcam. The model categorizes the waste as MEDICAL (syringes, gloves, masks, biomedical waste, etc.) or NON-MEDICAL (general waste such as food wrappers, paper, plastic, etc.) and sends control signals to an Arduino for appropriate action based on the classification.

Key Features

Real-time image capture using a webcam.

Zoom functionality to enhance captured image quality for classification.

Integration with Roboflow API for medical waste classification.

Serial communication with Arduino to control external devices based on waste type.

Robust retry mechanism for handling network-related issues.

Technologies Used

Python: The primary programming language for building the system.

OpenCV: For image processing and video capture.

Roboflow API: For classifying waste into Medical or Non-Medical categories.

Convolutional Neural Networks (CNN): Used for image-based waste classification.

Serial Communication: For interfacing with Arduino to send signals based on classification.

Matplotlib: For visualizing the live video feed.

Hardware Structure

The system includes the following hardware components:

1 × USB Camera – Used for capturing real-time waste images.

2 × Waste Bins – One for Medical waste and one for Non-Medical waste.

2 × Servo Motors (25 KG) – Responsible for moving and segregating waste into the appropriate bin.

1 × Arduino UNO Board – Central controller that receives classification signals and controls the motors.

1 × Buck Module (Step-Down) 5V – Converts voltage for powering the components.

1 × 12V Battery – Power source for the system.

Here is the hardware structure of the waste classification system:

<img width="4000" height="2250" alt="image" src="https://github.com/user-attachments/assets/b298ac75-2b9c-4a88-9af5-f86662c5f7e7" />


Project Flow

Capture an image from a webcam.

Apply zoom to the captured frame.

Save the image and send it to the Roboflow API for classification.

Based on the classification (Medical or Non-Medical), send appropriate signals to an Arduino.

Continuously update the counts for both categories and display them on the screen.

How it Works

The system captures an image of waste, processes it, and sends it to the Roboflow API using HTTP requests. The API returns predictions about the waste type (Medical or Non-Medical). The system then sends signals to an Arduino to perform different actions depending on the classification (e.g., moving a flap/servo to direct the waste into the correct bin). The counts for each type of waste are updated and displayed in real-time.
