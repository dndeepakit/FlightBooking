import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side

st.set_page_config(page_title="Flight Search Planner", layout="centered")

st.title("✈️ Flight Booking Planner (Simplified)")
st.caption("Quick tool for admin teams to generate flight search info instantly.")

# --- INPUT SECTION ---
st.header("🔹 Flight Search Details")

col1, col2 = st.columns(2)
with col1:
    from_city = st.text_input("From City", "Bangalore")
with col2:
    to_city = st.text_input("To City", "Delhi")

col3, col4, col5 = st.columns(3)
with col3:
    dep_date = st.date_input("Departure Date", value=date.today())
with col4:
    ret_date = st.date_input("Return Date (optional)", value=None)
with col5:
    travellers = st.number_input("No. of Travellers", min_value=1, max_value=10, value=1)

travel_class = st.selectbox("Travel Class", ["Economy", "Premium Economy", "Business", "First Class"])

st.divider()

if st.button("Generate Booking Links & Summary"):
    dep_str = dep_date.strftime("%d-%b-%Y")
    ret_str = ret_date.strftime("%d-%b-%Y") if ret_date else "One-way"

    # --- Summary text ---
    st.success("✅ Flight search summary generated successfully!")

    summary = (
        f"**Flight Booking Details**\n"
        f"- From: {from_city}\n"
        f"- To: {to_city}\n"
        f"- Departure: {dep_str}\n"
        f"- Return: {ret_str}\n"
        f"- Travellers: {travellers}\n"
        f"- Class: {travel_class}\n"
    )

    st.markdown(summary)

    # --- Flight Search URLs ---
    st.subheader("🌐 Quick Flight Search Links")

    from_code = from_city.replace(" ", "+")
    to_code = to_city.replace(" ", "+")

    st.markdown(f"""
    - [MakeMyTrip](https://www.makemytrip.com/flights/)
    - [EaseMyTrip](https://www.easemytrip.com/flight.html)
    - [Skyscanner](https://www.skyscanner.co.in/)
    - [Goibibo](https://www.goibibo.com/flights/)
    - [Cleartrip](https://www.cleartrip.com/flights)
    - [Yatra](https://www.yatra.com/flights)
    """)

    # --- Excel Output ---
    wb = Workbook()
    ws = wb.active
    ws.title = "Flight Search"
    bold = Font(bold=True)
    center = Alignment(horizontal="center", vertical="center")
    thin = Side(border_style="thin", color="000000")
    border = Border(top=thin, left=thin, right=thin, bottom=thin)

    ws["A1"] = "Flight Booking Details"
    ws["A1"].font = Font(size=14, bold=True)
    ws.merge_cells("A1:B1")

    info = {
        "From City": from_city,
        "To City": to_city,
        "Departure Date": dep_str,
        "Return Date": ret_str,
        "Travellers": travellers,
        "Class": travel_class,
    }

    row = 3
    for key, val in info.items():
        ws[f"A{row}"] = key
        ws[f"B{row}"] = val
        ws[f"A{row}"].font = bold
        ws[f"A{row}"].alignment = center
        ws[f"B{row}"].alignment = center
        ws[f"A{row}"].border = border
        ws[f"B{row}"].border = border
        row += 1

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    st.download_button(
        label="📥 Download Excel Summary",
        data=buffer,
        file_name=f"Flight_Search_{from_city}_to_{to_city}_{dep_str}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

st.markdown("---")
st.caption("© 2025 Simplified Flight Planner | Built for internal admin use")
