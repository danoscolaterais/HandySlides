# HandySlides 🙋‍♂️

<div align="center">
   <img width="600" height="600" alt="HandySlides Demo" src="https://github.com/user-attachments/assets/233ca1a9-8bef-4a36-905e-14888efd4e9c" />
</div>

<div align="center">
   
![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey)

</div>

> Control your presentations with simple arm gestures using computer vision!

## ✨ Features

- 🎯 **Intuitive arm gesture control** - Raise your arm to navigate slides
- ⚙️ **Easy-to-use configuration window** - Customize gestures without code
- 🌍 **Multi-language support** - Interface in Portuguese, English, and French
- 📹 **Real-time camera preview** - See gesture detection in action
- 🔧 **Adjustable sensitivity and cooldown** - Fine-tune for your presentation style
- 🎨 **Mirror camera option** - Natural interaction experience
- 🎹 **Flexible key mapping** - Choose between arrow keys or Page Up/Down

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/danoscolaterais/HandySlides.git
   cd HandySlides
   ```

2. **Install required dependencies:**
   ```bash
   pip install opencv-python mediapipe pyautogui
   ```

3. **Connect your webcam** and ensure it's working.

4. **Run the application:**
   ```bash
   python HandySlides.py
   ```

5. **Configure your preferences** in the setup window and click "Start"!

## 📸 Interface Preview

<div align="center">
   <img width="564" height="579" alt="HandySlides Configuration Interface" src="https://github.com/user-attachments/assets/6b9ca4af-f1fa-40bd-81ba-212b4b0d297c" />
   <p><em>Easy-to-use configuration interface with multi-language support</em></p>
</div>

## 🎯 Use Cases

- 📊 **Interactive presentations** - Engage your audience hands-free
- 👩‍🏫 **Teaching scenarios** - Keep focus on students, not slides
- 🏠 **Remote presentations** - Professional control from anywhere
- ♿ **Accessibility tool** - Alternative for users with mobility limitations
- 🎭 **Performance art** - Creative integration in artistic presentations

## ⚙️ How It Works

**By default:**
- **Right Arm Raised** → Next slide (right arrow key)
- **Left Arm Raised** → Previous slide (left arrow key)

The application uses **MediaPipe** for pose detection and **OpenCV** for camera input. When your wrist rises above your shoulder, **PyAutoGUI** simulates the appropriate keypress.

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Camera not detected** | Ensure no other apps are using the webcam |
| **Gestures not responding** | Adjust sensitivity in configuration window |
| **Poor detection** | Ensure good lighting and clear background |
| **Wrong gesture direction** | Use mirror camera option for natural interaction |
| **Too sensitive** | Increase cooldown time in advanced settings |

## 🛠️ System Requirements

- **Python 3.7+**
- **Webcam** (built-in or external)
- **Operating System**: Windows, macOS, or Linux
- **Dependencies**: OpenCV, MediaPipe, PyAutoGUI

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe** team for the excellent pose detection library
- **OpenCV** community for computer vision tools
- Original inspiration from gesture control research

---

<div align="center">
   <p>Made with ❤️ for better presentations</p>
   <p>⭐ Star this repo if you found it helpful!</p>
</div>
