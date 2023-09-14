import os
import openai
openai.organization = "Your open AI org"
openai.api_key = 'Your open AI api key'
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from flask_cors import CORS
from flask_cors import cross_origin
import json
from flask import Flask, request, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.security import generate_password_hash
import sqlite3
from datetime import datetime, timedelta
import uuid
import psutil
import time
import sys
import threading
from flask import make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from cryptography.fernet import Fernet
from logging.handlers import RotatingFileHandler
import traceback
from multiprocessing import Process
import time
import io
from bardapi import Bard
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from itsdangerous import URLSafeTimedSerializer

def prompt(X):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": "You are en email outreach assistant capable of personalizing emails for maximum open rates."
        },
        {
          "role": "user",
            "content": X
        },
      ],
      temperature=1,
      max_tokens=300,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['message']['content']
def promptc(X):
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=[
        {
          "role": "system",
          "content": "You are en email outreach assistant capable of personalizing emails for maximum open rates."
        },
        {
          "role": "user",
            "content": X
        },
      ],
      temperature=1,
      max_tokens=300,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response['choices'][0]['message']['content']
def scrape_website(url):
    all_contents = []
    from urllib.parse import urlparse
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    options = FirefoxOptions()
    options.add_argument("--headless")
    firefox_driver_path = "/usr/bin/geckodriver"
    service = Service(executable_path=firefox_driver_path)
    driver = webdriver.Firefox(service=service,options=options)

    parsed_url = urlparse(url)
    domain_name = parsed_url.netloc.split('.')[-2]

    # Website scraping
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    elements_to_scrape = ['header', 'footer', 'section', 'div', 'span', 'article', 'main', 'aside', 'h1', 'h2', 'h3', 'p', 'a']

    # Extract desired information from elements on the website
    for element in elements_to_scrape:
        elements = soup.find_all(element)
        for elem in elements:
            element_text = re.sub(r'[\n\t]+', ' ', elem.text.strip())
            all_contents.append(element_text)

    # Quit the web driver
    driver.quit()

    return all_contents

def find_index(text,word):
    start_index = text.find(word)
    end_index = start_index + len(word) - 1

    if start_index != -1:
        return(end_index+1)
    else:
        print("Word not found in the text.")

if os.path.exists('encryption_key.txt'):
    # If the file exists, read the key from the file
    with open('encryption_key.txt', 'r') as file:
        encryption_key = file.read().encode()
else:
    # If the file doesn't exist, generate a new key and save it to the file
    encryption_key = Fernet.generate_key()
    with open('encryption_key.txt', 'w') as file:
        file.write(encryption_key.decode())

cipher_suite = Fernet(encryption_key)

app = Flask(__name__)
app.secret_key = 'pranay214'
CORS(app, supports_credentials=True)
login_manager = LoginManager()
login_manager.init_app(app)
limiter = Limiter(app)
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
SMTP_SERVER = 'smtpout.secureserver.net'
SMTP_PORT = 587  
SMTP_USERNAME = 'admin@catalyst-tech.in'
SMTP_PASSWORD = 'Shivam#9121007036'
EMAIL_FROM = 'admin@catalyst-tech.in'
EMAIL_SUBJECT = 'Verify your email'
SERIALIZER = URLSafeTimedSerializer('pranay214')

def get_db():
    db = sqlite3.connect('Mailapp.db')
    return db


class User(UserMixin):
    def __init__(self, id_, email):
        self.id = id_
        self.email = email
def load_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM User WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        return None

    return User(id_=user[0], email=user[1])


@app.route('/Client')
@login_required
def Client():
    return {'message': 'Welcome to client page.'}

@app.route('/clients', methods=['POST'])
@limiter.limit("5 per minute", key_func=get_remote_address)    # This is an example. Adjust the rate limit to suit your needs.
@cross_origin(supports_credentials=True)
def save_client_details():
    try:
        db = get_db()
        cursor = db.cursor()

        # Fetch the session_id from the session
        session_id = request.cookies.get('session_id')
        if session_id is None:
            return jsonify({'message': 'No active session.'}), 401

        # Use session_id to get user_id from Session table
        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            return jsonify({'message': 'Invalid session_id.'}), 401
        cursor.execute("SELECT * FROM ClientInfo WHERE user_id = ?", (user_id[0],))
        existing_client_info = cursor.fetchone()

        # Get input variables from the request
        USP = request.form.get('USP')
        offer = request.form.get('offer')
        Company_Name = request.form.get('Company_Name')
        Owner_Name = request.form.get('Owner_Name')
        Phone_number = request.form.get('Phone_number')
        Website = request.form.get('Website')
        Consultation_link = request.form.get('Consultation_link')
        Service = request.form.get('Service')
        Customer = request.form.get('Customer')
        Industry = request.form.get('Industry')

        # Insert these details into the ClientInfo table
        if existing_client_info:
            # Update existing record
            cursor.execute("""
                UPDATE ClientInfo SET
                    USP = ?, 
                    offer = ?, 
                    Company_Name = ?, 
                    Owner_Name = ?, 
                    Phone_number = ?, 
                    Website = ?, 
                    Consultation_link = ?, 
                    Service = ?, 
                    Customer = ?, 
                    Industry = ?,
                    created_at = ?
                WHERE user_id = ?
            """, (
                USP, 
                offer, 
                Company_Name, 
                Owner_Name, 
                Phone_number, 
                Website, 
                Consultation_link, 
                Service, 
                Customer, 
                Industry,
                datetime.now(),
                user_id[0]
            ))
        else:
            # Insert new record
            cursor.execute("""
                INSERT INTO ClientInfo(
                    user_id,
                    USP, 
                    offer, 
                    Company_Name, 
                    Owner_Name, 
                    Phone_number, 
                    Website, 
                    Consultation_link, 
                    Service, 
                    Customer, 
                    Industry,
                    created_at
                ) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id[0], 
                USP, 
                offer, 
                Company_Name, 
                Owner_Name, 
                Phone_number, 
                Website, 
                Consultation_link, 
                Service, 
                Customer, 
                Industry,
                datetime.now()
            ))

        db.commit()

        return jsonify({'message': 'Data saved successfully.'}), 200

    except Exception as e:
        print(e)  # log the error
        return jsonify({'message': 'An error occurred.'})  # send a generic error message
    finally:
        db.close()


@app.route('/logout', methods=['POST'])
@cross_origin(supports_credentials=True)
def logout():
    try:
        db = get_db()
        cursor = db.cursor()

        # Fetch session id from cookies
        session_id = request.cookies.get('session_id')
        print("Session ID: ", session_id)
        if not session_id:
            return jsonify({"message": "No active session."}), 400

        # Check if the session exists in the database
        cursor.execute("SELECT * FROM Session WHERE session_id = ?", (session_id,))
        session_data = cursor.fetchone()
        if session_data is None:
            return jsonify({"message": "Invalid session."}), 400

        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()

        # Update session end time
        cursor.execute("UPDATE Session SET ended_at = ? WHERE session_id = ?", (datetime.now(), session_id))
        db.commit()

        # Clear the session_id cookie on the client-side
        response = make_response(jsonify({'message': 'Logged out.'}))
        response.set_cookie('session_id', '', expires=0)
        cursor.execute("INSERT INTO Request (user_id, request_data, created_at) VALUES (?, ?, ?)", (user_id[0], 'logout', datetime.now()))
        db.commit()
        return response, 200

    except Exception as e:
        return jsonify({'message': 'An error occurred. Please try again later.'}), 500
    finally:
        db.close()

@app.route('/schedule_email', methods=['POST'])
@cross_origin(supports_credentials=True)
def schedule_email():
    try:
        db = get_db()
        cursor = db.cursor()
        # Get user_id and session_id from session
        session_id = request.cookies.get('session_id')
        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            return jsonify({'message': 'Invalid session_id.'}), 401

        cursor.execute("SELECT * FROM ClientInfo WHERE user_id = ?", (user_id[0],))
        client_data = cursor.fetchone()
        if client_data is None:
            return jsonify({'message': 'User data not saved. Please save user details first.'}), 400

        
        # Get scheduled date and time from form data
        scheduled_date = request.form['scheduled_date']
        scheduled_time = request.form['scheduled_time']
        scheduled_date = request.form.get('scheduled_date')
        scheduled_time = request.form.get('scheduled_time')
        if not scheduled_date or not scheduled_time:
            return jsonify({'message': 'Scheduled date and time are required.'}), 400

        try:
            scheduled_datetime = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%B %d, %Y %H:%M")
            if scheduled_datetime <= datetime.now():
                return jsonify({'message': 'Invalid date. Please select a future date and time.'}), 400
        except ValueError:
            return jsonify({'message': 'Invalid date or time format.'}), 400

        # Validate leads file
        leads_file = request.files['leads']
        if not leads_file:
            return jsonify({'message': 'Leads file is required.'}), 400

        try:
            df = pd.read_csv(leads_file.stream)
            if not all(column in df.columns for column in ['Name', 'Website', 'Mail', 'L_Email']):
                return jsonify({'message': 'Invalid leads file format. Missing columns.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error reading leads file: {str(e)}'}), 400
        scheduled_datetime = datetime.strptime(f"{scheduled_date} {scheduled_time}", "%B %d, %Y %H:%M")
        cursor.execute("""
            INSERT INTO EmailSchedule(user_id, session_id, scheduled_date, status, created_at)
            VALUES(?, ?, ?, ?, ?)
            """, (user_id[0], session_id, scheduled_datetime, 'pending', datetime.now()))
        db.commit()
        email_schedule_id = cursor.lastrowid
        # Save the uploaded leads file
        # Iterate over each row in the dataframe and insert into the LeadsInfo table
        for _, row in df.iterrows():
            cursor.execute("""
            INSERT INTO LeadsInfo(email_schedule_id, user_id, name, website, mail, l_email)
            VALUES(?, ?, ?, ?, ?, ?)
            """, (email_schedule_id, user_id[0], row['Name'], row['Website'], row['Mail'], row['L_Email']))
        db.commit()
        # Insert the scheduled email into the EmailSchedule table
        cursor.execute("INSERT INTO Request (user_id, request_data, created_at) VALUES (?, ?, ?)", (user_id[0], 'Schedule', datetime.now()))
        db.commit()
        return jsonify({'message': 'Email scheduled successfully!'})
    except Exception as e:
        traceback.print_exc()
        return jsonify({'message': f'An error occurred: {str(e)}. Please try again later.'}), 500
    finally:
        db.close()


@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute", key_func=get_remote_address)  
@cross_origin(supports_credentials=True)
def login():
    data = request.get_json()
    email = data.get('email')
    profile_pic = data.get('profilePic')
    name = data.get('name')
    google_id = data.get('googleId')
    expires_in = data.get('expiresIn')
    created_at = data.get('createdAt')
    token = data.get('token')
    ip_address = data.get('ipAddress')

    try:
        db = get_db()
        cursor = db.cursor()

        # Check if user already exists, if not, create a new user
        cursor.execute("SELECT * FROM User WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user is None:
            cursor.execute("""
                INSERT INTO User(email, google_id, profile_pic, created_at, updated_at, ip, subscription_type, subscription_start_date, subscription_end_date, mails_generated_in_trial)
                VALUES(?, ?, ?, ?, ?, ?, 'FREE TRIAL', ?, ?, 0)
            """, (email, google_id, profile_pic, datetime.now(), datetime.now(), ip_address, datetime.now(), datetime.now() + timedelta(days=365)))
            user_id = cursor.lastrowid
        else:
            user_id = user[0]
            # Update profile pic of existing user
            cursor.execute("""
                UPDATE User SET profile_pic = ? WHERE id = ?
            """, (profile_pic, user_id))

        # Add token to OAuthToken table
        cursor.execute("""
            INSERT INTO OAuthToken(user_id, access_token, refresh_token, expires_in, token_type, created_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?, ?)
        """, (user_id, token, None, expires_in, 'Bearer', created_at, datetime.now()))

        session_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO Session(user_id, session_id, created_at)
            VALUES(?, ?, ?)
        """, (user_id, session_id, datetime.now()))
        
        db.commit()

        session['session_id'] = session_id
        response = make_response(jsonify({'message': 'Logged in.'}), 200)
        response.set_cookie('session_id', session_id,httponly=True, samesite='None',secure=True)
        cursor.execute("INSERT INTO Request (user_id, request_data, created_at) VALUES (?, ?, ?)", (user[0], 'google_login', datetime.now()))
        db.commit()
        return response

    except sqlite3.Error as e:
        print(f"Error: {e}")  # log the error
        return jsonify({'message': 'An error occurred.'}), 500
    finally:
        db.close()

