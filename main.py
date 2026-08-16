import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from analyzer import analyze_image_realism

app = FastAPI(title="AI Asset & Realism Inspector API")

# Enable CORS so your future frontend website can talk to this backend smoothly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all websites to connect during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an uploads directory to temporarily store uploaded images
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "AI Realism Inspector API is running successfully!"}

@app.post("/api/inspect")
async def inspect_image(file: UploadFile = File(...)):
    """
    Accepts an image upload, saves it temporarily, 
    runs your Phase 1 data science analyzer, and returns the results.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not an image.")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # Save the uploaded file locally
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Run your Phase 1 Data Science function
        result = analyze_image_realism(file_path)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
            
        return {
            "filename": file.filename,
            "analysis": result
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Clean up: delete the temporary file after analysis to save space
        if os.path.exists(file_path):
            os.remove(file_path)