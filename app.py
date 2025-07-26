from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl, time, datetime, os, smtplib
from PIL import Image
from io import BytesIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SCREENSHOT_FOLDER'] = 'static/screenshots'

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['SCREENSHOT_FOLDER'], exist_ok=True)

# Email credentials (Replace with .env or secure config in real use)
EMAIL_SENDER = 'your_email@example.com'
EMAIL_PASSWORD = 'app password'

results = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global results
    if request.method == 'POST':
        results.clear()
        file = request.files['excel']
        if file and file.filename.endswith('.xlsx'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            results = process_excel(filepath)
            return redirect(url_for('index'))
    return render_template('index.html', results=results)

def send_email_with_attachment(to_email, subject, body, attachment_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(attachment_path)}")
                msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True
    except Exception as e:
        print(f"Email to {to_email} failed: {e}")
        return False

def process_excel(file_path):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active
    
    service = Service("CHROMEDRIVER_PATH")
    status_list = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if not row or not all(row[:3]):
            continue  # ✅ Skip empty or invalid rows

        username, password, email = row[:3]

        # Convert scientific username if needed
        if isinstance(username, float):
            username = str(int(username))
        else:
            username = str(username)

        # Convert Excel date format to string
        if isinstance(password, datetime.datetime):
            password = password.strftime("%d-%m-%Y")
        else:
            password = str(password)

        try:
            driver = webdriver.Chrome(service=service)
            driver.set_window_size(1920, 1080)
            wait = WebDriverWait(driver, 10)

            driver.get("https://coe.example.edu.in/index.php")##replace ur webiste name #change the selector also.based on your html 
            wait.until(EC.presence_of_element_located((By.ID, "txtLoginId"))).send_keys(username)
            wait.until(EC.presence_of_element_located((By.ID, "txtPassword"))).send_keys(password)

            captcha_div = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='noselect']")))
            captcha_text = captcha_div.text.strip()
            driver.find_element(By.ID, "txtCaptcha").send_keys(captcha_text)
            driver.find_element(By.XPATH, "//input[@type='button' and @value='Submit']").click()
            time.sleep(3)

            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='End Sem Results']"))).click()
            time.sleep(3)
            driver.switch_to.frame("divRightPane")

            # ✅ Take high-quality screenshot
            png_data = driver.get_screenshot_as_png()
            img = Image.open(BytesIO(png_data)).convert('RGB')
            img = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)

            file_name = f"{username}.png"
            screenshot_path = os.path.join(app.config['SCREENSHOT_FOLDER'], file_name)
            img.save(screenshot_path, format="PNG", dpi=(300, 300), optimize=True)

            # ✅ Email sending
            email_sent = send_email_with_attachment(
                to_email=email,
                subject="Your Exam Result Screenshot",
                body=f"Dear {username},\n\nPlease find your exam result screenshot attached.\n\nRegards,\nExam Cell",
                attachment_path=screenshot_path
            )

            status_list.append({
                'username': username,
                'status': '✅ Success & Email Sent' if email_sent else '⚠️ Screenshot Saved, Email Failed',
                'screenshot': file_name
            })

        except Exception as e:
            status_list.append({
                'username': username,
                'status': f'❌ Failed: {str(e)}',
                'screenshot': None
            })

        finally:
            driver.quit()
            time.sleep(2)

    return status_list

@app.route('/screenshots/<filename>')
def get_screenshot(filename):
    return send_from_directory(app.config['SCREENSHOT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
