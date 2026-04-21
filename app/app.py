from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Azure DevOps Project!",
        "status": "running",
        "version": os.getenv("APP_VERSION", "1.0.0")
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }), 200

@app.route("/info")
def info():
    return jsonify({
        "app": "azure-devops-demo",
        "environment": os.getenv("ENVIRONMENT", "production"),
        "deployed_at": os.getenv("DEPLOY_TIME", "unknown")
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)