#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

# Add current directory to Python path to ensure imports work correctly
backend_dir = Path(__file__).resolve().parent
sys.path.append(str(backend_dir))

from river_engine.layout import set_layout_seed
from river_engine.pipeline import RiverWordPipeline

app = Flask(__name__)

# Enable CORS for frontend access
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "https://curseyou.vercel.app"
            ]
        }
    }
)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Backend Running",
        "service": "River Typography API"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    })


@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json or {}

    word = data.get("word", "").strip()

    if not word:
        return jsonify({"error": "Name cannot be empty"}), 400

    seed = data.get("seed")
    scale = data.get("scale", 1.0)
    debug = data.get("debug", False)

    if seed is not None:
        try:
            set_layout_seed(int(seed))
        except ValueError:
            pass

    try:
        pipeline = RiverWordPipeline(
            output_scale=scale,
            debug=debug
        )

        out_path = pipeline.generate(word)

        if not out_path.exists():
            return jsonify({
                "error": "Failed to generate image file"
            }), 500

        return send_file(
            str(out_path),
            mimetype="image/png"
        )

    except ValueError as exc:
        return jsonify({
            "error": str(exc)
        }), 400

    except Exception as exc:
        return jsonify({
            "error": f"Internal server error: {str(exc)}"
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
