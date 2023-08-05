import os as __os
try:
    import pandas as __pd
except:
    raise SystemExit("No package found")

__here = __os.path.abspath(__os.path.dirname(__file__))

GGPLAY = __pd.read_csv(__os.path.join(__here, "googleplaystore.csv"))
HOTELDATA = __pd.read_csv(__os.path.join(__here, "hotel_bookings.csv"))


# online data

