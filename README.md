 exam-result-mailer

A Python automation tool that scrapes student exam results from a secure portal and emails them to respective students using Excel credentials.

  
# 📤 Exam Result Mailer

A Flask-based automation tool that reads student credentials from an Excel sheet, logs into a result portal using Selenium, captures result screenshots, and securely emails them to the respective students.



## 📌 Features

- Upload Excel sheet with student credentials.
- Automate result portal login using Selenium.
- Solve CAPTCHA (manual input or OCR optional).
- Capture result screenshots (high quality).
- Email each student their result.
- Skip failed logins or empty rows.
- Secure handling of credentials via `.env`.



## 💻 Tech Stack

| Layer       | Technology         | Purpose                          |
|-------------|---------------------|----------------------------------|
| Backend     | Python (Flask)      | Web server and routing           |
| Automation  | Selenium WebDriver  | Browser automation               |
| Excel       | openpyxl            | Read Excel (.xlsx) data          |
| Screenshots | Pillow / Selenium   | Capture and enhance PNG quality |
| Email       | smtplib + email     | Send results to students         |
| UI          | HTML/CSS (Jinja2)   | Upload interface and status log |



## 📁 Folder Structure


📦exam-result-mailer/

├── static/screenshots/        # Stores result screenshots

├── templates/index.html       # Upload & result page

├── app.py                     # Main Flask app

├── requirements.txt          # Dependencies

└── README.md                  # Project documentation



 📌sample photo
 
WEB INTERFACE PAGE:
<img width="1920" height="1020" alt="image" src="https://github.com/user-attachments/assets/03005a55-5640-4da2-8d41-b56f771892fe" />
AFTER THE AUTOMATION:
<img width="1920" height="956" alt="image" src="https://github.com/user-attachments/assets/2bb0e0e0-a060-4a4f-9743-a900845ad8a8" />
 

## ⚙️ How It Works

1. **Upload Excel File**  
   Format:
   ```plaintext
   Username (Reg No) | Password (DOB) | Email
   82822XXXXXX       08-08-2005       student@example.com
   ```

2. **Read Credentials**  
   - Using `openpyxl`, read each row (skip empty/incomplete ones)
   - Convert usernames in scientific notation if necessary

3. **Automate Login (Selenium)**  
   - Open headless browser
   - Fill:
     - `Username` → `driver.find_element(By.ID, "regno")`
     - `DOB` → `driver.find_element(By.ID, "dob")`
     - `CAPTCHA` → `driver.find_element(By.ID, "captchacode")`
     - Click Login → `driver.find_element(By.ID, "submit")`

4. **Take Screenshot**  
   - Save as `static/screenshots/<username>.png`

5. **Send Email**  
   - Compose email with result image
   - Use credentials from `.env`



## 🧪 Getting Started

### 🔧 Prerequisites

- Python 3.8+
- Chrome + ChromeDriver
- GitHub account (for deployment)

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

###📦 Requirements.txt

You’ll also need to include this requirements.txt file:

Flask

selenium

openpyxl

python-dotenv

Pillow
    or 
    
✅ Required Python Packages
Install all of them using this command:

bash
pip install flask selenium pillow openpyxl

Or install them one by one:

Package	Purpose
Flask	For web application backend, routing, and file upload UI
Selenium	For browser automation to login, navigate, and capture results
Pillow (PIL)	For enhancing or resizing screenshots
OpenPyXL	For reading Excel sheets (student credentials and emails)
> ✅ **Note**: Use an app-specific password if using Gmail.

### 🚀 Run the App

```bash
python app.py
```

---

> ⛔ **The actual college website used for login automation is NOT shared publicly in this repository for privacy and security reasons.**


## ⚠️ Disclaimer

> This project is created **strictly for educational and personal automation purposes**.
>
> ❌ Do not use this to scrape unauthorized content or misuse educational portals.  
> ✅ Always obtain proper permission from the portal owner or administration before deploying this tool.  
> 🔒 Respect all terms of service, privacy rules, and ethical guidelines.

## 👨‍💻 Author
 
GitHub: [kavin-codes](https://github.com/kavin-codes)
