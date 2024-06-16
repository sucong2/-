from flask import Flask, request, send_file
from flask_cors import CORS
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
CORS(app)

# 데이터 처리 및 시각화 함수
def process_data(data):
    data['date'] = pd.to_datetime(data['date'])
    data['week'] = data['date'].dt.strftime('%Y-%U')
    weekly_data = data.groupby('week').mean()

    data['month'] = data['date'].dt.to_period('M')
    monthly_data = data.groupby('month').mean()
    
    return weekly_data, monthly_data

def create_charts(weekly_data, monthly_data):
    plt.figure(figsize=(10, 5))
    plt.plot(weekly_data.index, weekly_data['score'], label='Weekly Average Score')
    plt.xlabel('Week')
    plt.ylabel('Average Score')
    plt.title('Weekly Average Score Trend')
    plt.legend()
    plt.savefig('weekly_trend.png')
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_data.index.astype(str), monthly_data['score'], label='Monthly Average Score')
    plt.xlabel('Month')
    plt.ylabel('Average Score')
    plt.title('Monthly Average Score Trend')
    plt.legend()
    plt.savefig('monthly_trend.png')
    plt.close()

def create_pdf(report_title, charts):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica", 20)
    c.drawString(30, height - 40, report_title)

    y_position = height - 80
    for chart in charts:
        c.drawImage(chart, 30, y_position, width=500, height=200)
        y_position -= 220

    c.save()
    buffer.seek(0)
    return buffer

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        data = pd.read_csv(file)
        weekly_data, monthly_data = process_data(data)
        create_charts(weekly_data, monthly_data)
        pdf_buffer = create_pdf("Student Performance Report", ['weekly_trend.png', 'monthly_trend.png'])
        return send_file(pdf_buffer, as_attachment=True, download_name='student_report.pdf', mimetype='application/pdf')
    return "No file uploaded", 400


if __name__ == "__main__":
    app.run(debug=True)