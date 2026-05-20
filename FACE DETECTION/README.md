# Face Detection & Recognition System

## 🎯 Overview
A production-ready Streamlit application for real-time face detection and recognition with two operational modes:

1. **Object Detection Mode**: Detects and classifies human faces vs. non-human objects
2. **Face Recognition Mode**: Matches detected faces against a cached database of teammate profiles

## 🚀 Features

### Object Detection Mode
- Detects objects in images using YOLOv8
- Identifies human faces specifically
- Labels non-human objects (pen, phone, cup, etc.)
- Displays confidence scores and bounding boxes
- Color-coded detection (Green: Faces, Red: Objects)

### Face Recognition Mode
- Detects faces and matches against teammate profiles
- Displays matched teammate names and profile pictures
- Shows confidence scores for matches
- Handles unknown persons gracefully
- Caches encodings for fast performance

### General Features
- **Dual Input Methods**: Upload images or use webcam capture
- **Real-time Processing**: Fast detection and recognition
- **Interactive UI**: Clean Streamlit interface with sidebar controls
- **Adjustable Thresholds**: Configure confidence levels
- **Profile Management**: Easy reload and update of teammate profiles

## 📦 Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. For face_recognition library, you may need to install CMake and dlib:
```bash
# On Windows
pip install cmake
pip install dlib

# On Linux
sudo apt-get install cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

## 🎮 Usage

1. **Run the application**:
```bash
streamlit run app.py
```

2. **Add Teammate Profiles** (for Face Recognition Mode):
   - Add images to the `teammates_profiles` folder
   - Name files as: `PersonName.jpg` (e.g., `John_Doe.jpg`, `Jane_Smith.jpg`)
   - Ensure each image contains a clear, frontal face
   - Click "🔄 Reload Profiles" in the sidebar to load new profiles

3. **Select Mode**:
   - Choose "Object Detection Mode" or "Face Recognition Mode" from the sidebar
   - Select input method: "Upload Image" or "Webcam Capture"
   - Adjust confidence thresholds as needed

4. **Process Images**:
   - Upload an image or capture from webcam
   - View detection/recognition results in real-time
   - Check confidence scores and match details

## 📁 Project Structure

```
face_detection/
├── app.py                      # Main application
├── requirements.txt            # Dependencies
├── teammates_profiles/         # Teammate profile images folder
│   ├── John_Doe.jpg
│   ├── Jane_Smith.jpg
│   └── ...
├── encodings_cache.pkl         # Cached face encodings (auto-generated)
└── README.md                   # This file
```

## 🛠️ Technical Details

### Models Used
- **YOLOv8**: For object detection (yolov8n.pt - nano version for speed)
- **face_recognition**: For face encoding and matching
- **OpenCV Haar Cascades**: For supplementary face detection
- **dlib**: Backend for face_recognition library

### Key Parameters
- **CONFIDENCE_THRESHOLD**: 0.6 (adjustable via sidebar)
- **FACE_MATCH_THRESHOLD**: 0.6 (adjustable via sidebar)

### Image Formats Supported
- JPG/JPEG
- PNG

## 🔧 Configuration

### Adjusting Detection Sensitivity
- Use the sidebar sliders to adjust confidence thresholds
- Lower values = more detections (may include false positives)
- Higher values = fewer detections (more conservative)

### Optimizing Performance
- Use smaller image resolutions for faster processing
- The YOLOv8 nano model is optimized for speed
- Face encodings are cached for faster subsequent loads

## 📊 Example Use Cases

1. **Security & Access Control**: Identify authorized personnel
2. **Attendance System**: Track team member presence
3. **Event Management**: Recognize registered attendees
4. **Smart Workplace**: Personalized workspace experiences
5. **Object Detection**: Identify prohibited items or specific objects

## ⚠️ Troubleshooting

### Common Issues

**Issue**: "No face detected" in teammate profiles
- **Solution**: Ensure images contain clear, frontal faces with good lighting

**Issue**: face_recognition installation fails
- **Solution**: Install CMake and dlib first (see Installation section)

**Issue**: Slow performance
- **Solution**: Reduce image resolution or use a smaller model

**Issue**: YOLO model download fails
- **Solution**: Check internet connection; YOLOv8 downloads on first run

**Issue**: "Unknown Person" for known teammates
- **Solution**: Lower the face match threshold or use better quality profile images

## 🎨 Customization

### Adding New Models
You can replace YOLOv8 with other models:
```python
model = YOLO('yolov8s.pt')  # Small model
model = YOLO('yolov8m.pt')  # Medium model
```

### Changing Detection Colors
Modify the color tuples in the code:
```python
color = (0, 255, 0)  # BGR format - Green
color = (255, 0, 0)  # Blue
color = (0, 0, 255)  # Red
```

## 📝 License
This project is for educational and internal use.

## 👥 Contributing
To add your profile:
1. Take a clear, frontal face photo with good lighting
2. Save as `YourName.jpg` in `teammates_profiles/` folder
3. Click "🔄 Reload Profiles" in the app

## 🔐 Privacy & Security
- All processing is done locally
- No data is sent to external servers
- Profile images are stored locally only
- Face encodings are cached locally for performance

## 📞 Support
For issues or questions, please refer to the documentation or contact the development team.

---

**Built with**: Python, Streamlit, OpenCV, YOLOv8, face_recognition
**Last Updated**: January 2026