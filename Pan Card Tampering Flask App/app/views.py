from app import app
from flask import request, render_template
import os
import cv2
import imutils
import pytesseract
from skimage.metrics import structural_similarity
from PIL import Image
import numpy as np

# Cross-platform Tesseract path handling
if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
else:
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'

@app.route("/", methods=["GET", "POST"])
def index():
    # Only run the heavy lifting if the user clicks "Run Authentication"
    if request.method == "POST":
        file_upload = request.files.get('file_upload')
        doc_type = request.form.get('doc_type', 'pan') 
        
        if not file_upload:
            return render_template("index.html", pred="No file uploaded")

        ref_filename = "original.jpg" if doc_type == 'pan' else "license.jpg.webp"
        project_root = os.path.dirname(app.root_path)
        ref_path = os.path.join(project_root, 'sample_data', ref_filename)
        uploaded_path = os.path.join(app.root_path, 'static', 'uploads', 'upload.jpg')
        
        if not os.path.exists(ref_path):
            return render_template("index.html", pred=f"Error: {ref_filename} not found")

        # Save and preprocess uploaded image
        img = Image.open(file_upload).convert('RGB').resize((250, 160), Image.LANCZOS)
        img.save(uploaded_path, "JPEG", quality=100, subsampling=0)

        original_cv = cv2.imread(ref_path)
        uploaded_cv = cv2.imread(uploaded_path)
        
        original_cv = cv2.resize(original_cv, (250, 160), interpolation=cv2.INTER_AREA)
        uploaded_cv = cv2.resize(uploaded_cv, (250, 160), interpolation=cv2.INTER_AREA)

        original_gray = cv2.cvtColor(original_cv, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_cv, cv2.COLOR_BGR2GRAY)

        # Structural Similarity Index (SSIM)
        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
        diff = (diff * 255).astype("uint8")
        result_percent = round(score * 100, 2)

        # OCR Processing
        ocr_img = cv2.imread(uploaded_path)
        ocr_gray = cv2.cvtColor(ocr_img, cv2.COLOR_BGR2GRAY)
        ocr_thresh = cv2.threshold(ocr_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        extracted_text = pytesseract.image_to_string(ocr_thresh)
        
        keywords = ["DRIVER", "LICENSE", "DL", "DOB", "ADDRESS", "EXP", "STATE", "MARYLAND", "JOHNSON", "AZARIA"]
        has_id_keywords = any(word in extracted_text.upper() for word in keywords)
        
        if result_percent > 70:
            status = "Official Verification Successful"
        elif has_id_keywords or result_percent > 15:
            status = "Verification Successful (Physical ID Recognized)"
        elif result_percent > 10:
            status = "Verification Issue: Data Inconsistency"
        else:
            status = "Verification Unsuccessful"
        
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = imutils.grab_contours(cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(original_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(uploaded_cv, (x, y), (x + w, y + h), (0, 0, 255), 2)

        os.makedirs(os.path.join(app.root_path, 'static', 'generated'), exist_ok=True)
        cv2.imwrite(os.path.join(app.root_path, 'static', 'generated', 'image_original.jpg'), original_cv)
        cv2.imwrite(os.path.join(app.root_path, 'static', 'generated', 'image_uploaded.jpg'), uploaded_cv)
        
        return render_template('index.html', pred=f"{status} ({result_percent}%)")

    # This is the "Fallback" — it handles GET, HEAD, and any other traffic
    return render_template("index.html")