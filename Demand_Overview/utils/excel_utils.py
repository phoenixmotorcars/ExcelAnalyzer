import pandas as pd
import numpy as np
import re

def generate_output_dataframe(df, sheets):
    columns = ["Item No.", "Last Running Total", "Vendor", "Manager"]
    op_df = pd.DataFrame(columns=columns)
    new_row = {"Item No.": "", "Last Running Total": 0, "Vendor": np.nan, "Manager": np.nan}

    previous_item_no = None
    previous_running_total = 0
    for _, row in df.iterrows():
        current_item_no = row['Item No.'] if row['Item No.'] else previous_item_no
        current_running_total = row['Running Total'] if not pd.isna(row['Running Total']) else pd.NA

        if current_item_no and current_item_no != previous_item_no:
            if not pd.isna(previous_running_total) and previous_running_total != 0:
                new_row['Item No.'] = re.sub(r'[^a-zA-Z0-9\s-]', '', previous_item_no).strip()
                new_row['Last Running Total'] = previous_running_total
                op_df = pd.concat([op_df, pd.DataFrame([new_row])], ignore_index=True)

        previous_item_no = current_item_no
        previous_running_total = current_running_total

    # Add the last row
    if previous_running_total != 0:
        new_row['Item No.'] = re.sub(r'[^a-zA-Z0-9\s-]', '', previous_item_no).strip()
        new_row['Last Running Total'] = previous_running_total
        op_df = pd.concat([op_df, pd.DataFrame([new_row])], ignore_index=True)
    
    Items_data = []
    for row in sheets["Items"].iter_rows(values_only=True):  # Get all rows with values
        Items_data.append(row)

    # Assuming the first row contains headers
    item_df = pd.DataFrame(Items_data[1:], columns=Items_data[0])
    
    for idx, row in op_df.iterrows():
        match = item_df[item_df['Item Number Text'] == "x"+row['Item No.']]
        if not match.empty:
            if match['Vendor name'].values[0] is not None:
                op_df.loc[idx, 'Vendor'] = match['Vendor name'].values[0].strip()
            else:
                op_df.loc[idx, 'Vendor'] = "Not Found"
    
    vendors_data = []
    for row in sheets["Vendor Assignments"].iter_rows(values_only=True):  # Get all rows with values
        vendors_data.append(row)

    # Assuming the first row contains headers
    vendors_df = pd.DataFrame(vendors_data[1:], columns=vendors_data[0])
    vendors_df_columns = list(vendors_df.columns)

    for idx, row in op_df.iterrows():
        match = vendors_df[vendors_df[vendors_df_columns[0]] == row['Vendor']]
        if not match.empty:
            if match[vendors_df_columns[1]].values[0] is not None:
                op_df.loc[idx, 'Manager'] = match[vendors_df_columns[1]].values[0].strip()
            else:
                op_df.loc[idx, 'Manager'] = "Not Found"

    print(op_df)

    return op_df