
import streamlit as st
from enhancements import send_budget_email, get_budget_recommendation
from utils import get_db_path, get_transactions, get_budget

def show_settings_page(user_id):
    st.title("Settings")
    st.subheader("📧 Monthly Email Summary")
    user_email = st.text_input("Enter your email")
    if st.button("Send Summary Email"):
        success, msg = send_budget_email(user_email, "User", user_id)
        st.success(msg) if success else st.error(msg)

    st.subheader("💡 Budget Recommendation")
    st.info(get_budget_recommendation(user_id))

def main():
    user_id = 1  # Simplified for demo purposes
    show_settings_page(user_id)

if __name__ == "__main__":
    main()
