import streamlit as st
import pandas as pd
import base64
import json
import os
import random

# Fungsi untuk mengonversi gambar ke base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Fungsi untuk mengatur background halaman
def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = f'''
    <style>
    html, body, .stApp {{
        background-image: url("data:image/png;base64,{bin_str}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        margin: 0; 
        padding: 0;
        height: 100%;
        width: 100%;
    }}

    header, footer {{
        background-color: rgba(0, 0, 0, 0) !important;
    }}
    </style>
    '''
    st.markdown(page_bg_img, unsafe_allow_html=True)

def load_accounts():
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as f:
            return json.load(f)
    return {}

# Fungsi untuk menyimpan akun ke file JSON
def save_accounts(accounts):
    with open("accounts.json", "w") as f:
        json.dump(accounts, f)

# Inisialisasi akun terdaftar di session_state
if "registered_accounts" not in st.session_state:
    st.session_state["registered_accounts"] = load_accounts()

# Halaman pertama (Login)
def page1():
    set_background("log in.png")  # Ganti dengan path gambar lokal Anda

    st.write("") 
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("")  

    # col1, col2, col3, col4, col5,col6 = st.columns([25,10, 10, 10,10,10])
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    st.markdown(
    """
    <style>
        .stTextInput {
            margin-left: -90px;  /* Geser ke kiri sejauh yang diinginkan */
            width: 300px;        /* Sesuaikan lebar agar muat di kotak */
        }
    </style>
    """,
    unsafe_allow_html=True
)

    with col1:
        email = st.text_input("Enter E-mail:", key="login_email")
        password = st.text_input("Password", type='password', key="login_password")

        # Menggunakan kolom untuk menempatkan tombol Log In dan Sign Up sejajar
        col_log_in, col_sign_up = st.columns([1, 1])

        with col_log_in:
            if st.button("Log In"):
                registered_accounts = st.session_state["registered_accounts"]
                if email in registered_accounts and registered_accounts[email] == password:
                    st.success("Login berhasil!")
                    st.session_state["page"] = "page3"
                else:
                    st.error("Akun belum terdaftar atau password salah. Silakan sign up terlebih dahulu.")

        with col_sign_up:
            if st.button("Sign Up"):
                st.session_state["page"] = "page2"

# Halaman kedua (Sign-Up)
def page2():
    set_background("sign in.png")  # Ganti dengan path gambar lokal Anda
    st.write("") 
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("")  
    st.write("")  

    # col1, col2, col3, col4, col5,col6 = st.columns([25,10, 10, 10,10,10])
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    st.markdown(
    """
    <style>
        .stTextInput {
            margin-left: -90px;  /* Geser ke kiri sejauh yang diinginkan */
            width: 300px;        /* Sesuaikan lebar agar muat di kotak */
        }
    </style>
    """,
    unsafe_allow_html=True
)
    with col1:
        email = st.text_input("Enter E-mail:", key="signup_email")
        password = st.text_input("Password", type='password', key="signup_password")

        if st.button("Sign Up"):
            if email and password:
                st.session_state["registered_accounts"][email] = password
                save_accounts(st.session_state["registered_accounts"])  # Simpan akun ke file
                st.success("Account successfully registered! Please login")
                st.session_state["page"] = "page3"
            else:
                st.error("Please fill in your email and password to register")

# Fungsi untuk memuat data CSV
@st.cache_data
def load_data():
    data = pd.read_csv(r"dataset_employee.csv", delimiter=';')
    data.columns = ["JobId", "Department", "Gender", "HourlyRate", "JobRole", "MonthlyIncome", "OverTime", "PerformanceRating", "StandardHours"]
    return pd.DataFrame(data)

# Inisialisasi state untuk data dan jadwal
if "df" not in st.session_state:
    st.session_state["df"] = load_data()
if "schedule_df" not in st.session_state:
    st.session_state["schedule_df"] = None

# Mapping job role berdasarkan kategori pekerjaan
job_role_mapping = {
    "Healthcare": ["Healthcare Representative"],
    "Human Resources": ["Human Resources"],
    "Research": ["Laboratory Technician", "Research Director", "Research Scientist"],
    "Management": ["Manager", "Manufacturing Director"],
    "Sales": ["Sales Executive", "Sales Representative"]
}

