#!/usr/bin/env python3
"""
Advanced Image Enhancement Service
Provides AI-powered image enhancement capabilities
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def enhance_image_advanced(image_data):
    """Dramatic image enhancement with visible improvements"""
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to OpenCV format
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Dramatic contrast enhancement
        lab = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Strong noise reduction
        enhanced = cv2.bilateralFilter(enhanced, 15, 100, 100)
        
        # Aggressive sharpening
        kernel = np.array([[-1,-1,-1,-1,-1], [-1,2,2,2,-1], [-1,2,8,2,-1], [-1,2,2,2,-1], [-1,-1,-1,-1,-1]])
        enhanced = cv2.filter2D(enhanced, -1, kernel)
        
        # Brightness and contrast boost
        enhanced = cv2.convertScaleAbs(enhanced, alpha=1.3, beta=20)
        
        # Convert back to PIL
        enhanced_pil = Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
        
        # Dramatic PIL enhancements
        enhancer = ImageEnhance.Sharpness(enhanced_pil)
        enhanced_pil = enhancer.enhance(2.0)
        
        enhancer = ImageEnhance.Color(enhanced_pil)
        enhanced_pil = enhancer.enhance(1.4)
        
        enhancer = ImageEnhance.Contrast(enhanced_pil)
        enhanced_pil = enhancer.enhance(1.3)
        
        enhancer = ImageEnhance.Brightness(enhanced_pil)
        enhanced_pil = enhancer.enhance(1.1)
        
        # Convert to base64
        buffer = io.BytesIO()
        enhanced_pil.save(buffer, format='JPEG', quality=98)
        enhanced_b64 = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/jpeg;base64,{enhanced_b64}"
        
    except Exception as e:
        print(f"Enhancement error: {e}")
        return None

@app.route('/enhance', methods=['POST'])
def enhance_endpoint():
    """API endpoint for image enhancement"""
    try:
        data = request.json
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        enhanced = enhance_image_advanced(image_data)
        
        if enhanced:
            return jsonify({'enhanced_image': enhanced})
        else:
            return jsonify({'error': 'Enhancement failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)