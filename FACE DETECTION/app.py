import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os
import pickle
from pathlib import Path
from deepface import DeepFace
from ultralytics import YOLO
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Face Detection & Recognition System",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'teammate_encodings' not in st.session_state:
    st.session_state.teammate_encodings = {}
if 'teammate_images' not in st.session_state:
    st.session_state.teammate_images = {}

# Constants
TEAMMATES_FOLDER = "teammates_profiles"
ENCODINGS_CACHE = "encodings_cache.pkl"
CONFIDENCE_THRESHOLD = 0.6
FACE_MATCH_THRESHOLD = 0.6

# Create teammates folder if it doesn't exist
os.makedirs(TEAMMATES_FOLDER, exist_ok=True)


def load_yolo_model():
    """Load YOLO model for object detection"""
    try:
        model = YOLO('yolov8n.pt')  # Using YOLOv8 nano for speed
        return model
    except Exception as e:
        st.error(f"Error loading YOLO model: {e}")
        return None


def load_face_cascade():
    """Load Haar Cascade for face detection"""
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    return face_cascade


def load_or_create_teammate_encodings():
    """Load teammate face embeddings from cache or create new ones"""
    
    # Try to load from cache
    if os.path.exists(ENCODINGS_CACHE):
        try:
            with open(ENCODINGS_CACHE, 'rb') as f:
                cache_data = pickle.load(f)
                st.session_state.teammate_encodings = cache_data['encodings']
                st.session_state.teammate_images = cache_data['images']
                return
        except Exception as e:
            st.warning(f"Could not load cache: {e}. Rebuilding...")
    
    # Build encodings from scratch
    encodings = {}
    images = {}
    
    if not os.path.exists(TEAMMATES_FOLDER) or not os.listdir(TEAMMATES_FOLDER):
        st.info(f"📁 No teammate profiles found. Add images to '{TEAMMATES_FOLDER}' folder.")
        return
    
    with st.spinner("Loading teammate profiles..."):
        for filename in os.listdir(TEAMMATES_FOLDER):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(TEAMMATES_FOLDER, filename)
                try:
                    # Load image
                    image = cv2.imread(filepath)
                    if image is None:
                        st.warning(f"Could not load {filename}")
                        continue
                    
                    # Convert BGR to RGB
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    # Extract face embedding using DeepFace
                    try:
                        embedding = DeepFace.represent(
                            img_path=filepath,
                            model_name="Facenet",
                            enforce_detection=True,
                            detector_backend="opencv"
                        )
                        
                        if embedding and len(embedding) > 0:
                            # Use filename (without extension) as name
                            name = os.path.splitext(filename)[0]
                            encodings[name] = embedding[0]['embedding']
                            images[name] = image_rgb
                        else:
                            st.warning(f"No face detected in {filename}")
                    except Exception as e:
                        st.warning(f"No clear face detected in {filename}")
                        
                except Exception as e:
                    st.error(f"Error processing {filename}: {e}")
    
    # Save to cache
    if encodings:
        try:
            with open(ENCODINGS_CACHE, 'wb') as f:
                pickle.dump({'encodings': encodings, 'images': images}, f)
            st.success(f"✅ Loaded {len(encodings)} teammate profiles")
        except Exception as e:
            st.warning(f"Could not save cache: {e}")
    
    st.session_state.teammate_encodings = encodings
    st.session_state.teammate_images = images


def detect_objects_yolo(image, model):
    """Detect objects using YOLO and classify human faces"""
    results = model(image, conf=CONFIDENCE_THRESHOLD)
    
    # Convert to BGR for OpenCV
    img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    detections = []
    
    for result in results:
        boxes = result.boxes
        for box in boxes:
            # Get coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            
            # Check if it's a person (class_id 0 in COCO dataset)
            if class_id == 0:
                # Try to detect if there's a face in the person bounding box
                roi = img_bgr[y1:y2, x1:x2]
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                face_cascade = load_face_cascade()
                faces = face_cascade.detectMultiScale(gray_roi, 1.1, 4)
                
                if len(faces) > 0:
                    label = "Human Face"
                    color = (0, 255, 0)  # Green for faces
                else:
                    label = "Person (No face visible)"
                    color = (255, 165, 0)  # Orange
            else:
                label = class_name
                color = (0, 0, 255)  # Red for objects
            
            detections.append({
                'bbox': (x1, y1, x2, y2),
                'label': label,
                'confidence': confidence,
                'color': color
            })
    
    return detections


