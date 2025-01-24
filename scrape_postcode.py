import pandas as pd
import requests
import time

# Generate a list of postcodes from 00000 to 99999
num = ["%.5d" % i for i in range(0, 100000)]

def get_postcode(num):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    url = "https://api.pos.com.my/PostcodeWebApi/api/Postcode?Postcode={}".format(num)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for postcode {num}: {e}")
        return None

mergedcode = []
total_postcodes = len(num)

# Loop through each postcode
for index, i in enumerate(num):
    # Log progress
    print(f"Processing postcode {i} ({index + 1}/{total_postcodes})...")

    new = get_postcode(i)
    if new is not None:
        if all(elem in mergedcode for elem in new):
            continue
        else:
            mergedcode.extend(new)

    # Add a delay to avoid hitting rate limits
    time.sleep(1)

# Save the results to a CSV file
df = pd.DataFrame(mergedcode)
df.to_csv("postcode_my.csv", index=False)
print("Data saved to postcode_my.csv")