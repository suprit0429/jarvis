# internet_speed.py
import speedtest

def get_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # convert to Mbps
        upload = st.upload() / 1_000_000      # convert to Mbps
        ping = st.results.ping
        return f"Download: {download:.2f} Mbps, Upload: {upload:.2f} Mbps, Ping: {ping:.0f} ms"
    except Exception as e:
        return "Unable to fetch internet speed right now."
