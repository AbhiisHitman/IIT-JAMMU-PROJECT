import requests
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import markdown
import pdfkit
import shutil
from rich.console import Console
from rich.panel import Panel
import os

# ✅ Replace with your keys
GEMINI_KEY = "AIzaSyDRiIqef9EB9UsNoZrPRntMYDygLYHwM5M"
ALPHA_KEY = "XE5S6PJDA2WKOAU9"

# ✅ Configure Gemini
genai.configure(api_key=GEMINI_KEY)

console = Console()

# ✅ Auto-detect wkhtmltopdf
def get_pdfkit_config():
    wkhtmltopdf_path = shutil.which("wkhtmltopdf")
    if wkhtmltopdf_path:
        return pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    else:
        # Fallback - try default installation path
        default_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if os.path.exists(default_path):
            return pdfkit.configuration(wkhtmltopdf=default_path)
        else:
            console.print("[bold red]⚠ wkhtmltopdf not found! Install it from https://wkhtmltopdf.org/downloads.html[/bold red]")
            return None

def fetch_data(symbol, market_type="stock"):
    if market_type == "crypto":
        url = f"https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY&symbol={symbol}&market=USD&apikey={ALPHA_KEY}"
        data = requests.get(url).json()
        if "Time Series (Digital Currency Daily)" not in data:
            raise Exception("Crypto API Error")
        df = pd.DataFrame(data["Time Series (Digital Currency Daily)"]).T
        df.rename(columns={"4a. close (USD)": "close"}, inplace=True)
    else:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_KEY}"
        data = requests.get(url).json()
        if "Time Series (Daily)" not in data:
            raise Exception("Stock API Error")
        df = pd.DataFrame(data["Time Series (Daily)"]).T
        df.rename(columns={"4. close": "close"}, inplace=True)

    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    return df

def analyze_with_gemini(text):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(text)
    return response.text

def save_report(symbol, ai_response):
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(f"# Financial Report for {symbol}\n\n")
        f.write("![Stock Trend](trend.png)\n\n")
        f.write("## AI Recommendation\n\n")
        f.write(ai_response)

def convert_md_to_pdf():
    config = get_pdfkit_config()
    if config:
        with open("report.md", "r", encoding="utf-8") as f:
            html = markdown.markdown(f.read())
        pdfkit.from_string(html, "report.pdf", configuration=config)
        console.print("[bold green]✅ PDF report saved as report.pdf[/bold green]")
    else:
        console.print("[bold red]⚠ PDF not generated. Install wkhtmltopdf and try again.[/bold red]")

if __name__ == "__main__":
    console.print(Panel.fit("[bold green]Financial Data Extractor[/bold green]", border_style="green"))

    market_type = console.input("[cyan]Enter market type ([bold]stock[/bold]/[bold]crypto[/bold]): [/cyan]").strip().lower()
    symbol = console.input("[cyan]Enter symbol (e.g., AAPL, BTC): [/cyan]").strip().upper()

    try:
        console.print(f"[yellow]Fetching data for {symbol} ({market_type})...[/yellow]")
        df = fetch_data(symbol, market_type)

        df["close"].plot(title=f"{symbol} Closing Price")
        plt.savefig("trend.png")

        summary_text = f"Analyze this {market_type} trend for {symbol}:\n{df['close'].tail().to_dict()}"
        ai_response = analyze_with_gemini(summary_text)

        save_report(symbol, ai_response)
        convert_md_to_pdf()

        console.print(Panel(ai_response, title="AI Recommendation", border_style="yellow"))
        console.print("[bold green]✅ report.md and report.pdf generated successfully![/bold green]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
