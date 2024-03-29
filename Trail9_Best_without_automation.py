# This code is removes the data fetching automation

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Initialize Chrome WebDriver
driver = webdriver.Chrome()
driver.maximize_window()

# Function to wait for user input
def get_input(prompt):
    return input(prompt)

# Function to handle OTP input and verification
def handle_otp_verification():
    otp = get_input("Please enter the OTP received on your mobile and press Enter: ")

    # Find OTP field and input OTP
    otp_field = driver.find_element(By.ID, 'tfotp')
    otp_field.send_keys(otp)

    # Click on Verify button
    verify_button = driver.find_element(By.ID, "btverify")
    verify_button.click()

# Step 1: Provide phone number and wait for user to manually input captcha
login_url = "https://vahan.parivahan.gov.in/nrservices/faces/user/citizen/citizenlogin.xhtml"
driver.get(login_url)

# Find phone number field and input phone number
phone_number = '9371186069'  # Replace with your phone number
mobile_number_field = driver.find_element(By.ID, "TfMOBILENO")
mobile_number_field.send_keys(phone_number)

# Manually input captcha
captcha_text = get_input("Please enter the captcha and press Enter: ")

# Find captcha field and input captcha text
captcha_field = driver.find_element(By.ID, 'txt_ALPHA_NUMERIC')
captcha_field.send_keys(captcha_text)

# Click on Next button for step 1
next_button = driver.find_element(By.ID, "btRtoLogin")
next_button.click()

# Step 2: Provide password manually
password = get_input("Please enter the password and press Enter: ")

# Find password field and input password
password_field = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "tfPASSWORD")))
password_field.send_keys(password)

# Click on Continue button for step 2
continue_button = driver.find_element(By.ID, "btRtoLogin")
continue_button.click()

# Step 3: Handle OTP verification
handle_otp_verification()

# Function to input vehicle number
def input_vehicle_number(vehicle_number):
    vehicle_number_field = driver.find_element(By.ID, "regn_no1_exact")
    vehicle_number_field.send_keys(vehicle_number)

# Function to click on "Vahan Search" button
def click_vahan_search():
    vahan_search_button = driver.find_element(By.NAME, "j_idt57")
    vahan_search_button.click()

# Function to extract and return vehicle details
def extract_vehicle_details():
    # Wait for the details to load
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "rcDetailsPanel")))

    # Extract and return vehicle details as dictionary
    details = {}
    try:
        details["Registration Number"] = driver.find_element(By.XPATH, "//div[@title='Registration Number']").text.strip()
        details["RC Status"] = driver.find_element(By.XPATH, "//div[@title='RC Status']").text.strip().split(':')[1]
        details["Vehicle Class"] = driver.find_element(By.XPATH, "//div[@title='Vehicle Class']").text.strip()
        details["Fuel Type"] = driver.find_element(By.XPATH, "//div[@title='Fuel']").text.strip()
        details["Model Name"] = driver.find_element(By.XPATH, "//span[@title='Model Name']").text.strip()
        details["Manufacturer Name"] = driver.find_element(By.XPATH, "//span[@title='Manufacturer Name']").text.strip()
        details["Registering Authority"] = driver.find_element(By.XPATH, "//span[@title='Registering Authority']").text.strip()
        details["Owner's Name"] = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]").text.strip()
        details["Registration Date"] = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]/div[4]").text.strip()
        details["Fitness/Registration Validity"] = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[4]/div[2]/span[1]").text.strip()
        details["MV Tax Validity"] = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[4]/div[4]").text.strip()
        details["PUCC Validity"] = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[5]/div[2]/span[1]").text.strip()
        details["Insurance Company"] = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[7]/span[1]").text.strip()
        details["Insurance Validity"] = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[7]/span[2]").text.strip()
        details["Policy Number"] = driver.find_element(By.XPATH, "/html[1]/body[1]/form[1]/div[1]/div[4]/div[3]/div[1]/div[1]/div[1]/div[1]/div[7]/span[3]").text.strip()
    except NoSuchElementException as e:
        print("Error occurred while extracting details:", e)
    return details

# Click on Vahan Search button
click_vahan_search()

# Input vehicle number
vehicle_number = input("Please enter the vehicle number and press Enter: ")
input_vehicle_number(vehicle_number)

# Manually input captcha
captcha_text = get_input("Please enter the captcha and press Enter: ")
captcha_field = driver.find_element(By.ID, 'vahancaptcha:CaptchaID')
captcha_field.send_keys(captcha_text)

# Extract vehicle details
vehicle_details = extract_vehicle_details()
print("Vehicle Details:")
print(vehicle_details)

# Store fetched data into Pandas DataFrame
df = pd.DataFrame([vehicle_details])

# Load existing CSV file if it exists, otherwise create a new DataFrame
try:
    existing_df = pd.read_csv("all_vehicle_details.csv")
except FileNotFoundError:
    existing_df = pd.DataFrame()

# Concatenate existing DataFrame with the new DataFrame
updated_df = pd.concat([existing_df, df], ignore_index=True)

# Save the updated DataFrame to the CSV file
updated_df.to_csv("all_vehicle_details.csv", index=False)

# Close the browser session
driver.quit()