def detect_and_recognize_faces(image):
    """Detect faces and match against teammate profiles using DeepFace"""
    # Convert PIL to array
    img_array = np.array(image)
    
    # Detect faces using DeepFace
    try:
        # Save temp image for DeepFace processing
        temp_path = "temp_input.jpg"
        cv2.imwrite(temp_path, cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR))
        
        # Detect faces and extract embeddings
        detected_faces = DeepFace.extract_faces(
            img_path=temp_path,
            detector_backend="opencv",
            enforce_detection=False
        )
        
        matches = []
        
        for face_obj in detected_faces:
            if face_obj['confidence'] < 0.9:  # Skip low confidence detections
                continue
                
            # Get face location
            facial_area = face_obj['facial_area']
            x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
            left, top, right, bottom = x, y, x + w, y + h
            
            name = "Unknown Person"
            confidence = 0.0
            matched_image = None
            
            # Extract embedding for this face
            try:
                face_img = img_array[max(0, y):min(img_array.shape[0], y+h), 
                                    max(0, x):min(img_array.shape[1], x+w)]
                
                # Save face crop temporarily
                temp_face_path = "temp_face.jpg"
                cv2.imwrite(temp_face_path, cv2.cvtColor(face_img, cv2.COLOR_RGB2BGR))
                
                face_embedding_result = DeepFace.represent(
                    img_path=temp_face_path,
                    model_name="Facenet",
                    enforce_detection=False,
                    detector_backend="opencv"
                )
                
                if face_embedding_result and len(face_embedding_result) > 0:
                    face_embedding = face_embedding_result[0]['embedding']
                    
                    # Compare with teammate encodings
                    if st.session_state.teammate_encodings:
                        for teammate_name, teammate_encoding in st.session_state.teammate_encodings.items():
                            # Calculate cosine similarity
                            similarity = calculate_cosine_similarity(face_embedding, teammate_encoding)
                            
                            # Convert to 0-1 range (cosine similarity is -1 to 1)
                            normalized_similarity = (similarity + 1) / 2
                            
                            if normalized_similarity > FACE_MATCH_THRESHOLD and normalized_similarity > confidence:
                                name = teammate_name
                                confidence = normalized_similarity
                                matched_image = st.session_state.teammate_images.get(teammate_name)
                
                # Clean up temp files
                if os.path.exists(temp_face_path):
                    os.remove(temp_face_path)
                    
            except Exception as e:
                pass  # Face too small or unclear
            
            matches.append({
                'bbox': (left, top, right, bottom),
                'name': name,
                'confidence': confidence,
                'matched_image': matched_image
            })
        
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
    except Exception as e:
        st.warning(f"Face detection error: {e}")
        matches = []
    
    return matches


def calculate_cosine_similarity(embedding1, embedding2):
    """Calculate cosine similarity between two embeddings"""
    embedding1 = np.array(embedding1)
    embedding2 = np.array(embedding2)
    
    # Normalize vectors
    embedding1_norm = embedding1 / np.linalg.norm(embedding1)
    embedding2_norm = embedding2 / np.linalg.norm(embedding2)
    
    # Calculate cosine similarity
    similarity = np.dot(embedding1_norm, embedding2_norm)
    
    return similarity


