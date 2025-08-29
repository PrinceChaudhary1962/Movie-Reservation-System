import streamlit as st
import requests

# ⚠️ Replace with your current ngrok public URL from Colab
API_URL = "https://f889afb23a5b.ngrok-free.app"

st.set_page_config(page_title="🎬 Movie Reservation System", layout="centered")
st.title("🎬 Movie Reservation System")

# --- API functions ---
def get_movies():
    try:
        response = requests.get(f"{API_URL}/movies")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch movies: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

def reserve_seat(user, movie_id):
    payload = {"user": user, "movie_id": movie_id}
    try:
        response = requests.post(f"{API_URL}/reserve", json=payload)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json().get("detail", "Reservation failed"))
    except Exception as e:
        st.error(f"Error: {e}")

def get_reservations(movie_id):
    try:
        response = requests.get(f"{API_URL}/reservations/{movie_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"reservations": []}
    except:
        return {"reservations": []}

# --- UI ---
movies = get_movies()

if movies:
    st.subheader("Available Movies")
    for movie in movies:
        movie_id = movie["id"]
        title = movie["title"]
        seats = movie["seats"]

        with st.expander(f"{title} 🎟️ ({seats} seats left)"):
            user_name = st.text_input(
                f"Enter your name to reserve a seat in {title}", key=f"user_{movie_id}"
            )
            if st.button(f"Reserve Seat in {title}", key=f"btn_{movie_id}"):
                if user_name.strip():
                    reserve_seat(user_name, movie_id)
                else:
                    st.warning("Please enter your name")

            reservations = get_reservations(movie_id)
            if reservations["reservations"]:
                st.write("👥 Reservations:", ", ".join(reservations["reservations"]))
            else:
                st.write("No reservations yet.")