@app.route('/signup', methods=['POST'])
@limiter.limit("5 per minute", key_func=get_remote_address)  
@cross_origin(supports_credentials=True)
def signup():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    ip_address = data.get('ipAddress')
    hashed_password = generate_password_hash(password, method='sha256')

    first_letter = name[0].upper()
    profile_pic_url = f"https://ui-avatars.com/api/?name={first_letter}&background=random&color=fff"

    try:
        db = get_db()
        cursor = db.cursor()

        # Check if email already exists
        cursor.execute("SELECT * FROM User WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user:
            return jsonify({'message': 'Email already exists.'}), 400

        cursor.execute("SELECT * FROM User WHERE ip = ?", (ip_address,))
        user_with_same_ip = cursor.fetchone()
        if user_with_same_ip:
            return jsonify({'message': 'User already exists.'}), 400

        # Insert new user into the User table with is_verified set to False
        cursor.execute("""
            INSERT INTO User(email, name, password, profile_pic, created_at, updated_at, ip, subscription_type, subscription_start_date, subscription_end_date, mails_generated_in_trial, is_verified)
            VALUES(?, ?, ?, ?, ?, ?, ?, 'FREE TRIAL', ?, ?, 0, 0)
        """, (email, name, hashed_password, profile_pic_url, datetime.now(), datetime.now(), ip_address, datetime.now(), datetime.now() + timedelta(days=365)))

        db.commit()

        # Send verification email
        send_verification_email(email)

        return jsonify({'message': 'Signup successful. Please verify your email.'}), 200

    except sqlite3.Error as e:
        print(f"Error: {e}")  # log the error
        return jsonify({'message': 'An error occurred.'}), 500
    finally:
        db.close()


def send_verification_email(user_email):
    token = SERIALIZER.dumps(user_email, salt='email-verification-salt')
    link = url_for('verify_email', token=token, _external=True)
    
    msg = MIMEText(f'Click the link to verify your email: {link}')
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM
    msg['To'] = user_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(EMAIL_FROM, user_email, msg.as_string())
                print('Verification Sent')
    except Exception as e:
        print(f"Error sending email: {e}")


@app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = SERIALIZER.loads(token, salt='email-verification-salt', max_age=3600)
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE User SET is_verified = 1 WHERE email = ?", (email,))
        db.commit()
        return "Email verified successfully!"
    except:
        return "The verification link is invalid or has expired."

@app.route('/local-login', methods=['POST'])
@limiter.limit("5 per minute", key_func=get_remote_address)  
@cross_origin(supports_credentials=True)
def local_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        db = get_db()
        cursor = db.cursor()

        # Fetch user with the given email
        cursor.execute("SELECT * FROM User WHERE email = ?", (email,))
        user = cursor.fetchone()

        if not user[14]:  # Assuming the is_verified column is the 14th column (0-indexed)
            return jsonify({'message': 'Please verify your email before logging in.'}), 401
        print(user[14])

        if user and user[12] and check_password_hash(user[12], password):
            session['user_id'] = user[0]
            
            # Generate a new session ID
            session_id = str(uuid.uuid4())
            
            # Insert the session ID into the Session table
            cursor.execute("""
                INSERT INTO Session(user_id, session_id, created_at)
                VALUES(?, ?, ?)
            """, (user[0], session_id, datetime.now()))
            
            db.commit()
            
            response = jsonify({
                'message': 'Logged in.',
                'name': user[1],
                'email': user[2],
                'profilePic': user[7]
            })
            
            # Set the session ID as a cookie in the response
            response.set_cookie('session_id', session_id, httponly=True, samesite='None', secure=True)
            cursor.execute("INSERT INTO Request (user_id, request_data, created_at) VALUES (?, ?, ?)", (user[0], 'local_login', datetime.now()))
            db.commit()
            return response, 200
        else:
            return jsonify({'message': 'Invalid email or password.'}), 401

    except sqlite3.Error as e:
        print(f"Error: {e}")  # log the error
        return jsonify({'message': 'An error occurred.'}), 500
    finally:
        db.close()



@app.route('/check_auth', methods=['GET'])
@cross_origin(supports_credentials=True)
def check_auth(): 
    try:
        db = get_db()
        cursor = db.cursor()

        # Fetch the session_id from the session
        session_id = request.cookies.get('session_id')
        if session_id is None:
            print("No active session.")
            return jsonify({'message': 'No active session.'}), 401

        # Use session_id to get user_id from Sessions table
        cursor.execute("SELECT user_id FROM Session WHERE session_id = ? AND ended_at IS NULL", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            print("Invalid session_id.")
            return jsonify({'message': 'Invalid session_id.'}), 401


        # Use user_id to get user profile_pic
        cursor.execute("SELECT profile_pic FROM User WHERE id = ?", (user_id[0],))
        profile_pic_result = cursor.fetchone()
        if profile_pic_result:
            profile_pic = profile_pic_result[0]
        else:
            print("No profile pic found for this user.")
            return jsonify({'message': 'No profile pic found for this user.'}), 401

        cursor.execute("SELECT mails_generated_in_trial, subscription_type FROM User WHERE id = ?", (user_id[0],))
        user_data = cursor.fetchone()
        mails_generated = user_data[0]
        subscription_type = user_data[1]

        cursor.execute("SELECT email, profile_pic FROM User WHERE id = ?", (user_id[0],))
        user_details = cursor.fetchone()
        user_email = user_details[0]
        profile_pic = user_details[1]

        # Fetch max_mails_per_month for the user's subscription type
        cursor.execute("SELECT max_mails_per_month FROM SubscriptionPlans WHERE plan_name = ?", (subscription_type,))
        max_mails = cursor.fetchone()[0]
        print("User authenticated.")
        return jsonify({
        'message': 'User authenticated.',
        'user': {
            'email': user_email,
            'profilePic': profile_pic,
            'mailsGenerated': mails_generated,
            'maxMails': max_mails
        }
        })

    except Exception as e:
        print("Error: ", e)
        return jsonify({'message': 'Server error.'}), 500
    finally:
        db.close()

@app.route('/credentials', methods=['POST'])
@cross_origin(supports_credentials=True)
def save_credentials():
    try:
        db = get_db()
        cursor = db.cursor()

        session_id = request.cookies.get('session_id')
        if session_id is None:
            return jsonify({'message': 'No active session.'}), 401

        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            return jsonify({'message': 'Invalid session_id.'}), 401


        data = request.get_json()

        # Extract the email service provider from the email address
        email_service_provider = data['emailProvider']
        if email_service_provider == 'gmail':
            smtp_host = 'smtp.gmail.com'
            smtp_port = 587
        elif email_service_provider == 'yahoo':
            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 465
        elif email_service_provider == 'outlook':
            smtp_host = 'smtp-mail.outlook.com'
            smtp_port = 587
        elif email_service_provider == 'godaddy':
            smtp_host = 'smtpout.secureserver.net'
            smtp_port = 587
        else:
            return jsonify({'message': 'Unsupported email service provider.'}), 400

        smtp_username = data['email']
        smtp_password = data['password']

        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
        except smtplib.SMTPAuthenticationError:
            return jsonify({'message': 'Authentication failed. Please check your email and password. If you have 2-factor authentication enabled, please disable it or use an app-specific password.'}), 400
        except Exception as e:
            return jsonify({'message': f'Error connecting to the email provider: {str(e)}'}), 400

        encrypted_password = cipher_suite.encrypt(data['password'].encode()).decode()
        encrypted_api_key = cipher_suite.encrypt(data['apiKey'].encode()).decode()

        cursor.execute("""
            UPDATE UserCredentials
            SET email = ?, email_password = ?, email_service_provider = ?, Openai_api_key = ?, updated_at = ?
            WHERE user_id = ?
        """, (data['email'], encrypted_password, email_service_provider, encrypted_api_key, datetime.now(), user_id[0]))

        # If no record was updated, then insert a new record
        if cursor.rowcount == 0:
            cursor.execute("""
                INSERT INTO UserCredentials(user_id, email, email_password, email_service_provider, Openai_api_key, created_at, updated_at)
                VALUES(?, ?, ?, ?, ?, ?, ?)
            """, (user_id[0], data['email'], encrypted_password, email_service_provider, encrypted_api_key, datetime.now(), datetime.now()))
        
        db.commit()

        return jsonify({'message': 'User credentials saved successfully.'}), 200
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({'message': 'An error occurred. Please try again later.'}), 500
    finally:
        db.close()

@app.route('/process_leads',methods=['POST'])
@cross_origin(supports_credentials=True)
@limiter.limit("5 per minute", key_func=get_remote_address)
def process_leads():
    print(request.cookies)
    try:
        db = get_db()
        cursor = db.cursor()

        # Fetch the session_id from the session
        session_id = request.cookies.get('session_id')
        if session_id is None:
            return jsonify({'message': 'No active session.'}), 401

        # Use session_id to get user_id from Session table
        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            return jsonify({'message': 'Invalid session_id.'}), 401

        # Use user_id to get OAuth token
        cursor.execute("SELECT * FROM OAuthToken WHERE user_id = ?", (user_id[0],))
        oauth_token = cursor.fetchone()
        if oauth_token is None:
            return jsonify({'message': 'No OAuth token found for this user.'}), 401

        if user_id is None:
            return jsonify({'message': 'user_id is None.'}), 401

        cursor.execute("SELECT subscription_type, mails_generated_in_trial FROM User WHERE id = ?", (user_id[0],))
        subscription_data = cursor.fetchone()
        if not subscription_data:
            return jsonify({'message': 'User data not found.'}), 401

        subscription_type, mails_generated = subscription_data
        if subscription_type == 'FREE_TRIAL' and mails_generated >= 5:
            return jsonify({'message': 'You have reached the limit of your free trial. Please upgrade to continue.'}), 403

        data = "Generate"
        cursor.execute("""
        INSERT INTO Request(user_id, request_data, created_at)
        VALUES(?, ?, ?)
        """, (user_id[0], data, datetime.now()))
        request_id = cursor.lastrowid
        db.commit()

        form_data = request.form.copy()
        leads_file = request.files['Leads']
        if not leads_file:
            return jsonify({'message': 'Leads file is missing.'}), 400
        # Check file extension (assuming you expect a CSV file)
        if not leads_file.filename.endswith('.csv'):
            return jsonify({'message': 'Invalid file type. Please upload a CSV file.'}), 400
        filename = secure_filename(leads_file.filename)
        user_folder = os.path.join("/tmp", str(user_id[0]))
        # Check if the user's directory exists, if not, create it
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        # Check if the file already exists in the user's directory
        leads_file_path = os.path.join(user_folder, filename)
        # If the file exists, append a timestamp to the filename to make it unique
        if os.path.exists(leads_file_path):
            base, ext = os.path.splitext(filename)
            timestamp = int(time.time())  # Current time in seconds since the Epoch
            new_filename = f"{base}_{timestamp}{ext}"
            leads_file_path = os.path.join(user_folder, new_filename)
        # Now, save the file in the user's directory
        leads_file.save(leads_file_path)

        threading.Thread(target=process_leads_worker, args=(request_id, user_id, form_data, leads_file_path)).start()
        return jsonify({'message': 'Processing started', 'request_id': request_id})
    except sqlite3.Error as e:
        # log the error details somewhere the developers can access it
        traceback.print_exc()
        return jsonify({'message': 'An unexpected error occurred, please try again later.'}), 500
    except Exception as e:  # Catch any unexpected error
        # log the error details somewhere the developers can access it
        traceback.print_exc()
        return jsonify({'message': 'An unexpected error occurred, please try again later.'}), 500
    finally:
        if db is not None:
            db.close()
        
    
        


def process_leads_worker(request_id, user_id, form_data, leads_file_path):
    # Get input variables from the request
    try:
        db = get_db()
        cursor = db.cursor()
        USP = form_data.get('USP')
        offer = form_data.get('offer')
        Company_Name = form_data.get('Company_Name')
        Owner_Name = form_data.get('Owner_Name')
        Phone_number = form_data.get('Phone_number')
        Website = form_data.get('Website')
        Consultation_link = form_data.get('Consultation_link')
        Service = form_data.get('Service')
        Customer = form_data.get('Customer')
        Industry = form_data.get('Industry')
        # Get the uploaded CSV file
        Leads = pd.read_csv(leads_file_path)  # Read the saved CSV file
        os.remove(leads_file_path)
        for key in ['USP', 'offer', 'Company_Name', 'Owner_Name', 'Phone_number', 'Website', 'Consultation_link', 'Service', 'Customer', 'Industry']:
            value = form_data.get(key)
        user_id = user_id[0]
        # Validate and handle the file input
        i = 0
        flag = 0
        placeholder_pattern = r"(\[([^\[\]]+)\])|(\{([^\{\}]+)\})"
        placeholder_penalty = 1.5
        processing_times = []
        processing_weights = []
        while i < Leads.shape[0]:
            start_time = time.time()
            cursor.execute("SELECT mails_generated_in_trial, subscription_type FROM User WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            mails_generated = user_data[0]
            subscription_type = user_data[1]

            # Fetch the max mails allowed for the user's subscription type
            cursor.execute("SELECT max_mails_per_month FROM SubscriptionPlans WHERE plan_name = ?", (subscription_type,))
            max_mails = cursor.fetchone()[0]

        # Check if user has exceeded their subscription rights
            if mails_generated >= max_mails:
                cursor.execute("""
                    UPDATE Progress 
                    SET processed_leads = ?
                    WHERE user_id = ? 
                """, (Leads.shape[0], user_id))  # replace user_id with the actual user ID
                db.commit()
                return jsonify({'message': 'You have exhausted your current subscription plan.'})
                break
            if flag==0:
                base_url = "https://"+Leads['Website'][i]
                scrape = scrape_website(base_url,"latest news")
            print(Leads.shape[0])
            print(i+1)
            print("Gathered details for Lead: "+ str(i+1))
            #prompt1 = "Analyze this company from a view and only generate 3 concise points in bullets which could be used to personalize an email outreach to this company--"
            prompt1="Analyze and criticize these contents of a company website and only generate 3 short, concise points in bullets on their business strategy,any important current news,company values and how they could benefit from a  service--"
            prompt2 = "Generate a personalized email outreach message.Always use best regards at the end.Keep current news of the company at the start, if any.Make it compelling.Make the subject suspenseful.Restrict to 200 words.The sender business is a  company and some of its important details are-{Service:  ,Customer type: ,Industry:, USP: ,Offer: }.Use this as context to connect the 2 companies personally but don't use directly in text.The receiving company is .Use these points of  strategy for personalization of the mail towards company  which has these feature--  .---Use best practices of email outreach emails"
            prompt3="--Now Fill the sender details with these-{Company Name: , Owner Name: ,Phone number: , Website: ,Consultation link: www.example.com}.Also replace Recipient placeholders with  Team."
            RB= Leads['Name'][i] #Receiver_business
            Example_mail=[]
            Example_mail1="[Subject: You won't beleive this!!\n\n Hello,I was just going through few sites yesterday and came across your http://www.what-the-frock.com/ too.I really liked the way you have presented your site. I was reading some of your content and really found them interesting and informative. So I was just wondering if I can also do something for your site. Actually I am a freelance writer and I love writing articles as a hobby on topics related to Fashion and LIfestyle.What if I provide you with an unique article as a Guest Post. An article that will be informative for your readers. The article will be related to your website and will be apprciated by your readers.It would be great if you can add a small BIO of mine at the end of the article with my related site’s links. I guarantee you that hte article will be 100% copy scape protected and will be of around 700 words.Please let me know if this sound good to you, so that we can start working on your article.Regards, Ronin, Ronin Studios, 9876500697]"
            Example_mail2="[Subject: Show you the money!!\n\n Hi,How are you?I’m writing on behalf of [affordable fashion brand] and I wanted to get in touch to see if you would be interested in being sponsored to write a post on your blog for them? I’ve been looking at your blog, I see that you’ve featured [the brand] several times already, and think you would be perfect.We would like you to create a post in your own style about [brand] and we’ll compensate you for the time you’ve taken to do this. You can choose whatever you want as long as it fits one of the following categories:DressesJeansLeather jacketsBeyond that, you have the creative freedom to do whatever you want – the only thing that we require is that we approve of the post, and that you link to [brand websiteIf this sounds like something you would like to go forward with, let me know. Or, if you have any other ideas as to how you can partner with [brand], I’d love to hear them!I look forward to hearing from you,]"
            Example_mail3="[Subject: Is this for you?!!\n\n Hi,I wanted to personally present you with an opportunity I have coming up for [affordable clothing brand] this month.This opportunity promotes their deals for around $20 and under. Here are the details:We will provide a $50 gift card to [store]Shop at [brand store] for their $20 deals.Upload 1 photo of yourself shopping in-store to Instagram with the hashtag #[custom hashtag]Use items purchased at [store] to create your look (styled with your own clothes/accessories).Post your look on your blog.Promote post on Facebook/TwitterCan you please let me know if you are interested? I would love to send you more details.Thanks so much! Hope to work with you again soon.Best,]"
            Example_mail.append(Example_mail1)
            Example_mail.append(Example_mail2)
            Example_mail.append(Example_mail3)
            j=0 #random.randint(0,len(Example_mail)-1)
            Example_mail=Example_mail[j]
            print('Done')
            #analysis=prompt(prompt1[:28]+Service+" "+prompt1[28:]+str(scraped_contents))
            if flag==0:                
                analysis=prompt(prompt1[:207]+Service+prompt1[207:]+str(scrape)[:10000]) 
            print('Done1')
            Final_mail=promptc(prompt2[:find_index(prompt2,"business is a ")]+Industry+prompt2[find_index(prompt2,"business is a "):find_index(prompt2,"Service: ")]+Service+prompt2[find_index(prompt2,"Service: "):find_index(prompt2,"type:")]+Customer+prompt2[find_index(prompt2,"type:"):find_index(prompt2,"Industry:")]+Industry+prompt2[find_index(prompt2,"Industry:"):find_index(prompt2,"USP: ")]+USP+prompt2[find_index(prompt2,"USP: "):find_index(prompt2,"Offer: ")]+offer+prompt2[find_index(prompt2,"Offer: "):find_index(prompt2,"company is ")]+RB+prompt2[find_index(prompt2,"company is "):find_index(prompt2,"Use these points of ")]+RB+prompt2[find_index(prompt2,"Use these points of "):find_index(prompt2,"mail towards company ")]+RB+prompt2[find_index(prompt2,"mail towards company "):find_index(prompt2,"feature-- ")]+analysis+prompt2[find_index(prompt2,"feature-- "):]+prompt3[:find_index(prompt3,"Company Name: ")]+Company_Name+prompt3[find_index(prompt3,"Company Name: "):find_index(prompt3,"Owner Name: ")]+Owner_Name+prompt3[find_index(prompt3,"Owner Name: "):find_index(prompt3,"Phone number: ")]+Phone_number+prompt3[find_index(prompt3,"Phone number: "):find_index(prompt3,"Website: ")]+Website+prompt3[find_index(prompt3,"Website: "):find_index(prompt3,"Consultation link: ")]+Consultation_link)
            print("Generated Mail for Lead: "+ str(i+1))
            #Final_mail=prompt(Gen_mail+prompt3[:find_index(prompt3,"Company Name: ")]+Company_Name+prompt3[find_index(prompt3,"Company Name: "):find_index(prompt3,"Owner Name: ")]+Owner_Name+prompt3[find_index(prompt3,"Owner Name: "):find_index(prompt3,"Phone number: ")]+Phone_number+prompt3[find_index(prompt3,"Phone number: "):find_index(prompt3,"Website: ")]+Website+prompt3[find_index(prompt3,"Website: "):find_index(prompt3,"Consultation link: ")]+Consultation_link+prompt3[find_index(prompt3,"Consultation link: "):find_index(prompt3,"placeholders with ")]+RB+prompt3[find_index(prompt3,"placeholders with "):])
            Leads['Mail'][i]=Final_mail
            lead_email = Leads['L_Email'][i]
            print("Mails Personalized: "+ str(i+1))
            end_time = time.time()
            time_taken = end_time - start_time  # compute the time taken for this lead
            # update progress in database
            # Inform the client about the progress and estimated time of completion      
            if not re.findall(placeholder_pattern, Final_mail):
                cursor.execute("""
                INSERT INTO EmailGenerated(user_id, request_id, email_content, targeted_company, generated_at, lead_mail)
                    VALUES(?, ?, ?, ?, ?, ?)
                    """, (user_id, request_id, Final_mail, RB, datetime.now(), lead_email))
                db.commit()
                cursor.execute("""
                    UPDATE User 
                    SET mails_generated_in_trial = mails_generated_in_trial + 1 
                    WHERE id = ?
                """, (user_id,))
                db.commit()
            processing_weights.append(1)
            processing_times.append(time_taken)
            remaining_leads = Leads.shape[0] - i # compute the remaining number of leads
            average_processing_time = sum(t*w for t, w in zip(processing_times, processing_weights)) / sum(processing_weights)
            estimated_remaining_time = average_processing_time * remaining_leads
            print(f"Estimated time remaining: {estimated_remaining_time} seconds")
            Leads.to_csv(os.path.join("C:\\Openai\\App\\flask-server\\New", leads_file_path))
            cursor.execute("""
                INSERT INTO Progress (processed_leads, total_leads, estimated_time, last_updated, request_id, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (request_id) DO UPDATE
                SET processed_leads = EXCLUDED.processed_leads, total_leads = EXCLUDED.total_leads,
                estimated_time = EXCLUDED.estimated_time, last_updated = EXCLUDED.last_updated
                """, (i+1, Leads.shape[0], estimated_remaining_time, datetime.now(), request_id, user_id))
            db.commit()
            if re.findall(placeholder_pattern, Final_mail):
                print("Placeholders detected.Rerunning Lead: "+str(i+1))
                flag=1
                processing_weights.append(placeholder_penalty)
                cursor.execute("""
                    INSERT INTO Progress (request_id, user_id, processed_leads)
                    VALUES (?, ?, ?)
                    ON CONFLICT (request_id) DO UPDATE
                    SET processed_leads = EXCLUDED.processed_leads
                    """, (request_id, user_id, i))
                db.commit()
            else:
                flag=0
                i=i+1
    except sqlite3.Error as e:
        # log the error details somewhere the developers can access it
        traceback.print_exc()
        pass
    except Exception as e:  # Catch any unexpected error
        # log the error details somewhere the developers can access it
        traceback.print_exc()
        pass
    finally:
        if db is not None:
            db.close()

@app.route('/emailget/<request_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def email_get(request_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch the session_id from the session
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return jsonify({'message': 'No active session.'}), 401

    # Use session_id to get user_id from Session table
    cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
    user_id = cursor.fetchone()
    if user_id is None:
        return jsonify({'message': 'Invalid session_id.'}), 401

    # Use user_id to get OAuth token
    cursor.execute("SELECT * FROM OAuthToken WHERE user_id = ?", (user_id[0],))
    oauth_token = cursor.fetchone()
    if oauth_token is None:
        return jsonify({'message': 'No OAuth token found for this user.'}), 401

    cursor.execute("SELECT email_content FROM EmailGenerated WHERE request_id = ?", (request_id,))
    result = cursor.fetchall()
    if result is None:
        return jsonify({'message': 'No emails found for this request_id.'}), 404

    return jsonify({'Generated_mails': result}), 200

@app.route('/check_progress/<request_id>', methods=['GET'])
@cross_origin(supports_credentials=True)
def check_progress(request_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch the session_id from the session
    session_id = request.cookies.get('session_id')
    if session_id is None:
        return jsonify({'message': 'No active session.'}), 401

    # Use session_id to get user_id from Session table
    cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
    user_id = cursor.fetchone()
    if user_id is None:
        return jsonify({'message': 'Invalid session_id.'}), 401

    # Use user_id to get OAuth token
    cursor.execute("SELECT * FROM OAuthToken WHERE user_id = ?", (user_id[0],))
    oauth_token = cursor.fetchone()
    if oauth_token is None:
        return jsonify({'message': 'No OAuth token found for this user.'}), 401

    cursor.execute("SELECT processed_leads, total_leads, estimated_time FROM Progress WHERE request_id = ?", (request_id,))
    result = cursor.fetchone()

    if result is None:
        return jsonify({'message': 'Progress not yet available for this request_id.'}), 202

    processed_leads, total_leads, estimated_time = result

    status = 'processing'
    if processed_leads == total_leads:
        status = 'completed'

    return jsonify({'Processed_leads': processed_leads, 'Total_leads': total_leads, 'Estimated_time': estimated_time, 'status': status}), 200

@app.route('/send_email1', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_email1():
    try:
        db = get_db()
        cursor = db.cursor()

        session_id = request.cookies.get('session_id')
        if session_id is None:
            return jsonify({'message': 'No active session.'}), 401

        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            return jsonify({'message': 'Invalid session_id.'}), 401

        cursor.execute("SELECT * FROM UserCredentials WHERE user_id = ?", (user_id[0],))
        user_credentials = cursor.fetchone()
        if user_credentials is None:
            return jsonify({'message': 'No user credentials found for this user.'}), 401

        # Decrypt the SMTP username and password
        smtp_username = user_credentials[2]
        if not user_credentials[3].startswith("{ciphered}"):
            smtp_password = cipher_suite.decrypt(user_credentials[3].encode()).decode()
        else:
            smtp_password = user_credentials[3].replace("{ciphered}", "")
        

        # Assign the SMTP host and port based on the email service provider
        email_service_provider = user_credentials[4]
        if email_service_provider == 'gmail':
            smtp_host = 'smtp.gmail.com'
            smtp_port = 587
        elif email_service_provider == 'yahoo':
            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 465
        elif email_service_provider == 'outlook':
            smtp_host = 'smtp-mail.outlook.com'
            smtp_port = 587
        elif email_service_provider == 'godaddy':
            smtp_host = 'smtpout.secureserver.net'
            smtp_port = 465
        else:
            return jsonify({'message': 'Unsupported email service provider.'}), 400

        # Get the highest request_id from the EmailGenerated table
        cursor.execute("SELECT MAX(request_id) FROM EmailGenerated WHERE user_id = ?", (user_id[0],))
        max_request_id = cursor.fetchone()[0]

        # Get the emails to be sent from the EmailGenerated table with the highest request_id
        cursor.execute("SELECT * FROM EmailGenerated WHERE user_id = ? AND request_id = ? AND sent_at IS NULL", (user_id[0], max_request_id))
        emails_to_send = cursor.fetchall()

        template_path = 'C:/Users/Pranay/Downloads/Final.html'
        with open(template_path, 'r') as file:
            template = file.read()

        for email_to_send in emails_to_send:
            recipient_email = email_to_send[7]
            message = email_to_send[3]

            

            # Create email object
            email = MIMEMultipart()
            subject_pattern = r"Subject: (.+)"
            match = re.search(subject_pattern, email_to_send[3])
            subject_line = match.group(1)
            email['From'] = smtp_username
            email['To'] = recipient_email
            email['Subject'] = subject_line

            # Replace subject line and body in the template
            email_content = template.replace('Unlocking the Power of Collaboration and Recognition', subject_line)
            email_content = email_content.replace("Dear Coence Team,<br><br>\n                    Is this for you?! I hope this email finds you well and enjoying the benefits of collaboration and recognition at Coence.<br><br>\n                    I am reaching out on behalf of Fresco, a cutting-edge AI automation company specializing in business process automation. Our goal is to empower small to large businesses with cross-functional AI systems, and after researching Coence and witnessing your emphasis on collaboration and recognition, it became clear that we share similar values.<br><br>\n                    Our AI automation solutions have proven to streamline processes, increase efficiency, and enhance overall productivity. We offer a range of services tailored to meet the unique needs of businesses in the AI automation industry.<br><br>\n                    I would like to extend an invitation to schedule a free consultation, where we can discuss how our AI automation solutions can complement Coence\'s strategy. By leveraging our expertise, you can unlock the full potential of your collaborative platform, providing your users with transparent skill evaluation tools and access to global learning opportunities.<br><br>\n                    I am confident that our partnership will contribute to the continued success of Coence, and I look forward to exploring this opportunity further.<br><br>\n                    Please let me know if you are interested, and I will be delighted to provide you with more information about our services.<br><br>\n                    Thank you for your time, and I hope to hear from you soon.<br><br>\n                    Best regards,<br>\n                    Pranay Singh<br>\n                    Owner, Fresco<br>\n                    Phone: 6295807418<br>\n                    Website: Catalyst.framer.ai<br>\n                    Consultation link: www.example.com\n", message)
            email_content = email_content.replace('Fresco', "Your Company Name")
            email_content = email_content.replace('\n', '<br>')
            
            email.attach(MIMEText(email_content, 'html'))

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, recipient_email, email.as_string())
                print('Message Sent')

                # Update the sent_at field in the EmailGenerated table
                cursor.execute("UPDATE EmailGenerated SET sent_at = ? WHERE id = ?", (datetime.now(), email_to_send[0]))
                db.commit()

        print("Mail sent to all leads")

        # Add an entry to the Request table
        cursor.execute("INSERT INTO Request (user_id, request_data, created_at) VALUES (?, ?, ?)", (user_id[0], 'Send_mail', datetime.now()))
        db.commit()

        return jsonify({"message": "Emails sent successfully!"})

    except Exception as e:
        return jsonify({'message': 'An error occurred. Please try again later.'}), 500
    finally:
        db.close()

@app.route('/send_selected_emails', methods=['POST'])
@cross_origin(supports_credentials=True)
def send_selected_emails():
    try:
        db = get_db()
        cursor = db.cursor()

        session_id = request.cookies.get('session_id')
        if session_id is None:
            return jsonify({'message': 'No active session.'}), 401

        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            return jsonify({'message': 'Invalid session_id.'}), 401

        cursor.execute("SELECT * FROM UserCredentials WHERE user_id = ?", (user_id[0],))
        user_credentials = cursor.fetchone()
        if user_credentials is None:
            return jsonify({'message': 'No user credentials found for this user. Please save your credentials in Settings.'}), 401
        smtp_username = user_credentials[2]
        if not user_credentials[3].startswith("{ciphered}"):
            smtp_password = cipher_suite.decrypt(user_credentials[3].encode()).decode()
        else:
            smtp_password = user_credentials[3].replace("{ciphered}", "")
        

        # Assign the SMTP host and port based on the email service provider
        email_service_provider = user_credentials[4]
        if email_service_provider == 'gmail':
            smtp_host = 'smtp.gmail.com'
            smtp_port = 587
        elif email_service_provider == 'yahoo':
            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 465
        elif email_service_provider == 'outlook':
            smtp_host = 'smtp-mail.outlook.com'
            smtp_port = 587
        elif email_service_provider == 'godaddy':
            smtp_host = 'smtpout.secureserver.net'
            smtp_port = 465
        else:
            return jsonify({'message': 'Unsupported email service provider.'}), 400
        emailIds = request.json.get('emailIds')
        if not emailIds:
            return jsonify({'message': 'No email IDs provided.'}), 400
        placeholders = ', '.join(['?'] * len(emailIds))

        # Get the emails to be sent from the EmailGenerated table with the provided IDs
        cursor.execute(f"SELECT * FROM EmailGenerated WHERE user_id = ? AND id IN ({placeholders}) AND sent_at IS NULL", [user_id[0]] + emailIds)
        emails_to_send = cursor.fetchall()
        template = request.json.get('template')
        if not template:
            return jsonify({'message': 'No template provided.'}), 400
        for email_to_send in emails_to_send:
            recipient_email = email_to_send[7]
            message = email_to_send[3]

            

            # Create email object
            email = MIMEMultipart()
            subject_pattern = r"Subject: (.+)"
            match = re.search(subject_pattern, email_to_send[3])
            subject_line = match.group(1)
            email['From'] = smtp_username
            email['To'] = recipient_email
            email['Subject'] = subject_line
            split_position = message.lower().find("best regards,")
            main_message = message[:split_position]
            signature_details = message[split_position:]
            main_message = main_message.replace('\n', '<br>')
            signature_details = signature_details.replace('\n', '<br>')
            # Replace subject line and body in the template
            email_content=template
            email_content = email_content.replace('Unlocking the Power of Collaboration and Recognition', subject_line)
            email_content = email_content.replace("Dear example,...<br>", main_message)
            email_content = email_content.replace("contact details", signature_details)
            email_content = email_content.replace('Fresco', "Your Company Name")
            email.attach(MIMEText(email_content, 'html'))

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, recipient_email, email.as_string())
                print('Message Sent')

                # Update the sent_at field in the EmailGenerated table
                cursor.execute("UPDATE EmailGenerated SET sent_at = ? WHERE id = ?", (datetime.now(), email_to_send[0]))
                db.commit()

        print("Mail sent to all leads")

        # Add an entry to the Request table
        cursor.execute("INSERT INTO Request (user_id, request_data, created_at) VALUES (?, ?, ?)", (user_id[0], 'Send_mail', datetime.now()))
        db.commit()

        return jsonify({"message": "Emails sent successfully!"})

    except Exception as e:
        print(e)
        return jsonify({'message': 'An error occurred. Please try again later.'}), 500
    finally:
        db.close()

@app.route('/get_templates', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_templates():
    try:
        # Assuming you have 3 templates for demonstration
        with open('C:\\Users\\Pranay\\Downloads\\Pro.html', 'r') as file:
            template1 = file.read()
        with open('C:\\Users\\Pranay\\Downloads\\Pro1.html', 'r') as file:
            template2 = file.read()
        with open('C:\\Users\\Pranay\\Downloads\\Pro2.html', 'r') as file:
            template3 = file.read()
        with open('C:\\Users\\Pranay\\Downloads\\Pro3.html', 'r') as file:
            template4 = file.read()
        with open('C:\\Users\\Pranay\\Downloads\\Pro4.html', 'r') as file:
            template5 = file.read()

        return jsonify({"templates": [template1, template2, template3,template4,template5]})

    except Exception as e:
        return jsonify({'message': 'An error occurred. Please try again later.'}), 500

def send_email1_core(session_id):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            print('Invalid session_id.')

        cursor.execute("SELECT * FROM UserCredentials WHERE user_id = ?", (user_id[0],))
        user_credentials = cursor.fetchone()
        if user_credentials is None:
            print( 'No user credentials found for this user.')

        # Decrypt the SMTP username and password
        smtp_username = user_credentials[2]
        if not user_credentials[3].startswith("{ciphered}"):
            smtp_password = cipher_suite.decrypt(user_credentials[3].encode()).decode()
        else:
            smtp_password = user_credentials[3].replace("{ciphered}", "")
        

        # Assign the SMTP host and port based on the email service provider
        email_service_provider = user_credentials[4]
        if email_service_provider == 'gmail':
            smtp_host = 'smtp.gmail.com'
            smtp_port = 587
        elif email_service_provider == 'yahoo':
            smtp_host = 'smtp.mail.yahoo.com'
            smtp_port = 465
        elif email_service_provider == 'outlook':
            smtp_host = 'smtp-mail.outlook.com'
            smtp_port = 587
        elif email_service_provider == 'godaddy':
            smtp_host = 'smtpout.secureserver.net'
            smtp_port = 587
        else:
            print( 'Unsupported email service provider.')

        # Get the highest request_id from the EmailGenerated table
        cursor.execute("""
            SELECT request_id 
            FROM EmailGenerated 
            WHERE sent_at IS NULL 
            ORDER BY request_id DESC 
            LIMIT 1
        """)
        max_request_id = cursor.fetchone()[0]

        # Get the emails to be sent from the EmailGenerated table with the highest request_id
        cursor.execute("SELECT * FROM EmailGenerated WHERE user_id = ? AND request_id = ? AND sent_at IS NULL", (user_id[0], max_request_id))
        emails_to_send = cursor.fetchall()

        with open('C:\\Users\\Pranay\\Downloads\\Pro.html', 'r') as file:
            template = file.read()
        if not template:
            print( 'No template provided.')


        for email_to_send in emails_to_send:
            recipient_email = email_to_send[7]
            message = email_to_send[3]

            

            # Create email object
            email = MIMEMultipart()
            subject_pattern = r"Subject: (.+)"
            match = re.search(subject_pattern, email_to_send[3])
            subject_line = match.group(1)
            email['From'] = smtp_username
            email['To'] = recipient_email
            email['Subject'] = subject_line
            split_position = message.lower().find("best regards,")
            main_message = message[:split_position]
            signature_details = message[split_position:]
            main_message = main_message.replace('\n', '<br>')
            signature_details = signature_details.replace('\n', '<br>')
            # Replace subject line and body in the template
            email_content=template
            email_content = email_content.replace('Unlocking the Power of Collaboration and Recognition', subject_line)
            email_content = email_content.replace("Dear example,...<br>", main_message)
            email_content = email_content.replace("contact details", signature_details)
            email_content = email_content.replace('Fresco', "Your Company Name")
            email.attach(MIMEText(email_content, 'html'))

            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, recipient_email, email.as_string())
                print('Message Sent')

                # Update the sent_at field in the EmailGenerated table
                cursor.execute("UPDATE EmailGenerated SET sent_at = ? WHERE id = ?", (datetime.now(), email_to_send[0]))
                db.commit()

        print("Mail sent to all leads")

        # Add an entry to the Request table
        cursor.execute("INSERT INTO Request (user_id, request_data, created_at) VALUES (?, ?, ?)", (user_id[0], 'Send_mail', datetime.now()))
        db.commit()

        print( "Emails sent successfully!")

    except Exception as e:
        print(e)
        print( 'An error occurred. Please try again later.')
    finally:
        db.close()

def process_leads_core(session_id=None,form_data=None):
    print(request.cookies)
    try:
        db = get_db()
        cursor = db.cursor()
        print(form_data)
        # Use session_id to get user_id from Session table
        cursor.execute("SELECT user_id FROM Session WHERE session_id = ?", (session_id,))
        user_id = cursor.fetchone()
        if user_id is None:
            print( 'Invalid session_id.')

        # Use user_id to get OAuth token
        cursor.execute("SELECT * FROM OAuthToken WHERE user_id = ?", (user_id[0],))
        oauth_token = cursor.fetchone()
        if oauth_token is None:
            print( 'No OAuth token found for this user.')

        if user_id is None:
            print( 'user_id is None.')

        cursor.execute("SELECT subscription_type, mails_generated_in_trial FROM User WHERE id = ?", (user_id[0],))
        subscription_data = cursor.fetchone()
        if not subscription_data:
            print('User data not found.')

        subscription_type, mails_generated = subscription_data
        if subscription_type == 'FREE_TRIAL' and mails_generated >= 5:
            print( 'You have reached the limit of your free trial. Please upgrade to continue.')

        data = "Generate"
        cursor.execute("""
        INSERT INTO Request(user_id, request_data, created_at)
        VALUES(?, ?, ?)
        """, (user_id[0], data, datetime.now()))
        request_id = cursor.lastrowid
        db.commit()
        leads_file = request.files['Leads']
        if not leads_file:
            print( 'Leads file is missing.')
        # Check file extension (assuming you expect a CSV file)
        if not leads_file.filename.endswith('.csv'):
            print( 'Invalid file type. Please upload a CSV file.')
        filename = secure_filename(leads_file.filename)
        user_folder = os.path.join("/tmp", str(user_id[0]))
        # Check if the user's directory exists, if not, create it
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        # Check if the file already exists in the user's directory
        leads_file_path = os.path.join(user_folder, filename)
        # If the file exists, append a timestamp to the filename to make it unique
        if os.path.exists(leads_file_path):
            base, ext = os.path.splitext(filename)
            timestamp = int(time.time())  # Current time in seconds since the Epoch
            new_filename = f"{base}_{timestamp}{ext}"
            leads_file_path = os.path.join(user_folder, new_filename)
        # Now, save the file in the user's directory
        leads_file.save(leads_file_path)
        print('Processing started')
        cursor = db.cursor()
        USP = form_data['USP']
        offer = form_data['offer']
        Company_Name = form_data['Company_Name']
        Owner_Name = form_data['Owner_Name']
        Phone_number = form_data['Phone_number']
        Website = form_data['Website']
        Consultation_link = form_data['Consultation_link']
        Service = form_data['Service']
        Customer = form_data['Customer']
        Industry = form_data['Industry']
        # Get the uploaded CSV file
        Leads = pd.read_csv(leads_file_path)  # Read the saved CSV file
        os.remove(leads_file_path)
        for key in ['USP', 'offer', 'Company_Name', 'Owner_Name', 'Phone_number', 'Website', 'Consultation_link', 'Service', 'Customer', 'Industry']:
            value = form_data.get(key)
        user_id = user_id[0]
        # Validate and handle the file input
        i = 0
        flag = 0
        placeholder_pattern = r"(\[([^\[\]]+)\])|(\{([^\{\}]+)\})"
        placeholder_penalty = 1.5
        processing_times = []
        processing_weights = []
        while i < Leads.shape[0]:
            start_time = time.time()
            cursor.execute("SELECT mails_generated_in_trial, subscription_type FROM User WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            mails_generated = user_data[0]
            subscription_type = user_data[1]

            # Fetch the max mails allowed for the user's subscription type
            cursor.execute("SELECT max_mails_per_month FROM SubscriptionPlans WHERE plan_name = ?", (subscription_type,))
            max_mails = cursor.fetchone()[0]

        # Check if user has exceeded their subscription rights
            if mails_generated >= max_mails:
                cursor.execute("""
                    UPDATE Progress 
                    SET processed_leads = ?
                    WHERE user_id = ? 
                """, (Leads.shape[0], user_id))  # replace user_id with the actual user ID
                db.commit()
                return jsonify({'message': 'You have exhausted your current subscription plan.'})
                break
            if flag==0:
                base_url = "https://"+Leads['Website'][i]
                scrape = scrape_website(base_url)
            print(Leads.shape[0])
            print(i+1)
            print("Gathered details for Lead: "+ str(i+1))
            #prompt1 = "Analyze this company from a view and only generate 3 concise points in bullets which could be used to personalize an email outreach to this company--"
            prompt1="Analyze and criticize these contents of a company website and only generate 3 short, concise points in bullets on their business strategy,any important current news,company values and how they could benefit from a  service--"
            prompt2 = "Generate a personalized email outreach message.Always use best regards at the end.Keep current news of the company at the start, if any.Make it compelling.Make the subject suspenseful.Restrict to 200 words.The sender business is a  company and some of its important details are-{Service:  ,Customer type: ,Industry:, USP: ,Offer: }.Use this as context to connect the 2 companies personally but don't use directly in text.The receiving company is .Use these points of  strategy for personalization of the mail towards company  which has these feature--  .---Use best practices of email outreach emails"
            prompt3="--Now Fill the sender details with these-{Company Name: , Owner Name: ,Phone number: , Website: ,Consultation link: www.example.com}.Also replace Recipient placeholders with  Team."
            RB= Leads['Name'][i] #Receiver_business
            Example_mail=[]
            Example_mail1="[Subject: You won't beleive this!!\n\n Hello,I was just going through few sites yesterday and came across your http://www.what-the-frock.com/ too.I really liked the way you have presented your site. I was reading some of your content and really found them interesting and informative. So I was just wondering if I can also do something for your site. Actually I am a freelance writer and I love writing articles as a hobby on topics related to Fashion and LIfestyle.What if I provide you with an unique article as a Guest Post. An article that will be informative for your readers. The article will be related to your website and will be apprciated by your readers.It would be great if you can add a small BIO of mine at the end of the article with my related site’s links. I guarantee you that hte article will be 100% copy scape protected and will be of around 700 words.Please let me know if this sound good to you, so that we can start working on your article.Regards, Ronin, Ronin Studios, 9876500697]"
            Example_mail2="[Subject: Show you the money!!\n\n Hi,How are you?I’m writing on behalf of [affordable fashion brand] and I wanted to get in touch to see if you would be interested in being sponsored to write a post on your blog for them? I’ve been looking at your blog, I see that you’ve featured [the brand] several times already, and think you would be perfect.We would like you to create a post in your own style about [brand] and we’ll compensate you for the time you’ve taken to do this. You can choose whatever you want as long as it fits one of the following categories:DressesJeansLeather jacketsBeyond that, you have the creative freedom to do whatever you want – the only thing that we require is that we approve of the post, and that you link to [brand websiteIf this sounds like something you would like to go forward with, let me know. Or, if you have any other ideas as to how you can partner with [brand], I’d love to hear them!I look forward to hearing from you,]"
            Example_mail3="[Subject: Is this for you?!!\n\n Hi,I wanted to personally present you with an opportunity I have coming up for [affordable clothing brand] this month.This opportunity promotes their deals for around $20 and under. Here are the details:We will provide a $50 gift card to [store]Shop at [brand store] for their $20 deals.Upload 1 photo of yourself shopping in-store to Instagram with the hashtag #[custom hashtag]Use items purchased at [store] to create your look (styled with your own clothes/accessories).Post your look on your blog.Promote post on Facebook/TwitterCan you please let me know if you are interested? I would love to send you more details.Thanks so much! Hope to work with you again soon.Best,]"
            Example_mail.append(Example_mail1)
            Example_mail.append(Example_mail2)
            Example_mail.append(Example_mail3)
            j=0 #random.randint(0,len(Example_mail)-1)
            Example_mail=Example_mail[j]
            print('Done')
            #analysis=prompt(prompt1[:28]+Service+" "+prompt1[28:]+str(scraped_contents))
            print(Service)
            print(str(scrape)[:10000])
            if flag==0:                
                analysis=prompt(prompt1[:207]+Service+prompt1[207:]+str(scrape)[:10000]) 
            print('Done1')
            Final_mail=promptc(prompt2[:find_index(prompt2,"business is a ")]+Industry+prompt2[find_index(prompt2,"business is a "):find_index(prompt2,"Service: ")]+Service+prompt2[find_index(prompt2,"Service: "):find_index(prompt2,"type:")]+Customer+prompt2[find_index(prompt2,"type:"):find_index(prompt2,"Industry:")]+Industry+prompt2[find_index(prompt2,"Industry:"):find_index(prompt2,"USP: ")]+USP+prompt2[find_index(prompt2,"USP: "):find_index(prompt2,"Offer: ")]+offer+prompt2[find_index(prompt2,"Offer: "):find_index(prompt2,"company is ")]+RB+prompt2[find_index(prompt2,"company is "):find_index(prompt2,"Use these points of ")]+RB+prompt2[find_index(prompt2,"Use these points of "):find_index(prompt2,"mail towards company ")]+RB+prompt2[find_index(prompt2,"mail towards company "):find_index(prompt2,"feature-- ")]+analysis+prompt2[find_index(prompt2,"feature-- "):]+prompt3[:find_index(prompt3,"Company Name: ")]+Company_Name+prompt3[find_index(prompt3,"Company Name: "):find_index(prompt3,"Owner Name: ")]+Owner_Name+prompt3[find_index(prompt3,"Owner Name: "):find_index(prompt3,"Phone number: ")]+Phone_number+prompt3[find_index(prompt3,"Phone number: "):find_index(prompt3,"Website: ")]+Website+prompt3[find_index(prompt3,"Website: "):find_index(prompt3,"Consultation link: ")]+Consultation_link)
            print("Generated Mail for Lead: "+ str(i+1))
            #Final_mail=prompt(Gen_mail+prompt3[:find_index(prompt3,"Company Name: ")]+Company_Name+prompt3[find_index(prompt3,"Company Name: "):find_index(prompt3,"Owner Name: ")]+Owner_Name+prompt3[find_index(prompt3,"Owner Name: "):find_index(prompt3,"Phone number: ")]+Phone_number+prompt3[find_index(prompt3,"Phone number: "):find_index(prompt3,"Website: ")]+Website+prompt3[find_index(prompt3,"Website: "):find_index(prompt3,"Consultation link: ")]+Consultation_link+prompt3[find_index(prompt3,"Consultation link: "):find_index(prompt3,"placeholders with ")]+RB+prompt3[find_index(prompt3,"placeholders with "):])
            Leads['Mail'][i]=Final_mail
            lead_email = Leads['L_Email'][i]
            print("Mails Personalized: "+ str(i+1))
            end_time = time.time()
            time_taken = end_time - start_time  # compute the time taken for this lead
            # update progress in database
            # Inform the client about the progress and estimated time of completion      
            if not re.findall(placeholder_pattern, Final_mail):
                cursor.execute("""
                INSERT INTO EmailGenerated(user_id, request_id, email_content, targeted_company, generated_at, lead_mail)
                    VALUES(?, ?, ?, ?, ?, ?)
                    """, (user_id, request_id, Final_mail, RB, datetime.now(), lead_email))
                db.commit()
                cursor.execute("""
                    UPDATE User 
                    SET mails_generated_in_trial = mails_generated_in_trial + 1 
                    WHERE id = ?
                """, (user_id,))
                db.commit()
            processing_weights.append(1)
            processing_times.append(time_taken)
            remaining_leads = Leads.shape[0] - i # compute the remaining number of leads
            average_processing_time = sum(t*w for t, w in zip(processing_times, processing_weights)) / sum(processing_weights)
            estimated_remaining_time = average_processing_time * remaining_leads
            print(f"Estimated time remaining: {estimated_remaining_time} seconds")
            Leads.to_csv(os.path.join("C:\\Openai\\App\\flask-server\\New", leads_file_path))
            cursor.execute("""
                INSERT INTO Progress (processed_leads, total_leads, estimated_time, last_updated, request_id, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT (request_id) DO UPDATE
                SET processed_leads = EXCLUDED.processed_leads, total_leads = EXCLUDED.total_leads,
                estimated_time = EXCLUDED.estimated_time, last_updated = EXCLUDED.last_updated
                """, (i+1, Leads.shape[0], estimated_remaining_time, datetime.now(), request_id, user_id))
            db.commit()
            if re.findall(placeholder_pattern, Final_mail):
                print("Placeholders detected.Rerunning Lead: "+str(i+1))
                flag=1
                processing_weights.append(placeholder_penalty)
                cursor.execute("""
                    INSERT INTO Progress (request_id, user_id, processed_leads)
                    VALUES (?, ?, ?)
                    ON CONFLICT (request_id) DO UPDATE
                    SET processed_leads = EXCLUDED.processed_leads
                    """, (request_id, user_id, i))
                db.commit()
            else:
                flag=0
                i=i+1
    except sqlite3.Error as e:
        # log the error details somewhere the developers can access it
        traceback.print_exc()
        print( 'An unexpected error occurred, please try again later.')
    except Exception as e:  # Catch any unexpected error
        # log the error details somewhere the developers can access it
        traceback.print_exc()
        print('An unexpected error occurred, please try again later.')
    finally:
        if db is not None:
            db.close()

def check_for_scheduled_emails():
    print('Triggered')
    with app.app_context():
        send_scheduled_email()

def send_scheduled_email():
    try:
        current_time = datetime.now()
        current_time = datetime.now().replace(second=0, microsecond=0)

        db = get_db()
        cursor = db.cursor()

        # Fetch emails scheduled for the current_time
        cursor.execute("SELECT user_id, id, session_id FROM Emailschedule WHERE scheduled_date = ? AND status = 'pending'", (current_time.strftime('%Y-%m-%d %H:%M:%S'),))
        scheduled_emails = cursor.fetchall()

        if not scheduled_emails:
            print(f"No scheduled emails found for {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print( "No scheduled emails found for the current time.")

        for email in scheduled_emails:
            user_id, email_schedule_id, session_id = email

            cursor.execute("SELECT * FROM ClientInfo WHERE user_id = ?", (user_id,))
            client_data = cursor.fetchone()

            if client_data is None:
                print("ClientInfo not found for user_id:", user_id)
                return

            # Fetch leads data for the given email_schedule_id
            cursor.execute("SELECT * FROM LeadsInfo WHERE email_schedule_id = ?", (email_schedule_id,))
            leads_data = cursor.fetchall()

            # Convert leads_data to a DataFrame for easier processing
            df = pd.DataFrame(leads_data, columns=['id', 'email_schedule_id', 'user_id', 'Name', 'Website', 'Mail', 'L_Email', 'created_at'])
            df = df[['Name', 'Website', 'Mail', 'L_Email']]

            # Save this DataFrame to a temporary CSV file for processing
            temp_file_path = os.path.join("/tmp", f"temp_leads_{email_schedule_id}.csv")
            df.to_csv(temp_file_path, index=False)

            form_data = {
                'USP': client_data[2],
                'offer': client_data[3],
                'Company_Name': client_data[4],
                'Owner_Name': client_data[5],
                'Phone_number': client_data[6],
                'Website': client_data[7],
                'Consultation_link': client_data[8],
                'Service': client_data[9],
                'Customer': client_data[10],
                'Industry': client_data[11]
            }
            print(form_data)
            # Call the process_leads function with the session_id
            with app.test_request_context(data={'Leads': open(temp_file_path, 'rb')}):
                # This is to ensure that the request context is set up correctly
                app.preprocess_request()
                # Use the session_id in the process_leads function as needed
                process_leads_core(session_id,form_data)

            # After processing the leads, send the emails for the specific user
            with app.test_request_context():
                send_email1_core(session_id)

            # Update the status of the email to 'sent'
            cursor.execute("UPDATE Emailschedule SET status = 'sent' WHERE id = ?", (email_schedule_id,))
            db.commit()

        print("Scheduled emails processed successfully!")

    except Exception as e:
        traceback.print_exc()
        print( 'An error occurred. Please try again later.')
    finally:
        db.close()

# Schedule the job to run at minute 0, 15, 30, and 45 of every hour
scheduler = BackgroundScheduler()
trigger = CronTrigger(minute='0,15,30,45')
scheduler.add_job(check_for_scheduled_emails, trigger=trigger)
scheduler.start()
print("Scheduler started...")

        

if __name__ == '__main__':
    app.run(port=80,debug=True)

