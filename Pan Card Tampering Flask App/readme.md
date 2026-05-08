Project Link: https://id-validation-6pwz.onrender.com/

Project Overview

Azaria Scan is a high-precision Flask application designed to verify the authenticity of identity documents, specifically PAN cards and Driver's Licenses. By combining Structural Similarity Index (SSIM) and OCR keyword validation, the system can distinguish between authentic documents, modified files, and non-standard physical ID photos. Tech Stack:

Python 3.x Flask OpenCV Tesseract OCR Scikit-Image Pillow

Key Features

Advanced Document Verification & Tamper Detection System
Hybrid Analysis: Uses pixel-by-pixel SSIM for digital template matching and Tesseract OCR for data confirmation.
Real-World Adaptation: Adaptive thresholds handle smartphone photography challenges like glare, shadows, and perspective shifts.
High-Fidelity Comparison: Utilizes INTER_AREA interpolation and lossless saving to achieve 95%+ accuracy scores on official templates.
Visual Diff Mapping: Automatically highlights structural inconsistencies by drawing bounding boxes around detected discrepancies.
Installation & Setup

Clone the repository
Install dependencies: pip install flask opencv-python scikit-image pytesseract imutils pillow
Install Tesseract OCR on your system
Configure the path in views.py: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
Run the application: python app.py
Document Logic

The system applies a tiered verification logic to ensure accuracy: Perfect Match (>70%): Confirmed against official digital templates. Physical ID Match: Confirmed via keyword detection (e.g., "Maryland", "Johnson") even if visual scores are lower due to lighting. Inconsistency: Flagged when data exists but structural alignment is significantly warped.
