import os
import pilgram2 
import json
import io

from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import enhanceImage

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def load_filters():
    json_path = os.path.join('static', 'filters.json')
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data['filters']

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def home():
    """Show home screen"""
    return render_template("home.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    """Show Option for anyone to upload edit and download photos"""
    if request.method == "POST":
        if 'userPhoto' not in request.files:
            flash("File not supported")
            return redirect(request.url)

        file = request.files["userPhoto"]
        if file:
            filepath = os.path.join("static/uploads", file.filename)
            file.save(filepath)
            return redirect(url_for("edit", fileName=file.filename))
        else:
            flash("No file selected.")
    else:
        return render_template("upload.html")
    
@app.route("/edit")
def edit():
    """Show Option for anyone to edit and download photos"""
    fileName = request.args.get("fileName")
    filters = load_filters()
    return render_template("edit.html", fileName=fileName, filters=filters)

@app.route("/gallery")
def gallery():
    return render_template("error.html")

@app.route("/about")
def about():
    return render_template("error.html")

@app.route("/login")
def login():
    return render_template("error.html")

@app.route("/logout")
def logout():
    return render_template("error.html")

@app.route("/register")
def register():
    return render_template("error.html")

@app.route('/apply_filter', methods=['POST'])
def apply_filter():
    try:
        # Get the filter name and current image
        filter_name = request.json.get('filter_name')
        file_name = request.json.get('file_name')
        
        # Load the image
        image_path = os.path.join(app.static_folder, 'uploads', file_name)
        image = Image.open(image_path)
        
        # Apply the filter using pilgram2
        if hasattr(pilgram2, filter_name):
            filtered_image = getattr(pilgram2, filter_name)(image)
        else:
            return jsonify({'error': f'Filter {filter_name} not found'}), 400
        
        # Save the filtered image (replace original)
        filtered_path = os.path.join(app.static_folder, 'uploads', file_name)
        filtered_image.save(filtered_path)
        
        return jsonify({
            'success': True,
            'filtered_image': file_name
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/preview_filter', methods=['POST'])
def preview_filter():
    """Generate a preview of the filter without saving permanently"""
    try:
        filter_name = request.json.get('filter_name')
        file_name = request.json.get('file_name')
        
        image_path = os.path.join(app.static_folder, 'uploads', file_name)
        image = Image.open(image_path)
        
        # Apply filter using pilgram2
        if hasattr(pilgram2, filter_name):
            filtered_image = getattr(pilgram2, filter_name)(image)
        else:
            return jsonify({'error': f'Filter {filter_name} not found'}), 400
        
        # Save temporary preview
        preview_filename = f"preview_{filter_name}_{file_name}"
        preview_path = os.path.join(app.static_folder, 'uploads', preview_filename)
        filtered_image.save(preview_path)
        
        return jsonify({
            'success': True,
            'preview_image': preview_filename
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/enhance_image', methods=['POST'])
def enhance_image():
    try:
        file_name = request.json.get('file_name')
        image_path = os.path.join(app.static_folder, 'uploads', file_name)
        image = Image.open(image_path)

        # Apply AI enhancement (dummy implementation)
        enhanced_image = enhanceImage(image, method="realesrgan")

        # Save enhanced image
        enhanced_filename = f"enhanced_{file_name}"
        enhanced_path = os.path.join(app.static_folder, 'uploads', enhanced_filename)
        enhanced_image.save(enhanced_path)

        return jsonify({
            'success': True,
            'enhanced_image': enhanced_filename
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
