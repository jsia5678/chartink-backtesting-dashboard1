from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.utils
import json
import os
from datetime import datetime, timedelta
import requests
import io
from werkzeug.utils import secure_filename
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AngelOneAPI:
    def __init__(self, api_key=None, client_id=None, password=None, totp=None):
        self.api_key = api_key
        self.client_id = client_id
        self.password = password
        self.totp = totp
        self.base_url = "https://apiconnect.angelone.in"
        self.access_token = None
        self.refresh_token = None
        self.feed_token = None
        
        # Symbol to token mapping for common NSE stocks (from Angel One SmartAPI)
        self.symbol_tokens = {
            'RELIANCE': '2881',
            'TCS': '2951', 
            'INFY': '4081',
            'HDFCBANK': '1333',
            'ICICIBANK': '4963',
            'SBIN': '3045',
            'WIPRO': '4081',
            'LT': '11536',
            'BAJFINANCE': '317',
            'ASIANPAINT': '1660',
            'ITC': '1660',
            'ULTRACEMCO': '11536',
            'AXISBANK': '5900',
            'MARUTI': '10999'
        }
        
    def get_access_token(self):
        """Get access token for Angel One SmartAPI"""
        try:
            # Use the NEW SmartAPI authentication endpoint
            url = f"{self.base_url}/rest/auth/angelbroking/user/v1/loginByPassword"
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': '192.168.1.1',
                'X-ClientPublicIP': '106.193.147.98',
                'X-MACAddress': '00:00:00:00:00:00',
                'X-PrivateKey': self.api_key
            }
            
            payload = {
                "clientcode": self.client_id,
                "password": self.password,
                "totp": self.totp
            }
            
            logger.info(f"Authenticating with Angel One SmartAPI...")
            response = requests.post(url, headers=headers, json=payload)
            
            logger.info(f"Auth response status: {response.status_code}")
            logger.info(f"Auth response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') and data.get('data'):
                    self.access_token = data['data']['jwtToken']
                    self.refresh_token = data['data'].get('refreshToken')
                    self.feed_token = data['data'].get('feedToken')
                    logger.info("SmartAPI authentication successful")
                    return True
                else:
                    logger.error(f"SmartAPI auth failed: {data}")
            else:
                logger.error(f"SmartAPI auth request failed with status {response.status_code}: {response.text}")
            return False
        except Exception as e:
            logger.error(f"Error getting SmartAPI access token: {e}")
            return False
    
    def get_historical_data(self, symbol, interval="ONE_MINUTE", from_date=None, to_date=None):
        """Get historical data using Angel One SmartAPI"""
        try:
            # Add rate limiting - wait between API calls
            import time
            time.sleep(1)  # Wait 1 second between API calls
            
            if not self.access_token:
                if not self.get_access_token():
                    logger.error("Failed to get SmartAPI access token")
                    return None
            
            # Get token for the symbol
            token = self.symbol_tokens.get(symbol)
            if not token:
                logger.error(f"Invalid symbol: {symbol}. Valid symbols are: {list(self.symbol_tokens.keys())}")
                return None
            
            # Use the NEW SmartAPI historical data endpoint
            url = f"{self.base_url}/rest/secure/angelbroking/historical/v1/getCandleData"
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-UserType': 'USER',
                'X-SourceID': 'WEB',
                'X-ClientLocalIP': '192.168.1.1',
                'X-ClientPublicIP': '106.193.147.98',
                'X-MACAddress': '00:00:00:00:00:00',
                'X-PrivateKey': self.api_key
            }
            
            # Default to last 30 days if dates not provided
            if not from_date:
                from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            if not to_date:
                to_date = datetime.now().strftime('%Y-%m-%d')
            
            # SmartAPI historical data payload format
            payload = {
                "mode": "FULL",
                "exchangeTokens": {
                    "NSE": [token]
                },
                "interval": interval,
                "fromDate": from_date,
                "toDate": to_date
            }
            
            logger.info(f"Requesting SmartAPI historical data for {symbol} (token: {token}) from {from_date} to {to_date}")
            response = requests.post(url, headers=headers, json=payload)
            
            logger.info(f"SmartAPI historical data response status: {response.status_code}")
            logger.info(f"SmartAPI historical data response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') and data.get('data'):
                    return self._process_historical_data(data['data'])
                else:
                    logger.error(f"No data returned for {symbol}: {data}")
            else:
                logger.error(f"SmartAPI historical data request failed with status {response.status_code}: {response.text}")
            return None
        except Exception as e:
            logger.error(f"Error getting SmartAPI historical data for {symbol}: {e}")
            return None
    
    def _process_historical_data(self, data):
        """Process SmartAPI historical data into DataFrame"""
        try:
            df_data = []
            for exchange, tokens in data.items():
                for token, candles in tokens.items():
                    for candle in candles:
                        # Skip candles with empty or invalid data
                        if len(candle) < 6 or not all(candle[:6]):
                            logger.warning(f"Skipping invalid candle data: {candle}")
                            continue
                        
                        try:
                            # Safely convert to float, handling empty strings
                            open_price = float(candle[1]) if candle[1] and candle[1] != '' else 0.0
                            high_price = float(candle[2]) if candle[2] and candle[2] != '' else 0.0
                            low_price = float(candle[3]) if candle[3] and candle[3] != '' else 0.0
                            close_price = float(candle[4]) if candle[4] and candle[4] != '' else 0.0
                            volume = int(candle[5]) if candle[5] and candle[5] != '' else 0
                            
                            # Skip if all prices are zero (invalid data)
                            if open_price == 0 and high_price == 0 and low_price == 0 and close_price == 0:
                                logger.warning(f"Skipping candle with zero prices: {candle}")
                                continue
                            
                            df_data.append({
                                'timestamp': datetime.fromtimestamp(int(candle[0]) / 1000),
                                'open': open_price,
                                'high': high_price,
                                'low': low_price,
                                'close': close_price,
                                'volume': volume
                            })
                        except (ValueError, TypeError) as e:
                            logger.warning(f"Skipping invalid candle data: {candle}, error: {e}")
                            continue
            
            if not df_data:
                logger.error("No valid historical data found")
                return None
            
            df = pd.DataFrame(df_data)
            df = df.sort_values('timestamp').reset_index(drop=True)
            logger.info(f"Processed {len(df)} SmartAPI historical data points")
            return df
        except Exception as e:
            logger.error(f"Error processing SmartAPI historical data: {e}")
            return None

class BacktestEngine:
    def __init__(self, api_client):
        self.api_client = api_client
        
    def run_backtest(self, trades_df, stop_loss_pct, target_pct, exit_days):
        """Run backtest on trades"""
        results = []
        
        for _, trade in trades_df.iterrows():
            try:
                # Parse entry date and time
                entry_datetime = pd.to_datetime(trade['entry_datetime'])
                symbol = trade['symbol']
                
                # Get historical data for the symbol
                hist_data = self.api_client.get_historical_data(
                    symbol, 
                    from_date=(entry_datetime - timedelta(days=5)).strftime('%Y-%m-%d'),
                    to_date=(entry_datetime + timedelta(days=exit_days + 5)).strftime('%Y-%m-%d')
                )
                
                if hist_data is None or hist_data.empty:
                    logger.warning(f"No historical data for {symbol}")
                    continue
                
                # Find entry price (closest 1-hour candle)
                entry_price = self._get_entry_price(hist_data, entry_datetime)
                if entry_price is None:
                    logger.warning(f"Could not find entry price for {symbol} at {entry_datetime}")
                    continue
                
                # Calculate stop loss and target prices
                try:
                    sl_price = float(entry_price) * (1 - float(stop_loss_pct) / 100)
                    target_price = float(entry_price) * (1 + float(target_pct) / 100)
                except (ValueError, TypeError) as e:
                    logger.error(f"Error calculating prices for {symbol}: {e}, entry_price: {entry_price}")
                    continue
                
                # Find exit conditions
                exit_result = self._find_exit(hist_data, entry_datetime, entry_price, 
                                            sl_price, target_price, exit_days)
                
                if exit_result:
                    pnl_pct = ((exit_result['exit_price'] - entry_price) / entry_price) * 100
                    results.append({
                        'symbol': symbol,
                        'entry_datetime': entry_datetime,
                        'entry_price': entry_price,
                        'exit_datetime': exit_result['exit_datetime'],
                        'exit_price': exit_result['exit_price'],
                        'exit_reason': exit_result['exit_reason'],
                        'pnl_pct': pnl_pct,
                        'pnl_amount': exit_result['exit_price'] - entry_price,
                        'stop_loss': sl_price,
                        'target': target_price
                    })
                    
            except Exception as e:
                logger.error(f"Error processing trade for {trade.get('symbol', 'unknown')}: {e}")
                continue
        
        return pd.DataFrame(results)
    
    def _get_entry_price(self, hist_data, entry_datetime):
        """Get entry price from closest 1-hour candle"""
        try:
            # Filter data around entry time (±2 hours)
            start_time = entry_datetime - timedelta(hours=2)
            end_time = entry_datetime + timedelta(hours=2)
            
            mask = (hist_data['timestamp'] >= start_time) & (hist_data['timestamp'] <= end_time)
            nearby_data = hist_data[mask]
            
            if nearby_data.empty:
                return None
            
            # Find closest timestamp
            nearby_data['time_diff'] = abs(nearby_data['timestamp'] - entry_datetime)
            closest_idx = nearby_data['time_diff'].idxmin()
            
            close_price = nearby_data.loc[closest_idx, 'close']
            # Ensure we have a valid price
            if pd.isna(close_price) or close_price == 0:
                logger.warning(f"Invalid close price for {entry_datetime}: {close_price}")
                return None
            return float(close_price)
        except Exception as e:
            logger.error(f"Error getting entry price: {e}")
            return None
    
    def _find_exit(self, hist_data, entry_datetime, entry_price, sl_price, target_price, exit_days):
        """Find exit conditions for a trade"""
        try:
            # Filter data after entry time
            post_entry_data = hist_data[hist_data['timestamp'] > entry_datetime].copy()
            
            if post_entry_data.empty:
                return None
            
            # Check for stop loss or target hits
            for _, row in post_entry_data.iterrows():
                try:
                    # Safely convert prices to float
                    low_price = float(row['low']) if not pd.isna(row['low']) else 0
                    high_price = float(row['high']) if not pd.isna(row['high']) else 0
                    close_price = float(row['close']) if not pd.isna(row['close']) else 0
                    
                    # Skip if prices are invalid
                    if low_price == 0 or high_price == 0 or close_price == 0:
                        continue
                    
                    # Check if low hit stop loss
                    if low_price <= sl_price:
                        return {
                            'exit_datetime': row['timestamp'],
                            'exit_price': sl_price,
                            'exit_reason': 'Stop Loss'
                        }
                    
                    # Check if high hit target
                    if high_price >= target_price:
                        return {
                            'exit_datetime': row['timestamp'],
                            'exit_price': target_price,
                            'exit_reason': 'Target'
                        }
                except (ValueError, TypeError) as e:
                    logger.warning(f"Error processing row data: {e}, row: {row}")
                    continue
            
            # If neither hit, exit after n days
            exit_date = entry_datetime + timedelta(days=exit_days)
            exit_data = post_entry_data[post_entry_data['timestamp'] >= exit_date]
            
            if not exit_data.empty:
                exit_row = exit_data.iloc[0]
                try:
                    exit_price = float(exit_row['close']) if not pd.isna(exit_row['close']) else 0
                    if exit_price == 0:
                        logger.warning(f"Invalid exit price for time exit: {exit_row['close']}")
                        return None
                    return {
                        'exit_datetime': exit_row['timestamp'],
                        'exit_price': exit_price,
                        'exit_reason': f'Time Exit ({exit_days} days)'
                    }
                except (ValueError, TypeError) as e:
                    logger.error(f"Error processing time exit: {e}, exit_row: {exit_row}")
                    return None
            
            return None
        except Exception as e:
            logger.error(f"Error finding exit: {e}")
            return None

def calculate_metrics(results_df):
    """Calculate performance metrics"""
    if results_df.empty:
        return {}
    
    total_trades = len(results_df)
    winning_trades = len(results_df[results_df['pnl_pct'] > 0])
    losing_trades = len(results_df[results_df['pnl_pct'] < 0])
    
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    avg_gain = results_df[results_df['pnl_pct'] > 0]['pnl_pct'].mean() if winning_trades > 0 else 0
    avg_loss = results_df[results_df['pnl_pct'] < 0]['pnl_pct'].mean() if losing_trades > 0 else 0
    
    # Calculate equity curve
    results_df = results_df.sort_values('exit_datetime')
    results_df['cumulative_pnl'] = results_df['pnl_pct'].cumsum()
    
    # Calculate max drawdown
    peak = results_df['cumulative_pnl'].expanding().max()
    drawdown = results_df['cumulative_pnl'] - peak
    max_drawdown = drawdown.min()
    
    # Risk-reward ratio
    risk_reward = abs(avg_gain / avg_loss) if avg_loss != 0 else 0
    
    return {
        'total_trades': total_trades,
        'winning_trades': winning_trades,
        'losing_trades': losing_trades,
        'win_rate': round(win_rate, 2),
        'avg_gain': round(avg_gain, 2),
        'avg_loss': round(avg_loss, 2),
        'max_drawdown': round(max_drawdown, 2),
        'risk_reward': round(risk_reward, 2),
        'total_pnl': round(results_df['pnl_pct'].sum(), 2)
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Parse CSV
            df = pd.read_csv(filepath)
            
            # Check if we have enough columns
            if len(df.columns) < 2:
                return jsonify({'error': 'CSV must have at least 2 columns: date/time and symbol'}), 400
            
            # Flexible column mapping - handle different CSV formats
            column_mapping = {}
            for i, col in enumerate(df.columns):
                col_lower = str(col).lower().strip()
                if any(keyword in col_lower for keyword in ['date', 'time', 'datetime', 'entry']):
                    column_mapping[col] = 'entry_datetime'
                elif any(keyword in col_lower for keyword in ['symbol', 'stock', 'scrip', 'ticker']):
                    column_mapping[col] = 'symbol'
                elif any(keyword in col_lower for keyword in ['market', 'cap', 'mcap']):
                    column_mapping[col] = 'market_cap'
                elif any(keyword in col_lower for keyword in ['sector', 'industry']):
                    column_mapping[col] = 'sector'
            
            # Rename columns based on mapping
            df = df.rename(columns=column_mapping)
            
            # If we don't have required columns, try to map by position
            if 'entry_datetime' not in df.columns:
                df.columns.values[0] = 'entry_datetime'
            if 'symbol' not in df.columns:
                df.columns.values[1] = 'symbol'
            if 'market_cap' not in df.columns and len(df.columns) > 2:
                df.columns.values[2] = 'market_cap'
            if 'sector' not in df.columns and len(df.columns) > 3:
                df.columns.values[3] = 'sector'
            
            # Ensure we have at least entry_datetime and symbol
            if 'entry_datetime' not in df.columns or 'symbol' not in df.columns:
                return jsonify({'error': 'CSV must have date/time and symbol columns'}), 400
            
            # Fill missing columns with defaults
            if 'market_cap' not in df.columns:
                df['market_cap'] = 'Unknown'
            if 'sector' not in df.columns:
                df['sector'] = 'Unknown'
            
            # Flexible date parsing - handle multiple formats
            try:
                # Try different date formats
                df['entry_datetime'] = pd.to_datetime(df['entry_datetime'], format='%m-%d-%Y %I:%M %p', errors='coerce')
                if df['entry_datetime'].isna().any():
                    # Try alternative format
                    df['entry_datetime'] = pd.to_datetime(df['entry_datetime'], format='%d-%m-%Y %I:%M %p', errors='coerce')
                if df['entry_datetime'].isna().any():
                    # Try with mixed format
                    df['entry_datetime'] = pd.to_datetime(df['entry_datetime'], format='mixed', dayfirst=True, errors='coerce')
                if df['entry_datetime'].isna().any():
                    # Try ISO format
                    df['entry_datetime'] = pd.to_datetime(df['entry_datetime'], format='ISO8601', errors='coerce')
                
                # Check if any dates are still invalid
                if df['entry_datetime'].isna().any():
                    invalid_rows = df[df['entry_datetime'].isna()]
                    return jsonify({
                        'error': f'Invalid date format found in rows: {invalid_rows.index.tolist()}. Please use format: MM-DD-YYYY HH:MM AM/PM or DD-MM-YYYY HH:MM AM/PM'
                    }), 400
                    
            except Exception as e:
                return jsonify({'error': f'Date parsing error: {str(e)}. Please check your date format.'}), 400
            
            # Store in session or temporary file
            df.to_csv(filepath, index=False)
            
            # Log the processed data for debugging
            logger.info(f"Processed CSV with {len(df)} rows")
            logger.info(f"Columns: {list(df.columns)}")
            logger.info(f"Sample data: {df.head().to_dict('records')}")
            
            return jsonify({
                'success': True,
                'filename': filename,
                'trades_count': len(df),
                'preview': df.head().to_dict('records'),
                'columns': list(df.columns)
            })
        
        return jsonify({'error': 'Invalid file format. Please upload a CSV file.'}), 400
        
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/backtest', methods=['POST'])
def run_backtest():
    try:
        data = request.get_json()
        
        filename = data.get('filename')
        stop_loss = float(data.get('stop_loss', 5))
        target = float(data.get('target', 10))
        exit_days = int(data.get('exit_days', 10))
        
        # API credentials
        api_key = data.get('api_key')
        client_id = data.get('client_id')
        password = data.get('password')
        totp = data.get('totp')
        
        if not all([filename, api_key, client_id, password, totp]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Load trades data
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        trades_df = pd.read_csv(filepath)
        trades_df['entry_datetime'] = pd.to_datetime(trades_df['entry_datetime'])
        
        # Initialize API client and backtest engine
        api_client = AngelOneAPI(api_key, client_id, password, totp)
        backtest_engine = BacktestEngine(api_client)
        
        # Run backtest
        results_df = backtest_engine.run_backtest(trades_df, stop_loss, target, exit_days)
        
        if results_df.empty:
            logger.error("No trades could be processed - results DataFrame is empty")
            return jsonify({
                'error': 'No trades could be processed. Common issues:\n\n1. INVALID TOTP: Get a fresh 6-digit code from your authenticator app\n2. INVALID SYMBOLS: Use valid NSE symbols like RELIANCE, TCS, INFY, HDFCBANK\n3. RATE LIMITING: Wait a few minutes before trying again\n4. API CREDENTIALS: Check your API Key, Client ID, and MPIN\n\nValid symbols: RELIANCE, TCS, INFY, HDFCBANK, ICICIBANK, SBIN, WIPRO, LT, BAJFINANCE, ASIANPAINT, ITC, ULTRACEMCO, AXISBANK, MARUTI'
            }), 400
        
        # Calculate metrics
        metrics = calculate_metrics(results_df)
        
        # Create charts
        equity_curve = create_equity_curve_chart(results_df)
        returns_distribution = create_returns_distribution_chart(results_df)
        
        return jsonify({
            'success': True,
            'results': results_df.to_dict('records'),
            'metrics': metrics,
            'equity_curve': equity_curve,
            'returns_distribution': returns_distribution
        })
        
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        return jsonify({'error': str(e)}), 500

def create_equity_curve_chart(results_df):
    """Create equity curve chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=results_df['exit_datetime'],
        y=results_df['cumulative_pnl'],
        mode='lines',
        name='Equity Curve',
        line=dict(color='blue', width=2)
    ))
    
    fig.update_layout(
        title='Equity Curve',
        xaxis_title='Date',
        yaxis_title='Cumulative P&L (%)',
        hovermode='x unified'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_returns_distribution_chart(results_df):
    """Create returns distribution chart"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=results_df['pnl_pct'],
        nbinsx=20,
        name='Returns Distribution',
        marker_color='lightblue'
    ))
    
    fig.update_layout(
        title='Returns Distribution',
        xaxis_title='P&L (%)',
        yaxis_title='Frequency',
        bargap=0.1
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/export', methods=['POST'])
def export_results():
    try:
        data = request.get_json()
        results = data.get('results', [])
        export_format = data.get('format', 'csv')
        
        if not results:
            return jsonify({'error': 'No results to export'}), 400
        
        df = pd.DataFrame(results)
        
        if export_format == 'excel':
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Backtest Results', index=False)
            output.seek(0)
            return send_file(
                output,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name='backtest_results.xlsx'
            )
        else:
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name='backtest_results.csv'
            )
            
    except Exception as e:
        logger.error(f"Error exporting results: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)