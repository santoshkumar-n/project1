import streamlit as st
import os
import datetime
import pytz
import time
import sqlite3
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Surprise",
    page_icon="🎁",
    layout="wide",
    initial_sidebar_state="collapsed",
    
)

conn = sqlite3.connect('booking_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        selected_image TEXT,
        date TEXT,
        time TEXT
    )
''')
conn.commit()

def store_booking_data(selected_image, date,time):
    cursor.execute('''
        INSERT INTO bookings (selected_image, date,time)
        VALUES (?, ?,?)
    ''', (selected_image, date,time))
    conn.commit()

def get_image_files(directory):
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    return image_files

def display_image_details(image_file,image_path):
    path=image_path.split(".")[0]
    image_name=image_file.split(".")[0]
    image = Image.open(image_path)
    resized_image = image.resize((300, 300))
    col=st.columns([1,4,1])
    col[1].image(resized_image)

def display_images(images_directory):
    image_files = get_image_files(images_directory)
    images_per_row = 3
    num_rows = len(image_files) // images_per_row + (len(image_files) % images_per_row > 0)
    for row_num in range(num_rows):
        row_images = image_files[row_num * images_per_row: (row_num + 1) * images_per_row]
        cols = st.columns(images_per_row)
        for col, image_file in zip(cols, row_images):
            image_path = os.path.join(images_directory, image_file)
            image = Image.open(image_path)
            resized_image = image.resize((300, 300))
            col.image(resized_image)
            image_name=image_file.split(".")[0]
            if col.button("See this",key=f"{image_name}"):
                st.session_state.page = 3
                st.session_state.image_path=image_path
                st.session_state.image_file=image_file
                st.experimental_rerun()
    
def display_product_images(images_directory):
    image_files = get_image_files(images_directory)
    images_per_row = 2
    num_rows = len(image_files) // images_per_row + (len(image_files) % images_per_row > 0)
    for row_num in range(num_rows):
        row_images = image_files[row_num * images_per_row: (row_num + 1) * images_per_row]
        cols = st.columns(images_per_row)
        for col, image_file in zip(cols, row_images):
            image_path = os.path.join(images_directory, image_file)
            image = Image.open(image_path)
            resized_image = image.resize((350, 350))
            col.image(resized_image)

def get_current_time_ist():
    ist = pytz.timezone('Asia/Kolkata') 
    now = datetime.datetime.now(ist)
    date_now= now.strftime("%d-%m-%Y")
    time_now=now.strftime("%I:%M %p")
    return date_now,time_now

def get_all_bookings():
    cursor.execute('''
        SELECT * FROM bookings
    ''')
    return cursor.fetchall()

def main():
    # Page 1: Cacontinue Selection
    if "page" not in st.session_state:
        st.session_state.page = 1
    if st.session_state.page == 1:
        if st.sidebar.button("Login", key="login_button"):
            st.session_state.page = 5
            st.experimental_rerun()
        if("booking_data" in st.session_state):
            selected_item=st.session_state.selected_item.split(".")[0]
            st.success(f"You Succesfully Booked  \" {selected_item} \"   you may leave now")
            st.title("Home")
            st.header("హోమ్ పేజీకి స్వాగతం !")
            st.write("ఒకవేళ బహుమతి మార్చుకోవాలంటే క్రింద ఉన్న బటన్ క్లిక్ చేయండి")
            if(st.button("change item")):
                st.session_state.page = 2
                st.experimental_rerun()
        else:
            audio_file_path= "_images/audio/audio.mp3"
            st.title("Happy Anniversary")
            st.header("Daddy & Mom")
            st.header("-By Lokesh & Santosh")
            st.audio(audio_file_path, format="audio/mp3")
            st.empty()
            st.header("తర్వాత పేజీకి వెళ్ళటానికి క్రింద ఉన్న బటన్ క్లిక్ చేయండి")
            if st.button("continue"):
                st.session_state.category = ""
                st.session_state.page = 2
                st.experimental_rerun()
            st.caption("Click to see the suprise")
            
    # Page 2: Display Images
    elif st.session_state.page == 2:
        st.subheader("ఈ క్రింద ఉన్న బహుమతులలో ఒకటి ఎంచుకోండి")
        images_directory = "_images"
        display_images(images_directory)

    # Page 3: Complete Details
    elif st.session_state.page == 3:
        selected_image = st.session_state.image_file
        directory_name=st.session_state.image_path.split("/")[-2]
        image_name=selected_image.split(".")[0]
        st.subheader("ఇవి మీరు ఎంచుకున్న బహుమతి యొక్క ఫోటోలు")
        display_product_images(directory_name+"/"+image_name)
        st.subheader("మీకు ఈ బహుమతి నచ్చితే క్రింద ఉన్న బటన్ క్లిక్ చేయండి")
        # Show booking button
        if st.button("కొనసాగించు"):
            st.session_state.page = 4  # Go to confirmation page
            st.session_state.image_file=selected_image
            st.experimental_rerun()
        if st.button("వెన్నక్కి వేళ్ళు"):
            st.session_state.page = 2
            st.experimental_rerun()
        
    #Page 4: order confirmation
    elif st.session_state.page == 4:
        selected_image = st.session_state.image_file
        directory_name=st.session_state.image_path.split("/")[-2]
        image_name=selected_image.split(".")[0]
        st.title("ఇది మీరు ఎంచుకున్న బహుమతి")
        display_image_details(st.session_state.image_file,st.session_state.image_path)
        st.empty()
        st.subheader("మీకు ఈ బహుమతి నచ్చితే క్రింద ఉన్న బటన్ క్లిక్ చేసి నిర్దారించండి")
        columns=st.columns([3,4,9])
        # Show booking button
        if columns[1].button("సరే నిర్దారించు"):
            # Prompt for booking confirmation
            date_now,time_now = get_current_time_ist()
            st.session_state.booking_data = {"selected_image": selected_image, "date_time": date_now,"time":time_now}
            store_booking_data(selected_image, date_now,time_now)
            time.sleep(0.3)
            st.success("మీ ఆర్డర్ నిర్దారించబడినది !")
            time.sleep(0.7)
            st.success("హోమ్ పేజీకి తీసుకువెళ్తున్నాము ...")
            time.sleep(0.7)
            st.session_state.selected_item=selected_image
            st.session_state.page = 1  # Go back to the category selection page
            st.experimental_rerun()
        elif columns[2].button("వెన్నక్కి వేళ్ళు"):
            st.session_state.page = 2
            st.experimental_rerun()

    #Page 5: Login
    elif st.session_state.page == 5:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        # Check if the login button is clicked
        if st.button("Login"):
            # Check if the entered credentials are valid
            if username == "Venkat" and password == "venkat":
                st.success("Login successful!")
                data=get_all_bookings()
                st.table(pd.DataFrame(data, columns=['S.No','Product', 'Date','Time']))
            else:
                st.error("Invalid username or password. Please try again.")
            pass
if __name__ == "__main__":
    main()
