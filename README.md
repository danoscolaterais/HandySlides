# Hand Gesture Control for PowerPoint Slides

This Python project uses OpenCV and MediaPipe to control PowerPoint presentations through hand gestures. By clenching your left or right arms, you can navigate between slides. The project detects arm gestures in real-time using a webcam and simulates key presses on the keyboard (left or right arrow) to move between slides.

## Features:
- **Right Arm Gesture:** When the right arm is clenched, the "right arrow" key is pressed, moving to the next slide.
- **Left Arm Gesture:** When the left arm is clenched, the "left arrow" key is pressed, moving to the previous slide.
- Real-time hand gesture detection using MediaPipe's hand landmark model.
- Uses OpenCV to capture video feed and detect gestures.
- Simulates keypresses with the `pyautogui` library.

## Installation:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/hand-gesture-control.git
   ```

2. Install required dependencies:
   ```bash
   pip install opencv-python mediapipe pyautogui
   ```

3. Connect your webcam and ensure it's working.

## Usage:

1. Run the Python script:
   ```bash
   python hand_gesture_control.py
   ```

2. The webcam feed will appear. Raise your right or left arm and clench your fist to move through your PowerPoint slides.

3. To exit, press `q` on your keyboard.

## Notes:
- The script assumes your webcam is connected and functional.
- You might need to adjust the conditions for detecting clenched arms based on your fist positioning.

## Contributing:
Feel free to open an issue or submit a pull request if you'd like to contribute or suggest improvements!

## License:
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

You can customize this further to suit your project!
