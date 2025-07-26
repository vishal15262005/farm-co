from flask import Flask, request, render_template, jsonify, url_for  # Add url_for here
import tensorflow as tf
import numpy as np
import os
import base64 
from io import BytesIO
from PIL import Image, ImageDraw
print(tf.__version__)
from tensorflow.keras.preprocessing import image
from chatbox import get_chat_response  # Import chatbot logic
from werkzeug.utils import secure_filename  # Add this import
from urllib.parse import quote
import webbrowser
import time
from io import BytesIO
import base64
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_babel import Babel, gettext

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///prices.db'
db = SQLAlchemy(app)
babel = Babel(app)

# Language translations dictionary
translations = {
    'ta': {
        'home': 'முகப்பு',
        'settings': 'அமைப்புகள்',
        'language': 'மொழி',
        'disease_detection': 'நோய் கண்டறிதல்',
        'veterinary_support': 'கால்நடை மருத்துவ ஆதரவு',
        'insurance': 'காப்பீடு',
        'chat_assistant': 'உதவியாளர்',
        # Add more translations as needed
    }
}

# Update this section
def get_locale():
    return request.args.get('lang', 'en')

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def utility_processor():
    def translate(text):
        lang = request.args.get('lang', 'en')
        if lang == 'en':
            return text
        return translations.get(lang, {}).get(text, text)
    return dict(t=translate)

# Near the top of your file, after app initialization
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load trained model
# For .keras format (recommended)
# model = tf.keras.models.load_model("model/cow_skin_model.keras")
# For .h5 format (if you must use it)
model = tf.keras.models.load_model("model/cow_skin_model.h5")

# Ensure upload folder exists
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Define class labels
class_labels = ["Lumpy", "Normal"]

# Precaution lists
lsd_precautions = [
    "Isolate infected cattle immediately.",
    "Provide clean and nutritious food.",
    "Regularly disinfect the cattle shed.",
    "Avoid sharing equipment between infected and healthy animals.",
    "Consult a veterinarian for vaccination and treatment."
]

healthy_precautions = [
    "Provide a balanced diet rich in nutrients.",
    "Ensure clean and fresh drinking water is always available.",
    "Regularly clean and disinfect the cattle shed.",
    "Schedule routine veterinary check-ups and vaccinations.",
    "Monitor cattle behavior and isolate sick animals immediately."
]

# Function to predict disease
def predict_disease(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    confidence = float(np.max(predictions) * 100)  # Convert to float

    predicted_class = int(predictions[0][0] > 0.5)
    result = class_labels[predicted_class]

    return result, confidence

# Function to draw a bounding box (Dummy Example)
def draw_bounding_box(image_path):
    try:
        # Open the image
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Get image dimensions
        width, height = img.size
        
        # Calculate bounding box coordinates (center 50% of image)
        x1 = width // 4
        y1 = height // 4
        x2 = (width * 3) // 4
        y2 = (height * 3) // 4
        
        # Draw red rectangle with thickness of 3 pixels
        draw.rectangle([x1, y1, x2, y2], outline="red", width=3)
        
        # Save the image with bounding box
        output_filename = f"detected_{os.path.basename(image_path)}"
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_filename)
        img.save(output_path)
        
        return output_path
    except Exception as e:
        print(f"Error drawing bounding box: {str(e)}")
        return image_path

