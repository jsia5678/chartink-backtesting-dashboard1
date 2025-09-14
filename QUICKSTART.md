# Quick Start Guide

Get your Chartink Backtesting Dashboard running in 5 minutes!

## 🚀 Option 1: Deploy to Heroku (Recommended - No Local Setup)

### Step 1: Fork the Repository
1. Go to the GitHub repository
2. Click the "Fork" button (top right)
3. This creates your own copy

### Step 2: Deploy to Heroku
1. Go to [heroku.com](https://heroku.com) and sign up (free)
2. Install Heroku CLI from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. Open Command Prompt/Terminal and run:
   ```bash
   heroku login
   heroku create your-app-name
   git clone https://github.com/YOUR_USERNAME/chartink-backtesting-dashboard.git
   cd chartink-backtesting-dashboard
   git push heroku main
   heroku open
   ```

**That's it! Your app is now live on the internet! 🎉**

## 🖥️ Option 2: Run Locally (If you have Python)

### Step 1: Install Python
- Windows: Download from [python.org](https://python.org) (check "Add to PATH")
- macOS: `brew install python`
- Linux: `sudo apt install python3 python3-pip`

### Step 2: Run the App
```bash
# Download the project files
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

### Step 3: Open in Browser
Go to `http://localhost:5000`

## 📊 How to Use

### 1. Get Angel One API Credentials
1. Go to [smartapi.angelbroking.com](https://smartapi.angelbroking.com)
2. Create account and app
3. Note down: API Key, Client ID, Password, TOTP

### 2. Prepare Your CSV
Your CSV should look like this:
```csv
entry_datetime,symbol,market_cap,sector
06-08-2025 10:15 am,YATHARTH,Midcap,Pharmaceuticals
06-08-2025 10:15 am,KAMATHOTEL,Smallcap,Services
```

### 3. Run Backtest
1. Upload your CSV file
2. Enter API credentials
3. Set parameters (SL: 5%, Target: 10%, Exit: 10 days)
4. Click "Run Backtest"
5. Wait for results (2-5 minutes)

### 4. Analyze Results
- View performance metrics
- Check equity curve
- See individual trade results
- Export to CSV/Excel

## 🆘 Need Help?

### Common Issues
- **"Python not found"**: Install Python and add to PATH
- **"No historical data"**: Check symbol format and API credentials
- **"App won't start"**: Run `pip install -r requirements.txt`

### Free Hosting Options
1. **Heroku** (Recommended): 550-1000 hours/month free
2. **Railway**: $5 credit/month free
3. **Render**: 750 hours/month free

### Sample Data
Use the included `sample_data.csv` to test the system.

## 📱 Mobile Friendly
The dashboard works on mobile devices too!

## 🔒 Security
- Your API credentials are only used for the session
- No data is permanently stored
- All processing happens in memory

## 🎯 What You Get
- **Win Rate**: Percentage of profitable trades
- **Average Gain/Loss**: Performance metrics
- **Max Drawdown**: Risk assessment
- **Equity Curve**: Visual performance tracking
- **Export Results**: Download for further analysis

---

**Ready to start backtesting? Choose your deployment option above! 📈**
