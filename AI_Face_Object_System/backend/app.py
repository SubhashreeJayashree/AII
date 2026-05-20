import streamlit as st
import cv2
import numpy as np

from face_module import recognize_face
from mask_module import detect_mask
from object_module import detect_objects


st.set_page_config(page_title="AI Face, Mask & Object Detection")

st.title("AI Face, Mask & Object Detection System")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    # Read image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if frame is None:
        st.error("Invalid image file")
    else:
        st.image(frame, channels="BGR", caption="Uploaded Image")

        with st.spinner("Processing..."):
            faces = recognize_face(frame)
            masks = detect_mask(frame)
            objects = detect_objects(frame)

        st.success("Detection completed")

        # ---------------- FACES ----------------
        st.subheader("Faces Detected")
        if faces:
            for t, r, b, l, name in faces:
                st.write(f"👤 **{name}** | Box: Left={l}, Top={t}, Right={r}, Bottom={b}")
        else:
            st.write("No faces detected")

        # ---------------- MASKS ----------------
        st.subheader("Mask Detection")
        if masks:
            for m in masks:
                st.write(f"😷 Mask Status: **{m[4]}**")
        else:
            st.write("No mask data")

        # ---------------- OBJECTS ----------------
        st.subheader("Objects Detected")
        if objects:
            for obj in objects:
                st.write(f"📦 {obj}")
        else:
            st.write("No objects detected")