# Homepage Route
@app.route("/", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file:
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                file.save(filepath)

                result, confidence = predict_disease(filepath)

                if result == "Normal":
                    message = "✅ No Lumpy Skin Disease detected. Keep following good cattle management practices!"
                    result_display = "✅ Healthy - No Disease Detected"
                    precautions = healthy_precautions
                else:
                    message = "⚠ Lumpy Skin Disease detected! Take immediate precautions."
                    result_display = "⚠ Lumpy Skin Disease Detected!"
                    precautions = lsd_precautions
                    filepath = draw_bounding_box(filepath)

                return render_template(
                    "index.html",
                    file_path=filepath,
                    result_display=result_display,
                    confidence=confidence,
                    message=message,
                    precautions=precautions,
                )
    return render_template("index.html")

# Capture Image Route
@app.route("/capture", methods=["POST"])
def capture_image():
    try:
        # Get image data from request
        data = request.json["image"]
        img_data = base64.b64decode(data.split(",")[1])
        img = Image.open(BytesIO(img_data))
        
        # Create uploads directory if it doesn't exist
        os.makedirs(os.path.join('static', 'uploads'), exist_ok=True)
        
        # Save captured image
        filename = f"captured_{int(time.time())}.jpg"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        img.save(filepath)

        # Predict disease
        result, confidence = predict_disease(filepath)

        # Process result
        if result == "Normal":
            message = "✅ No Lumpy Skin Disease detected"
            result_display = "✅ Healthy - No Disease Detected"
            precautions = healthy_precautions
            display_path = f'uploads/{filename}'
        else:
            message = "⚠ Lumpy Skin Disease detected!"
            result_display = "⚠ Disease Detected!"
            precautions = lsd_precautions
            # Draw bounding box
            new_filepath = draw_bounding_box(filepath)
            display_path = f'uploads/{os.path.basename(new_filepath)}'

        # Return JSON response
        return jsonify({
            "file_path": url_for('static', filename=display_path),
            "result_display": result_display,
            "confidence": float(confidence),
            "message": message,
            "precautions": precautions
        })

    except Exception as e:
        print(f"Capture error: {str(e)}")  # Add logging
        return jsonify({"error": str(e)}), 500

# Database Models
class PriceAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    alert_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PriceEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes for price monitoring
@app.route("/prices")
def prices():
    return render_template("prices.html")

@app.route("/set-alert", methods=["POST"])
def set_alert():
    try:
        data = request.json
        new_alert = PriceAlert(
            product_name=data['product_name'],
            alert_price=float(data['alert_price'])
        )
        db.session.add(new_alert)
        db.session.commit()
        return jsonify({"status": "success", "message": "Alert set successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/add-price", methods=["POST"])
def add_price():
    try:
        data = request.json
        product_name = data['product_name']
        new_price = float(data['price'])

        # Add new price entry
        price_entry = PriceEntry(product_name=product_name, price=new_price)
        db.session.add(price_entry)
        db.session.commit()

        # Check alerts for this product
        alerts = PriceAlert.query.filter_by(product_name=product_name).all()
        triggered_alerts = []
        
        for alert in alerts:
            if new_price > alert.alert_price:
                triggered_alerts.append({
                    "product": product_name,
                    "alert_price": alert.alert_price,
                    "current_price": new_price
                })

        return jsonify({
            "status": "success",
            "message": "Price added successfully",
            "triggered_alerts": triggered_alerts
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/get-alerts")
def get_alerts():
    try:
        alerts = PriceAlert.query.all()
        return jsonify([{
            "product_name": alert.product_name,
            "alert_price": alert.alert_price,
            "created_at": alert.created_at.isoformat()
        } for alert in alerts])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-prices")
def get_prices():
    try:
        prices = PriceEntry.query.all()
        return jsonify([{
            "product_name": price.product_name,
            "price": price.price,
            "created_at": price.created_at.isoformat()
        } for price in prices])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add these routes after your existing routes
@app.route("/detect")
def detect():
    return render_template("detect.html")

@app.route("/veterinary")
def veterinary():
    return render_template("veterinary.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

@app.route("/vet-booking")
def vet_booking():
    return render_template("vet_booking.html")

@app.route("/insurance")
def insurance():
    return render_template("insurance.html")

@app.route("/predict_growth", methods=["POST"])
def predict_growth():
    try:
        data = request.json
        age = data['age']
        weight = data['weight']
        milking = data['milking']

        # Calculate growth rate (example calculation)
        growth_rate = 0.8 if milking == 'yes' else 0.6  # kg per month
        future_weight = weight + (growth_rate * 6)  # 6 months projection
        
        # Calculate health score
        ideal_weight = age * 30  # Example: rough estimate of ideal weight
        health_score = min(100, (weight / ideal_weight) * 100)

        # Generate recommendations based on data
        recommendations = []
        if weight < ideal_weight * 0.8:
            recommendations.append({
                "title": "Weight Management",
                "description": "Current weight is below ideal range. Consider increasing feed intake.",
                "action": "Increase daily feed by 10% and monitor progress"
            })
        
        if milking == 'yes':
            recommendations.append({
                "title": "Nutrition for Milking",
                "description": "Ensure adequate protein and mineral intake for milk production",
                "action": "Supplement with dairy-specific nutrients"
            })

        # Add general recommendations
        recommendations.append({
            "title": "Regular Exercise",
            "description": "Maintain activity levels for optimal health",
            "action": "Ensure 2-3 hours of daily movement"
        })

        return jsonify({
            "status": "success",
            "growth_rate": f"{growth_rate:.1f} kg/month",
            "weight_progress": f"{(weight/ideal_weight)*100:.1f}%",
            "health_score": f"{health_score:.1f}%",
            "expected_weight": f"{future_weight:.1f} kg",
            "future_weight": future_weight,
            "recommendations": recommendations
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/upload", methods=["POST"])
def handle_upload():
    if "file" not in request.files:
        return render_template("detect.html", error="No file uploaded")
    
    file = request.files["file"]
    if file.filename == "":
        return render_template("detect.html", error="No file selected")

    if file:
        try:
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Predict disease
            result, confidence = predict_disease(filepath)

            # Process result and create bounding box
            if result == "Normal":
                message = "✅ No Lumpy Skin Disease detected"
                result_display = "✅ Healthy - No Disease Detected"
                precautions = healthy_precautions
                display_path = f'uploads/{filename}'
            else:
                message = "⚠ Lumpy Skin Disease detected!"
                result_display = "⚠ Disease Detected!"
                precautions = lsd_precautions
                # Draw bounding box
                new_filepath = draw_bounding_box(filepath)
                display_path = f'uploads/{os.path.basename(new_filepath)}'

            return render_template(
                "detect.html",
                file_path=display_path,
                result_display=result_display,
                confidence=round(confidence * 100, 2),
                message=message,
                precautions=precautions,
                image_uploaded=True
            )
        except Exception as e:
            return render_template("detect.html", error=f"Error processing image: {str(e)}")

    return render_template("detect.html")

@app.route("/chat", methods=["GET", "POST"])
def chat_response():
    if request.method == "POST":
        try:
            data = request.json
            user_message = data.get('message', '').strip().lower()
            reply = get_chat_response(user_message)
            return jsonify({"reply": reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("chat.html")

@app.route("/vet-booking", methods=["POST"])
def handle_booking():
    try:
        data = request.json
        farmer_name = data.get('farmer_name')
        phone = data.get('phone')
        date = data.get('date')
        time = data.get('time')
        reason = data.get('reason')
        vet_number = data.get('vet_number')

        # Create WhatsApp message
        message = f"Hello Doctor,\n\n"
        message += f"New appointment request from {farmer_name}:\n"
        message += f"📅 Date: {date}\n"
        message += f"⏰ Time: {time}\n"
        message += f"📱 Phone: {phone}\n"
        message += f"🏥 Reason: {reason}\n"

        # Create WhatsApp link
        whatsapp_link = f"https://wa.me/{vet_number}?text={quote(message)}"

        return jsonify({
            "status": "success",
            "whatsapp_link": whatsapp_link
        })

    except Exception as e:
        print(f"Booking error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Add this route after your existing routes
@app.route("/apply-insurance")
def apply_insurance():
    return render_template("apply_insurance.html")

@app.route("/open-tn-portal")
def open_tn_portal():
    url = "https://tnlda.tn.gov.in/index.php"
    
    webbrowser.open(url, new=2)  # new=2 opens in new tab
    return jsonify({"status": "success"})

# At the bottom of app.py
if __name__ == "__main__":
    # Get local IP address
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(f"\nLocal network access:")
    print(f"Computer: http://localhost:5000")
    print(f"Mobile: http://{local_ip}:5000")
    
    # Run the app making it visible on the network
    app.run(host='0.0.0.0', port=5000, debug=True)

model.save("model/cow_skin_model.h5")


