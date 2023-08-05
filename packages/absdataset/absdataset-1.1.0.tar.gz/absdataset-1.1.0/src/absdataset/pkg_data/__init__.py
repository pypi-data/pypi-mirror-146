## Import library ##

import os as __os
try:
    import pandas as __pd
except:
    raise SystemExit("No package found")

## Variables ##
__here = __os.path.abspath(__os.path.dirname(__file__))
CSV_DATA = {
    "ggplay": "googleplaystore.csv",
    "hotel": "hotel_bookings.csv",
}

## Function ##
def load_data(data_name: str):
    """
    Simple data loader
    """
    try:
        if data_name.endswith(".csv"): # CSV file
            return __pd.read_csv(__os.path.join(__here, data_name))
        else:
            raise SystemExit("No data found")
    except:
        raise SystemExit("No data found")


# online data

