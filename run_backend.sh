cd backend || exit
echo "Starting the application from directory: $(pwd)"
uvicorn main:app --reload
# User config here...
