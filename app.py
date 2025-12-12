# Load CSV
hex_df = pd.read_csv("HEX.csv")

# Clean all column names: strip spaces and remove invisible characters
hex_df.columns = hex_df.columns.str.strip().str.replace('\u200b','')

# Now check the column names
st.write("Columns in HEX.csv:", hex_df.columns.tolist())

# Use the correct column for ISO codes
hex_df['ISO3'] = hex_df['ISO3'].str.upper().str.strip()
