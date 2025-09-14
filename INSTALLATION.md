# Installation Guide

## Prerequisites

Before running the Chartink Backtesting Dashboard, you need to install Python and the required dependencies.

## Step 1: Install Python

### Windows
1. Go to [python.org](https://www.python.org/downloads/)
2. Download Python 3.11 or later
3. Run the installer
4. **Important**: Check "Add Python to PATH" during installation
5. Verify installation by opening Command Prompt and typing: `python --version`

### macOS
```bash
# Using Homebrew (recommended)
brew install python

# Or download from python.org
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

## Step 2: Install Dependencies

Once Python is installed, install the required packages:

```bash
pip install -r requirements.txt
```

If you get permission errors, try:
```bash
pip install --user -r requirements.txt
```

## Step 3: Run the Application

### Option A: Using the provided script
```bash
python run_local.py
```

### Option B: Direct execution
```bash
python app.py
```

### Option C: Using Flask directly
```bash
export FLASK_APP=app.py
flask run
```

## Step 4: Access the Dashboard

1. Open your web browser
2. Go to `http://localhost:5000`
3. You should see the Chartink Backtesting Dashboard

## Troubleshooting

### Python not found
- Make sure Python is installed and added to PATH
- Try `python3` instead of `python`
- Restart your terminal/command prompt after installation

### Permission errors
- Use `pip install --user` for user-level installation
- On Windows, run Command Prompt as Administrator
- On macOS/Linux, use `sudo pip install` (not recommended)

### Port already in use
- Change the port in `app.py`: `app.run(port=5001)`
- Or kill the process using port 5000

### Module not found errors
- Make sure you're in the correct directory
- Run `pip install -r requirements.txt` again
- Check if you're using the correct Python version

## Testing the Installation

Run the test script to verify everything is working:

```bash
python test_app.py
```

This will check:
- ✅ All required modules can be imported
- ✅ All required files are present
- ✅ CSV parsing works correctly
- ✅ Flask app starts successfully

## Next Steps

Once the application is running locally:

1. **Test with sample data**: Use the provided `sample_data.csv`
2. **Get Angel One API credentials**: Follow the instructions in README.md
3. **Deploy to free hosting**: Follow the DEPLOYMENT.md guide

## Getting Help

If you encounter issues:

1. Check this installation guide
2. Verify Python and pip are working: `python --version` and `pip --version`
3. Try installing dependencies one by one to identify the problematic package
4. Check the troubleshooting section in README.md

## Alternative: Use Online Development Environment

If you can't install Python locally, you can use online development environments:

### Replit
1. Go to [replit.com](https://replit.com)
2. Create a new Python repl
3. Upload all project files
4. Run the application

### Google Colab
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Upload the project files
3. Install dependencies: `!pip install -r requirements.txt`
4. Run the app (note: Colab is better for Jupyter notebooks)

### GitHub Codespaces
1. Fork the repository on GitHub
2. Open in Codespaces
3. Run the application in the cloud

---

**Once Python is installed, you're ready to start backtesting! 🚀**
