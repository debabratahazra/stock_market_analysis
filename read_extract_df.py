import pandas as pd

def read_extract_company(file_path):
    """
    Reads a CSV file and extracts the first 5 rows of the DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame: A DataFrame containing the first 5 rows of the CSV file.
    """
    try:
        df = pd.read_csv(file_path)
        # extract SYMBOL and NAME OF COMPANY from the df
        df = df[['YahooEquiv', 'NAME OF COMPANY']]
        return df
    except Exception as e:
        print(f"Error reading the file: {e}")
        return None