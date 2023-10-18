from flask import Flask, render_template, request, redirect, url_for
import easyocr
import cv2
import numpy as np
import base64

app = Flask(__name__)

# Load the EasyOCR reader
reader = easyocr.Reader(['en'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' in request.files:
        # Get the uploaded image
        image_file = request.files['image']
        
        # Read and process the image using EasyOCR
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        result = reader.readtext(image)
        
        # Draw text bounding boxes on the image
        for detection in result:
            top_left = tuple(map(int, detection[0][0]))
            bottom_right = tuple(map(int, detection[0][2]))
            text = detection[1]
            image = cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 3)
            image = cv2.putText(image, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Extract the detected text
        detected_text = "\n".join([detection[1] for detection in result])

        # Convert the processed image to base64 for displaying in HTML
        retval, buffer = cv2.imencode('.jpg', image)
        img_base64 = base64.b64encode(buffer).decode()

        return render_template('result.html', img_base64=img_base64, detected_text=detected_text)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
