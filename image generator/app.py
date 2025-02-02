from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from diffusers import StableDiffusionPipeline, StableVideoDiffusionPipeline
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import torch
import uuid
import os
import imageio

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set device
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Stable Diffusion (Prompt-to-Image)
image_pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
image_pipe.to(device)

# Load Stable Video Diffusion (Prompt-to-Video)
video_pipe = StableVideoDiffusionPipeline.from_pretrained(
    "stabilityai/stable-video-diffusion-img2vid", torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
video_pipe.to(device)

# Load ModelScope Image-to-Video Model
image2video_pipeline = pipeline(Tasks.text_to_video_synthesis, model="damo-vilab/modelscope-text-to-video-synthesis")

# Directory for storing generated files
os.makedirs("static", exist_ok=True)

# Route: Prompt to Image
@app.route("/generate/image", methods=["POST"])
def generate_image():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        image = image_pipe(prompt).images[0]
        image_path = f"static/{uuid.uuid4()}.png"
        image.save(image_path)
        return jsonify({"image_url": f"http://localhost:5000/{image_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Prompt to Video
@app.route("/generate/video", methods=["POST"])
def generate_video():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        video_frames = video_pipe(prompt, num_inference_steps=50).frames
        video_path = f"static/{uuid.uuid4()}.mp4"
        imageio.mimsave(video_path, video_frames, fps=10)
        return jsonify({"video_url": f"http://localhost:5000/{video_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route: Image to Video
@app.route("/generate/image-to-video", methods=["POST"])
def image_to_video():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    input_image_path = f"static/{uuid.uuid4()}.png"
    output_video_path = f"static/{uuid.uuid4()}.mp4"

    file.save(input_image_path)

    try:
        result = image2video_pipeline({"image": input_image_path})
        os.rename(result["video"], output_video_path)
        return jsonify({"video_url": f"http://localhost:5000/{output_video_path}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
