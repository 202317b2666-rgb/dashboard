import streamlit as st

st.title("Interactive World Map - Click Popup")

country_selected = st.selectbox("Simulate click country", ["India", "USA", "China"])

if st.button(f"Show Popup for {country_selected}"):
    st.components.v1.html(f"""
    <div style="
        position:fixed;
        top:50%;
        left:50%;
        transform:translate(-50%, -50%);
        width:400px;
        height:300px;
        background-color:white;
        border:2px solid #000;
        box-shadow:0 4px 20px rgba(0,0,0,0.3);
        z-index:999;
        padding:20px;
    ">
        <h3>{country_selected} Details</h3>
        <p>This is a floating popup window!</p>
        <p>You can later add charts and indicators here.</p>
    </div>
    """, height=0)
