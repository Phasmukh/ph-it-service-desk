
import streamlit as st
import pandas as pd
import random
import os
from datetime import datetime

st.set_page_config(
    page_title="PH IT Services - Internal Service Desk Portal",
    page_icon="💻",
    layout="wide"
)

CSV_FILE = "tickets.csv"

st.title("💻 PH IT Services")
st.caption("Internal Service Desk Portal")

if os.path.exists(CSV_FILE):
    tickets = pd.read_csv(CSV_FILE)
else:
    tickets = pd.DataFrame(columns=[
        "Ticket ID","Created","Employee","Department","Device",
        "Issue","Priority","Description","Status"
    ])

total = len(tickets)
open_count = len(tickets[tickets["Status"]=="Open"]) if not tickets.empty else 0
high = len(tickets[tickets["Priority"]=="High"]) if not tickets.empty else 0
critical = len(tickets[tickets["Priority"]=="Critical"]) if not tickets.empty else 0

c1,c2,c3,c4 = st.columns(4)
c1.metric("📂 Total", total)
c2.metric("🟢 Open", open_count)
c3.metric("🟠 High", high)
c4.metric("🔴 Critical", critical)

st.divider()
st.subheader("Create Incident")

left,right = st.columns(2)

with left:
    employee = st.text_input("Employee Name")
    department = st.selectbox("Department",
        ["Finance","HR","IT","Sales","Operations","Warehouse","Management"])
    device = st.selectbox("Device",
        ["Laptop","Desktop","Mobile Phone","Printer"])

with right:
    issue = st.selectbox("Issue Category",
        ["Password Reset","Outlook","Microsoft Teams",
         "VPN","Printer","Network","Windows Login","Hardware"])
    priority = st.selectbox("Priority",
        ["Low","Medium","High","Critical"])

description = st.text_area("Incident Description", height=120)

guides = {
    "Password Reset":[
        "Verify user identity","Unlock account if required",
        "Reset password","Ask user to sign in again"],
    "VPN":[
        "Check internet connection","Restart VPN client",
        "Verify credentials","Confirm MFA","Test another network"],
    "Outlook":[
        "Restart Outlook","Check internet connection",
        "Verify mailbox","Repair Microsoft Office"],
    "Printer":[
        "Check printer power","Clear print queue",
        "Restart Print Spooler","Print test page"],
    "Microsoft Teams":[
        "Restart Teams","Sign out/in","Clear Teams cache"],
    "Network":[
        "Check cable/Wi-Fi","Run network diagnostics",
        "Restart adapter"],
    "Windows Login":[
        "Check username","Check Caps Lock",
        "Unlock/reset account"],
    "Hardware":[
        "Check connections","Restart device",
        "Test with another device"]
}

if st.button("Create Ticket", use_container_width=True):
    ticket_id = f"INC-{random.randint(100000,999999)}"

    new_ticket = {
        "Ticket ID":ticket_id,
        "Created":datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Employee":employee,
        "Department":department,
        "Device":device,
        "Issue":issue,
        "Priority":priority,
        "Description":description,
        "Status":"Open"
    }

    tickets = pd.concat([tickets, pd.DataFrame([new_ticket])], ignore_index=True)
    tickets.to_csv(CSV_FILE,index=False)

    st.success(f"Ticket {ticket_id} created successfully!")

    st.subheader("First-Line Troubleshooting")
    for step in guides.get(issue,["Perform standard troubleshooting","Escalate if unresolved"]):
        st.write(f"✅ {step}")

    st.subheader("Service Desk Notes")
    st.code(f"""Ticket: {ticket_id}

Employee: {employee}
Department: {department}
Device: {device}
Issue: {issue}
Priority: {priority}
Status: Open

Description:
{description}
""")

st.divider()
st.subheader("Current Tickets")

search = st.text_input("Search by Employee or Ticket ID")

display = tickets.copy()

if search:
    s = search.lower()
    display = display[
        display["Employee"].astype(str).str.lower().str.contains(s) |
        display["Ticket ID"].astype(str).str.lower().str.contains(s)
    ]

st.dataframe(display, use_container_width=True, hide_index=True)

if not tickets.empty:
    st.download_button(
        "⬇️ Download Tickets CSV",
        tickets.to_csv(index=False),
        "tickets.csv",
        "text/csv"
    )
