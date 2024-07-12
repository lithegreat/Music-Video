from flask import Flask, request, jsonify
from flask_cors import CORS
from main import *

product_description = """Amazon Essentials Men's Short Sleeve T-Shirt with Crew Neck in Regular Fit, Pack of 2 Material Composition: Solids: 100% Cotton Heathered: 60% Cotton, 40% Polyester, Care Instructions: Machine wash warm, Tumble dry: Closure Type, Button: Collar Style, Crew neck"""
LLManager = LLM("An advertisement for Amazon.de", product_description)
diffusionManager = diffusion()
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for local development


@app.route('/generate-video', methods=['POST'])
async def generate_video():
    data = request.get_json()
    topic = data.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400

    access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOnsidXNlcl91dWlkIjoiNDU4M2UxNzMtNmJkMi00NDlhLTllNzAtYzE1M2ViNzQ1MzliIiwiY2xpZW50X2lkIjoiIn0sImV4cCI6MTcyMDc3OTMyNX0.ApJv5aWUIIZOAafzQXjlxt_YpoTMppGKq-XOPYToXzo'
    output_file = await process_topicCompleteVideo(topic, LLManager, diffusionManager, access_token)
    video_url = f"/static/{output_file}"  # Assuming you serve static files from a static directory
    return jsonify({'videoUrl': video_url})

if __name__ == '__main__':
    app.run(debug=True)
