from app import app
from app.api_modules import google_gemini_api
from app.api_modules import video_api

app.register_blueprint(google_gemini_api.gemini_api)
app.register_blueprint(video_api.video_api)
if __name__ == "__main__":
    app.run(debug=True ,port=8080)