import urllib.request
import re
from time import sleep
from tqdm import tqdm

print("\nFetching market results pages...", end=" ")

#gets first 100 listings of AWP | Asiimov (Battle-Scarred)
market_page = str(urllib.request.urlopen("https://steamcommunity.com/market/listings/730/AWP%20%7C%20Asiimov%20%28Battle-Scarred%29/render/?query=&start=0&count=100&country=US&language=english&currency=1").read())

#gets rest of listings of AWP | Asiimov (Battle-Scarred)
results_count = re.findall("total_count\":\d+,\"results_html", market_page)[0].replace("total_count\":", "").replace(",\"results_html", "")
start = 100
while start < int(results_count):
    market_page += str(urllib.request.urlopen("https://steamcommunity.com/market/listings/730/AWP%20%7C%20Asiimov%20%28Battle-Scarred%29/render/?query=&start=" + str(start) + "&count=100&country=US&language=english&currency=1").read())
    start += 100

#creates list containing each listing info
listing_info = re.findall("listingid\":.+?in Game...\"", market_page)

print("Fetching all inspect links...", end=" ")
sleep(1)

#creates list of inspect links pulled from listings
inspect_links = []
for i in range(len(listing_info)):
    listingid = re.findall("\d+\",\"price\"", listing_info[i])[0].replace("\",\"price\"", "")
    asset_id = re.findall(",\"id\":\"\d+\",", listing_info[i])[0].replace(",\"id\":\"", "").replace("\",", "")
    special_D = re.findall("%assetid%D\d+\",", listing_info[i])[0].replace("%assetid%D", "").replace("\",", "")
    inspect_links.append("steam://rungame/730/76561202255233023/+csgo_econ_action_preview%20M" + listingid + "A" + asset_id + "D" + special_D)

print("Fetching all prices...")
sleep(1)

#creates list of prices pulled from listings
price_area = re.findall("market_listing_price_with_fee.+?span>", market_page.replace(",", ""))
prices = []
for i in range(len(price_area)):
    prices.append(re.findall("\$\d+\.\d+", price_area[i]))

print("\nResults parsing done!\n\t- Listings found: " + str(len(listing_info)) + "\n\t- Inspect links generated: " + str(len(inspect_links)) + "\n\t- Prices pulled: " + str(len(prices)) + "\n")
if str(len(listing_info)) == str(len(inspect_links)) == str(len(prices)):
    print("Matching number of listings, inspect links and prices. Moving on...\n")
    sleep(1)
else:
    print("Error! Listing count, inspect link count and price count did not all match. EXITING...\n")
    exit()

for i in tqdm (range (len(listing_info)), desc="Checking " + str(len(listing_info)) + " listings..."):
    item_data = str(urllib.request.urlopen("https://api.csgofloat.com/?url=" + inspect_links[i]).read())
    item_float_val = float(re.findall("0.[0-9]*", re.findall("floatvalue\":0.[0-9]*", item_data)[0])[0])
    price = prices[i][0].replace("$", "")
    if (item_float_val > 0.95) & (float(price) < 100):
        print("\n---- BLACKIIMOV FOUND ----")
        print("\tFloat: " + str(item_float_val) + "\n\tPrice: " + str(prices[i]) + "\n")
        ans = input("Continue? [y/n]: ")
        if ans == "n":
            exit()

input("\nNo underpriced Blackiimovs found in these listings :(\n\nPress ENT to exit...\n")