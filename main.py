from streamlit_ui import make_ui
from fetch_nse_info import get_nse_data

if __name__ == "__main__":
    
    # Loading and background process
    df = get_nse_data()      
    
    # Make UI
    make_ui(df)
    