def draw_detections_objects(image, detections):
    """Draw bounding boxes and labels for object detection"""
    img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        label = det['label']
        confidence = det['confidence']
        color = det['color']
        
        # Draw rectangle
        cv2.rectangle(img_bgr, (x1, y1), (x2, y2), color, 2)
        
        # Draw label background
        label_text = f"{label} ({confidence:.2f})"
        (text_width, text_height), baseline = cv2.getTextSize(
            label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        cv2.rectangle(img_bgr, (x1, y1 - text_height - 10), 
                     (x1 + text_width, y1), color, -1)
        
        # Draw label text
        cv2.putText(img_bgr, label_text, (x1, y1 - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def draw_face_matches(image, matches):
    """Draw bounding boxes and labels for face recognition"""
    img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    for match in matches:
        left, top, right, bottom = match['bbox']
        name = match['name']
        confidence = match['confidence']
        
        # Color based on match
        if name == "Unknown Person":
            color = (0, 0, 255)  # Red
        else:
            color = (0, 255, 0)  # Green
        
        # Draw rectangle
        cv2.rectangle(img_bgr, (left, top), (right, bottom), color, 2)
        
        # Draw label background
        if confidence > 0:
            label_text = f"{name} ({confidence:.2%})"
        else:
            label_text = name
            
        (text_width, text_height), baseline = cv2.getTextSize(
            label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        cv2.rectangle(img_bgr, (left, top - text_height - 10),
                     (left + text_width, top), color, -1)
        
        # Draw label text
        cv2.putText(img_bgr, label_text, (left, top - 5),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def main():
    # Header
    st.title("👤 Real-Time Face Detection & Recognition System")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Mode selection
        mode = st.radio(
            "Select Mode:",
            ["Object Detection Mode", "Face Recognition Mode"],
            help="Choose between object detection or face recognition"
        )
        
        st.markdown("---")
        
        # Input method
        input_method = st.radio(
            "Input Method:",
            ["Upload Image", "Webcam Capture"],
            help="Choose how to provide input"
        )
        
        st.markdown("---")
        
        # Configuration
        st.subheader("📊 Configuration")
        
        global CONFIDENCE_THRESHOLD, FACE_MATCH_THRESHOLD
        
        if mode == "Object Detection Mode":
            CONFIDENCE_THRESHOLD = st.slider(
                "Detection Confidence",
                0.1, 1.0, 0.6, 0.05,
                help="Minimum confidence for object detection"
            )
        else:
            FACE_MATCH_THRESHOLD = st.slider(
                "Face Match Threshold",
                0.1, 1.0, 0.6, 0.05,
                help="Minimum similarity for face recognition"
            )
        
        st.markdown("---")
        
        # Info section
        if mode == "Face Recognition Mode":
            st.subheader("👥 Teammate Profiles")
            if st.button("🔄 Reload Profiles"):
                if os.path.exists(ENCODINGS_CACHE):
                    os.remove(ENCODINGS_CACHE)
                st.session_state.teammate_encodings = {}
                st.session_state.teammate_images = {}
                load_or_create_teammate_encodings()
                st.rerun()
            
            profiles_count = len(st.session_state.teammate_encodings)
            st.metric("Loaded Profiles", profiles_count)
            
            if profiles_count > 0:
                st.success("✅ Profiles loaded")
                with st.expander("View Teammates"):
                    for name in st.session_state.teammate_encodings.keys():
                        st.text(f"• {name}")
            else:
                st.info(f"📁 Add images to `{TEAMMATES_FOLDER}` folder")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📥 Input")
        
        input_image = None
        
        if input_method == "Upload Image":
            uploaded_file = st.file_uploader(
                "Choose an image",
                type=['jpg', 'jpeg', 'png'],
                help="Upload an image for processing"
            )
            
            if uploaded_file is not None:
                input_image = Image.open(uploaded_file)
                st.image(input_image, caption="Uploaded Image", use_container_width=True)
        
        else:  # Webcam Capture
            camera_photo = st.camera_input("Take a picture")
            
            if camera_photo is not None:
                input_image = Image.open(camera_photo)
                st.image(input_image, caption="Captured Image", use_container_width=True)
    
    with col2:
        st.subheader("📤 Output")
        
        if input_image is not None:
            with st.spinner("Processing..."):
                if mode == "Object Detection Mode":
                    # Object Detection
                    yolo_model = load_yolo_model()
                    
                    if yolo_model:
                        detections = detect_objects_yolo(input_image, yolo_model)
                        
                        if detections:
                            result_image = draw_detections_objects(input_image, detections)
                            st.image(result_image, caption="Detection Results", use_container_width=True)
                            
                            # Display detection stats
                            st.markdown("### 📊 Detection Results")
                            for i, det in enumerate(detections, 1):
                                st.write(f"**{i}.** {det['label']} - Confidence: {det['confidence']:.2%}")
                        else:
                            st.info("No objects detected")
                            st.image(input_image, use_container_width=True)
                
                else:  # Face Recognition Mode
                    # Load teammate profiles if not loaded
                    if not st.session_state.teammate_encodings:
                        load_or_create_teammate_encodings()
                    
                    # Face Recognition
                    matches = detect_and_recognize_faces(input_image)
                    
                    if matches:
                        result_image = draw_face_matches(input_image, matches)
                        st.image(result_image, caption="Recognition Results", use_container_width=True)
                        
                        # Display match details
                        st.markdown("### 👤 Recognition Results")
                        
                        for i, match in enumerate(matches, 1):
                            with st.container():
                                if match['name'] != "Unknown Person":
                                    col_a, col_b = st.columns([1, 2])
                                    with col_a:
                                        if match['matched_image'] is not None:
                                            st.image(
                                                match['matched_image'],
                                                caption=match['name'],
                                                width=150
                                            )
                                    with col_b:
                                        st.write(f"**Name:** {match['name']}")
                                        st.write(f"**Confidence:** {match['confidence']:.2%}")
                                        st.success("✅ Match Found")
                                else:
                                    st.write(f"**{i}.** Unknown Person")
                                    st.warning("⚠️ No Match Found")
                                
                                st.markdown("---")
                    else:
                        st.info("No faces detected in the image")
                        st.image(input_image, use_container_width=True)
        else:
            st.info("👆 Please provide an input image using the left panel")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray;'>
        <p>Face Detection & Recognition System | Built with Streamlit, OpenCV, and YOLO</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()