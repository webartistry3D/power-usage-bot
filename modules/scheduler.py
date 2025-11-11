# task automation

import schedule, time
from modules.data_collector import fetch_usage_data
from modules.analyzer import analyze_usage
from modules.predictor import train_model, predict_next_day_usage
from modules.notifier import send_report

def job():
    print("⏳ Running scheduled job...")
    fetch_usage_data()
    train_model()
    summary = analyze_usage()
    prediction = predict_next_day_usage()
    send_report(summary, prediction)
    print("✅ Report sent successfully.\n")

def run_scheduler():
    schedule.every().day.at("07:00").do(job)
    print("🚀 PowerPal Scheduler Started (Runs daily at 7:00 AM)")
    while True:
        schedule.run_pending()
        time.sleep(60)