# Halaman ketiga: Memilih pekerjaan dan jumlah pekerja
def page3(): 
    set_background("input.png")
    

    # Menambahkan elemen-elemen ke sidebar
    with st.sidebar:
        st.header("Schedule Setting")
        st.markdown(
            """
            <style>
                [data-testid="stAppViewContainer"] img {
                    width: 200px;  /* Atur lebar sesuai keinginan */
                    height: auto;  /* Menjaga aspek rasio gambar */
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.logo('logo.png')
        selected_jobs = st.selectbox("Choose a Job:", ["Healthcare", "Human Resources", "Research", "Management", "Sales"])
        num_workers = st.number_input("NUmber of Employee per Day:", min_value=1, step=1)

        if st.button("Search"):
            if selected_jobs and num_workers:
                # Mengambil semua job roles relevan dari kombinasi job yang dipilih
                relevant_roles = job_role_mapping.get(selected_jobs, [])

                df = st.session_state["df"]
                filtered_data = df[df["JobRole"].isin(relevant_roles) & (df["PerformanceRating"] >= 3)].copy()

                # Menambahkan kolom Value dan RemainingHours
                filtered_data['Value'] = filtered_data['PerformanceRating'] / filtered_data['HourlyRate']
                filtered_data["RemainingHours"] = filtered_data["StandardHours"]

                data_list = filtered_data.to_dict('records')

                # Mengurutkan pekerja berdasarkan Value secara descending
                n = len(data_list)
                for i in range(n):
                    for j in range(0, n - i - 1):
                        if data_list[j]['Value'] < data_list[j + 1]['Value']:
                            data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]

                # Mengambil data pekerja teratas
                data_lists = data_list[:15]
                
                for worker in data_lists:
                    worker['valuee'] = worker['Value'] * worker['RemainingHours']
                
                schedule = {f"Day {i+1}": [] for i in range(20)}

                for day in schedule.keys():
                    for worker in data_lists:
                        worker['valuee'] = worker['Value'] * worker['RemainingHours']

                    # Filter pekerja yang masih memiliki jam kerja tersisa
                    available_workers = [worker for worker in data_lists if worker["RemainingHours"] > 0]

                    # Urutkan pekerja berdasarkan nilai `valuee` (menurun)
                    available_workers.sort(key=lambda x: x['valuee'], reverse=True)

                    # Pilih maksimal 4 pekerja dengan nilai `valuee` tertinggi
                    selected_workers = available_workers[:num_workers]

                    # Tambahkan pekerja yang terpilih ke jadwal hari ini
                    schedule[day] = [worker["JobId"] for worker in selected_workers]

                    # Kurangi jam kerja pekerja yang terpilih
                    for worker in selected_workers:
                        worker["RemainingHours"] -= 8 

                # Mengonversi jadwal ke DataFrame
                schedule_df = pd.DataFrame.from_dict(schedule, orient='index', columns=[f"Worker {i+1}" for i in range(num_workers)])
                # Konversi semua ID pekerja menjadi string agar tidak diformat sebagai angka
                schedule_df = schedule_df.map(str)
                schedule_df.index.name = 'Day'

                st.session_state["schedule_df"] = schedule_df
                st.session_state["page"] = "page4"
            else:
                st.error("Please select at least one occupation and specify the number of workers")


def page4():
    set_background("output.png")
    st.markdown(
    "<h1 style='color: #fff8f0; text-align: center;'>Work Schedule</h1>",
    unsafe_allow_html=True
    )

    with st.sidebar:
        st.markdown(
            """
            <style>
                [data-testid="stAppViewContainer"] img {
                    width: 200px;
                    height: auto; 
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.logo('logo.png')
        st.header("Schedule Setting")
        selected_jobs = st.selectbox("Choose a Job:", ["Healthcare", "Human Resources", "Research", "Management", "Sales"])
        num_workers = st.number_input("NUmber of Employee per Day:", min_value=1, step=1)

        if st.button("Search"):
            st.session_state["page"] = "page3"

    if "schedule_df" in st.session_state and st.session_state["schedule_df"] is not None:
        schedule_df = st.session_state["schedule_df"]

        # CSS untuk mendesain kotak hari dengan warna dan desain rounded
        st.markdown(
            """
            <style>
            .day-container {
                border: 4px solid #ccc;
                border-radius: 15px;
                padding: 20px;
                margin: 10px;
                background-color: #fff8f0; /* Warna kotak mirip seperti contoh */
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                text-align: left;
                height: 200px; /* Menentukan tinggi kotak agar konten tidak keluar */
                width: 230px;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
            }
            .day-title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 2px;
                color: #333;
                text-align: center;
            }
            .worker-list {
                font-size: 14px;
                color: #555;
            }
            .day-row {
                display: flex;
                justify-content: flex-start;  /* Menggeser kotak-kotak ke kiri */
                flex-wrap: wrap;  /* Agar kotak bisa pindah ke baris berikutnya jika sudah penuh */
                gap: 100px;
                margin: 20px auto;
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Mengatur tata letak grid untuk menampilkan kotak
        col_count = 3 # Jumlah kolom per baris
        cols = st.columns(col_count)

        # Membuat kontainer untuk kotak-kotak agar bisa diatur dengan flexbox
        st.markdown('<div class="day-row">', unsafe_allow_html=True)

        # Menampilkan setiap hari dalam kotak individual
        for idx, (day, row) in enumerate(schedule_df.iterrows()):
            # Menentukan kolom untuk setiap kotak
            with cols[idx % col_count]:
                # HTML untuk menampilkan kotak dengan judul dan daftar pekerja
                workers = [f"Worker {i+1}: {row[i]}" for i in range(len(row))]
                worker_list_html = "<br>".join(workers)

                st.markdown(
                    f"""
                    <div class="day-container">
                        <div class="day-title">{day}</div>
                        <div class="worker-list">{worker_list_html}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)  # Menutup div container kotak
        # st.dataframe(schedule_df)
        csv_schedule = schedule_df.to_csv(index = True).encode('utf-8')
        st.download_button(
            label = "Download",
            data= csv_schedule,
            file_name= 'Work Schedule.csv',
            mime='text/csv'
        )

    else:
        st.warning("No schedule generated yet")
    

    if st.button("Back"):
        st.session_state["page"] = "page3"


# Inisialisasi state halaman
if "page" not in st.session_state:
    st.session_state["page"] = "page1"

# Navigasi berdasarkan state
if st.session_state["page"] == "page1":
    page1()
elif st.session_state["page"] == "page2":
    page2()
elif st.session_state["page"] == "page3":
    page3()
elif st.session_state["page"] == "page4":
    page4()