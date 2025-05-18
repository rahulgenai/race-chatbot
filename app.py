import streamlit as st
import time
import math  # Import the math module

def calculate_speed(latitude1, longitude1, latitude2, longitude2, time_difference):
    """
    Calculate speed between two geographic points.

    Args:
        latitude1, longitude1: Initial coordinates in decimal degrees.
        latitude2, longitude2: Final coordinates in decimal degrees.
        time_difference: Time elapsed between the two points in seconds.

    Returns:
        Speed in meters per second (m/s).  Returns 0 if time_difference is 0.
    """
    if time_difference == 0:
        return 0.0  # Avoid division by zero

    R = 6371000  # Radius of the Earth in meters

    lat1_rad = math.radians(latitude1)
    lon1_rad = math.radians(longitude1)
    lat2_rad = math.radians(latitude2)
    lon2_rad = math.radians(longitude2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c  # Distance in meters
    speed = distance / time_difference
    return speed

def main():
    st.title("Speed Display")
    speed_kmh_placeholder = st.empty()
    speed_mph_placeholder = st.empty()
    location_warning_placeholder = st.empty() # For location permission warning
    no_geolocation_placeholder = st.empty()

    # Initial values (will be updated)
    latitude1 = None
    longitude1 = None
    timestamp1 = None

    no_geolocation = False
    location_permission_denied = False

    if 'geolocation' not in st.session_state:
        st.session_state.geolocation = True

    if st.session_state.geolocation:
        try:
            while True:
                # Simulate getting location data (replace with actual data acquisition)
                # In a real-world scenario, you would use a library or API to get
                # GPS data.  This simplified example gets it once.  Streamlit doesn't
                # have a continuously updating location service.
                location_data = st.session_state.get('location_data')
                if location_data is None:
                    # Simulate a one-time location acquisition
                    latitude2 = st.session_state.get('latitude', 34.0522)  # Example: Los Angeles
                    longitude2 = st.session_state.get('longitude', -118.2437)
                    timestamp2 = time.time()
                    st.session_state.location_data = {'latitude': latitude2, 'longitude': longitude2, 'timestamp': timestamp2}
                else:
                    latitude2 = location_data['latitude']
                    longitude2 = location_data['longitude']
                    timestamp2 = location_data['timestamp']

                if latitude1 is not None and longitude1 is not None and timestamp1 is not None:
                    time_difference = timestamp2 - timestamp1
                    speed_mps = calculate_speed(latitude1, longitude1, latitude2, longitude2, time_difference)
                    speed_kmh = speed_mps * 3.6
                    speed_mph = speed_mps * 2.23694
                    speed_kmh_placeholder.text(f"Current Speed: {speed_kmh:.2f} km/h")
                    speed_mph_placeholder.text(f"Current Speed: {speed_mph:.2f} mph")
                    location_warning_placeholder.empty() #clear
                    no_geolocation_placeholder.empty()

                else:
                    speed_kmh_placeholder.text("Waiting for location data...")
                    speed_mph_placeholder.text("")
                    location_warning_placeholder.empty()
                    no_geolocation_placeholder.empty()

                # Update for the next iteration
                latitude1 = latitude2
                longitude1 = longitude2
                timestamp1 = timestamp2
                time.sleep(1) #important

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        no_geolocation_placeholder.error("Geolocation is not supported in this browser.")
        speed_kmh_placeholder.empty()
        speed_mph_placeholder.empty()

if __name__ == "__main__":
    main()
