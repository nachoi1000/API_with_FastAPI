# Create a virtual environment
python -m venv virtual_env

# Activate the virtual environment
.\virtual_env\Scripts\Activate

# Install the required packages
pip install -r requirements.txt

# Change directory to backend/FastAPI
cd backend\FastAPI

# Start the FastAPI server with uvicorn
uvicorn main:app --reload