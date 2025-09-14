# Chartink Backtesting Dashboard

A complete web-based backtesting dashboard for Chartink scanner signals using Angel One SmartAPI historical data.

## Features

- **Easy CSV Upload**: Drag & drop or browse to upload your Chartink CSV files
- **Angel One Integration**: Fetches real historical OHLC data from Angel One SmartAPI
- **Flexible Backtesting**: Configurable stop loss, target, and exit days
- **Performance Metrics**: Win rate, average gain/loss, max drawdown, risk-reward ratio
- **Visual Analytics**: Equity curve and returns distribution charts
- **Export Results**: Download results as CSV or Excel files
- **Free Hosting Ready**: Deploy easily on Heroku, Railway, or other free platforms

## Quick Start

### Option 1: Deploy to Heroku (Recommended - Completely Free)

1. **Fork this repository** to your GitHub account
2. **Create a Heroku account** at [heroku.com](https://heroku.com)
3. **Install Heroku CLI** from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
4. **Deploy to Heroku**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/chartink-backtesting-dashboard.git
   cd chartink-backtesting-dashboard
   heroku create your-app-name
   git push heroku main
   ```
5. **Open your app**: `heroku open`

### Option 2: Deploy to Railway (Alternative Free Option)

1. **Fork this repository** to your GitHub account
2. **Go to [railway.app](https://railway.app)** and sign up with GitHub
3. **Click "New Project"** → "Deploy from GitHub repo"
4. **Select your forked repository**
5. **Railway will automatically deploy** your app

### Option 3: Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/chartink-backtesting-dashboard.git
   cd chartink-backtesting-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Open your browser** and go to `http://localhost:5000`

## How to Use

### Step 1: Get Angel One API Credentials

1. Go to [Angel One SmartAPI](https://smartapi.angelbroking.com/)
2. Create an account and log in
3. Create a new app with "Historical Data APIs" selected
4. Note down your:
   - API Key
   - Client ID
   - Password
   - TOTP (6-digit code from your authenticator app)

### Step 2: Prepare Your Chartink CSV

Your CSV should have this format:
```csv
entry_datetime,symbol,market_cap,sector
06-08-2025 10:15 am,YATHARTH,Midcap,Pharmaceuticals
06-08-2025 10:15 am,KAMATHOTEL,Smallcap,Services
08-08-2025 9:15 am,SIRCA,Smallcap,Industrials
```

**Important Notes**:
- Date format: `DD-MM-YYYY HH:MM am/pm`
- Symbol should match Angel One's symbol format (usually NSE symbols)
- The system will automatically parse your CSV format

### Step 3: Run Backtest

1. **Upload your CSV file** using drag & drop or browse button
2. **Enter your Angel One API credentials**
3. **Configure backtest parameters**:
   - Stop Loss % (default: 5%)
   - Target % (default: 10%)
   - Exit Days (default: 10 days)
4. **Click "Run Backtest"**
5. **Wait for results** (this may take a few minutes depending on the number of trades)

### Step 4: Analyze Results

The dashboard will show:
- **Performance Metrics**: Win rate, average gains/losses, max drawdown, risk-reward ratio
- **Equity Curve**: Visual representation of your portfolio performance over time
- **Returns Distribution**: Histogram showing the distribution of your trade returns
- **Detailed Results Table**: Individual trade results with entry/exit prices and P&L

### Step 5: Export Results

Click the "Export CSV" or "Export Excel" buttons to download your results for further analysis.

## CSV Format Requirements

Your Chartink CSV must have these columns (in any order):
- **entry_datetime**: Date and time of the signal (format: DD-MM-YYYY HH:MM am/pm)
- **symbol**: Stock symbol (e.g., YATHARTH, KAMATHOTEL, SIRCA)
- **market_cap**: Market cap category (e.g., Midcap, Smallcap, Largecap)
- **sector**: Sector name (e.g., Pharmaceuticals, Services, Industrials)

## Backtesting Logic

For each trade in your CSV:

1. **Entry Price**: 1-hour candle price at the given entry time
2. **Stop Loss**: Exit if price drops by the specified percentage
3. **Target**: Exit if price rises by the specified percentage
4. **Time Exit**: If neither SL nor target is hit, exit at closing price after N days

## Performance Metrics Explained

- **Win Rate**: Percentage of profitable trades
- **Average Gain**: Average percentage gain of winning trades
- **Average Loss**: Average percentage loss of losing trades
- **Max Drawdown**: Maximum peak-to-trough decline in your equity curve
- **Risk-Reward Ratio**: Average gain divided by average loss

## Troubleshooting

### Common Issues

1. **"No historical data found"**:
   - Check if the symbol exists in Angel One's database
   - Ensure the symbol format matches NSE format
   - Verify your API credentials are correct

2. **"Authentication failed"**:
   - Double-check your API Key, Client ID, and Password
   - Make sure your TOTP is current (6-digit code from authenticator app)
   - Ensure your Angel One account has API access enabled

3. **"CSV parsing error"**:
   - Check your CSV format matches the required structure
   - Ensure date format is DD-MM-YYYY HH:MM am/pm
   - Make sure all required columns are present

4. **Slow performance**:
   - Large CSV files with many trades will take longer to process
   - The system fetches historical data for each unique symbol
   - Consider testing with a smaller dataset first

### Getting Help

If you encounter issues:
1. Check the browser console for error messages
2. Verify your CSV format matches the examples
3. Test with a small sample of trades first
4. Ensure your Angel One API credentials are working

## Technical Details

### Architecture
- **Backend**: Flask (Python web framework)
- **Frontend**: Bootstrap 5 + Plotly.js for charts
- **Data Processing**: Pandas for CSV handling and calculations
- **API Integration**: Angel One SmartAPI for historical data

### Dependencies
- Flask 2.3.3
- Pandas 2.1.1
- Plotly 5.17.0
- Requests 2.31.0
- Gunicorn (for production deployment)

### File Structure
```
chartink-backtesting-dashboard/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version specification
├── templates/
│   └── index.html        # Main dashboard template
├── static/
│   ├── css/              # Custom styles
│   └── js/               # JavaScript files
└── README.md             # This documentation
```

## Free Hosting Options

### Heroku (Recommended)
- **Free tier**: 550-1000 dyno hours per month
- **Limitations**: App sleeps after 30 minutes of inactivity
- **Perfect for**: Personal use and testing

### Railway
- **Free tier**: $5 credit per month (usually enough for small apps)
- **Advantages**: No sleep mode, better performance
- **Perfect for**: More frequent usage

### Render
- **Free tier**: 750 hours per month
- **Limitations**: App sleeps after 15 minutes of inactivity
- **Perfect for**: Development and testing

## Security Notes

- Your API credentials are only used for the backtest session
- No data is permanently stored on the server
- All uploaded files are processed in memory
- Use HTTPS in production (automatically provided by hosting platforms)

## Contributing

Feel free to fork this project and submit pull requests for improvements:
- Bug fixes
- New features
- Performance optimizations
- UI/UX improvements

## License

This project is open source and available under the MIT License.

## Support

For questions or issues:
1. Check this README first
2. Look at the troubleshooting section
3. Create an issue on GitHub
4. Ensure you've tested with a small sample first

---

**Happy Backtesting! 📈**
