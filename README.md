# scroll-using-finger-
# Hand Gesture Browser Scroll

A Python project that uses a webcam to detect hand movement and scroll web pages up and down.

## Features

- Detects your hand using webcam
- Scrolls browser pages using hand movement
- Works when only **one finger (index finger)** is raised
- Scrolls **up and down** based on finger movement
- Only works when a **browser window is active**
- Smooth scrolling with motion filtering

## Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- PyGetWindow

## How It Works

1. The webcam captures your hand.
2. MediaPipe detects hand landmarks.
3. The system checks if only the **index finger** is raised.
4. When the browser is active, moving your finger:
   - **up** scrolls the page
   - **down** scrolls the page
5. Small random movements are filtered for smoother scrolling.

## Project Structure

```bash
HandScrollProject/
│── hand_scroll.py
│── README.md


Installation

1. Clone the repository
git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
2. Create a virtual environment
python -m venv venv
3. Activate the virtual environment
Windows
venv\Scripts\activate
4. Install dependencies
python -m pip install opencv-python pyautogui pygetwindow mediapipe==0.10.21
How to Run
python hand_scroll.py


How to Use


Run the program
Open a browser such as Chrome, Edge, or Firefox
Click once inside the webpage
Raise only your index finger
Move your hand:
Up to scroll the page
Down to scroll the page in the opposite direction
Press Q to quit the application


Configuration

You can change these values in hand_scroll.py:

REVERSE_SCROLL
Change scroll direction
MOVEMENT_THRESHOLD
Controls sensitivity
SCROLL_MULTIPLIER
Controls scroll speed
SCROLL_COOLDOWN
Controls how often scrolling happens
Example Settings
REVERSE_SCROLL = False
MOVEMENT_THRESHOLD = 0.006
SCROLL_MULTIPLIER = 3000
SCROLL_COOLDOWN = 0.05
Supported Browsers

This project checks whether the active window is a browser. Supported browser names include:

Chrome
Edge
Firefox
Brave
Opera
Requirements
Python 3.10 recommended
Windows
Webcam
Notes
Make sure your room has enough light for better hand detection
Keep your hand clearly visible to the camera
Click inside the browser page before testing scrolling
If scrolling direction feels wrong, set:
REVERSE_SCROLL = True
Future Improvements
Support any single finger
Start/stop gesture control
Better gesture recognition
Improved browser detection
GUI settings panel
Author

J.A.S. Bandara

License

This project is for educational purposes.