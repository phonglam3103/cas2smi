import argparse
try:
    import requests
except ImportError:
    raise ImportError("The requests module is required. Run 'pip install requests' and try again.")
import pandas as pd
import os

def cas_to_smiles_pubchem(cas):
    """
    Fetches the SMILES representation for a CAS number from PubChem.
    
    Parameters:
    cas (str): The CAS number of the compound.
    
    Returns:
    str: The SMILES string if found, or an error meassage.
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{cas}/property/IsomericSMILES/JSON"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        smiles = data['PropertyTable']['Properties'][0]['IsomericSMILES']
        return smiles
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
    except (KeyError, IndexError):
        return "CAS number not found or SMILES not available"

def load_data(input_file, is_excel):
    """
    Loads data from an Excel or CSV file, dropping duplicates and stripping whitespace.
    
    Parameters:
    input_file (str): Path to the input file.
    is_excel (bool): If True, the input file is an Excel file; if False, it’s a CSV.
    
    Returns:
    pd.DataFrame: The cleaned DataFrame with columns 'Name' and 'CAS'.
    """
    if is_excel:
        df = pd.read_excel(input_file, usecols='A:B', names=['Name', 'CAS'])
    else:
        with open(input_file, 'r') as f:
            first_line = f.readline().strip()
        if ',' in first_line: sep = ','
        else: sep = '\t'
        df = pd.read_csv(input_file, names=['Name', 'CAS'], sep=sep)

    df.dropna(inplace=True)
    df.drop_duplicates(subset='CAS', inplace=True)
    df['CAS'] = df['CAS'].str.strip()
    return df.reset_index(drop=True)

def main():
    help_text = """Convert CAS numbers in a file to SMILES strings using PubChem.
    The input file should be an Excel or CSV file without header. 
    To avoid ambiguity, only comma-separated or tab-separated files are supported.

    Example file format:
        o-Tolylboronic acid, 16419-60-6
        3-Hydroxyphenylboronic acid, 87199-18-6

    Example Excel file format (columns A and B - no header):
        o-Tolylboronic acid          |   16419-60-6
        3-Hydroxyphenylboronic acid  |   87199-18-6

    Example usage:
        cas2smi.py input.csv
        cas2smi.py input.xls -xls
"""
    parser = argparse.ArgumentParser(description=help_text, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input_file", type=str, help="Path to the input file (Excel or CSV)")
    parser.add_argument("-xls", action="store_true", help="Flag indicating the input file is an Excel file (.xls or .xlsx)")

    args = parser.parse_args()
    if os.path.exists(args.input_file) == False:
        print(f"File {args.input_file} not found.")
        return
    input_file = args.input_file
    is_excel = args.xls

    # Load the data
    df = load_data(input_file, is_excel)

    # Apply the SMILES conversion function
    df['SMILES'] = df['CAS'].apply(cas_to_smiles_pubchem)

    # Save the resulting DataFrame to a CSV file
    output_file = f"{input_file.split('.')[0]}_SMILES.csv"
    df.to_csv(output_file, index=False, header=False)
    print(f"Processed file saved to {output_file}")

if __name__ == "__main__":
    main()
