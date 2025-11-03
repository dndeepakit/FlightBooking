import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="Flight Options Generator", layout="wide")

st.title("✈️ Flight Options Table Generator")
st.write("Quickly prepare flight comparison tables for employee bookings.")

# ---- INPUT SECTION ----
st.header("🔹 Enter Trip Details")

col1, col2, col3, col4 = st.columns(4)
with col1:
    dep_city = st.text_input("Departure City", "Delhi")
with col2:
    arr_city = st.text_input("Arrival City", "Bangalore")
with col3:
    dep_date = st.date_input("Departure Date")
with col4:
    ret_date = st.date_input("Return Date")

# format dates
dep_date_str = dep_date.strftime("%d/%m/%Y")
ret_date_str = ret_date.strftime("%d/%m/%Y")

st.divider()

# ---- ADD FLIGHT OPTIONS ----
st.header("🛫 Enter Flight Options")
st.caption("Add as many options as you want (each option = outbound + return pair).")

num_options = st.number_input("Number of Options", min_value=1, max_value=20, value=3)

data = []

for i in range(num_options):
    st.subheader(f"Option {i+1}")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        outbound_airline = st.text_input(f"Outbound Airline (Option {i+1})", "Air India (Economy)")
    with c2:
        outbound_dep_time = st.text_input(f"Outbound Departure Time (Option {i+1})", "18:00")
    with c3:
        outbound_arr_time = st.text_input(f"Outbound Arrival Time (Option {i+1})", "21:00")
    with c4:
        outbound_price = st.text_input(f"Round Trip Cost (Option {i+1})", "16,000")

    c5, c6, c7, c8 = st.columns(4)
    with c5:
        return_airline = st.text_input(f"Return Airline (Option {i+1})", "Air India (Economy)")
    with c6:
        return_dep_time = st.text_input(f"Return Departure Time (Option {i+1})", "14:00")
    with c7:
        return_arr_time = st.text_input(f"Return Arrival Time (Option {i+1})", "16:55")
    with c8:
        _ = st.text_input(f"(Optional) Notes (Option {i+1})", "")

    data.append({
        "Option": f"Option {i+1}",
        "Outbound Airline": outbound_airline,
        "Return Airline": return_airline,
        "Outbound Departure Time": outbound_dep_time,
        "Outbound Arrival Time": outbound_arr_time,
        "Return Departure Time": return_dep_time,
        "Return Arrival Time": return_arr_time,
        "Round Trip Cost": outbound_price
    })

st.divider()

# ---- GENERATE OUTPUT ----
if st.button("Generate Flight Table"):
    if not dep_city or not arr_city:
        st.error("Please fill in all trip details.")
    else:
        df = pd.DataFrame(data)

        st.success("✅ Flight Options Generated Successfully!")
        st.subheader(f"Flight Options For {dep_date.strftime('%d %b %Y')} - {ret_date.strftime('%d %b %Y')}")
        
        # ---- Display formatted table ----
        st.dataframe(df, use_container_width=True)

        # ---- Excel download ----
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Flight Options")
        st.download_button(
            label="📥 Download as Excel",
            data=buffer,
            file_name=f"Flight_Options_{dep_date_str}_to_{ret_date_str}.xlsx",
            mime="application/vnd.ms-excel"
        )

        # ---- Copyable Text Output ----
        st.subheader("📝 Copyable Text Summary")
        text_output = f"**Flight Options For {dep_date.strftime('%d %b %Y')} - {ret_date.strftime('%d %b %Y')}**\n\n"
        text_output += f"**From {dep_city} → {arr_city} and Return**\n\n"

        for i, row in df.iterrows():
            text_output += (
                f"**{row['Option']}**\n"
                f"Outbound: {row['Outbound Airline']} | Depart: {row['Outbound Departure Time']} | Arrive: {row['Outbound Arrival Time']}\n"
                f"Return: {row['Return Airline']} | Depart: {row['Return Departure Time']} | Arrive: {row['Return Arrival Time']}\n"
                f"Round Trip Cost: ₹{row['Round Trip Cost']}\n\n"
            )

        st.text_area("Copy this summary:", text_output, height=250)

        # ---- Add search URLs ----
        st.subheader("🌍 Quick Search Links")
        st.markdown(f"""
        - [MakeMyTrip](https://www.makemytrip.com/flights)
        - [Skyscanner](https://www.skyscanner.co.in/)
        - [EaseMyTrip](https://www.easemytrip.com/)
        - [Goibibo](https://www.goibibo.com/)
        - [ClearTrip](https://www.cleartrip.com/flights)
        - [Yatra](https://www.yatra.com/flights)
        """)

st.markdown("---")
st.caption("© 2025 Flight Options Tool | Built for internal use by Admin Team")
