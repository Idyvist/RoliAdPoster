# RoliAdPoster
#   @desc     Tool for automatically posting ads on Rolimon's with your highest items
#   @author   Idyvist (with some modified code originally from @zentred)
#   @version  1.0
#
import requests, time, threading, ctypes, os
from threading import Thread

# Settings
user_id = ______
roli_data = "______"
roli_verification = "______"
interval = 20

sent = 0
failed = 0
lock = threading.Lock()
os.system('cls')


# Use the Roblox API to return a list of item IDs from your inventory
def get_inv():
    inv_response = requests.get(f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=100").json()
    inv_data = inv_response.get("data", [])
    inventory = [item["assetId"] for item in inv_data if not item.get("isOnHold", False)]
    return inventory


# Sort your inventory from highest to lowest in values, and return up to four of your highest items
def sort_inv(inventory):
    item_details = requests.get("https://api.rolimons.com/items/v1/itemdetails").json()
    item_values = {}

    for item_id in inventory:
        item_data = item_details["items"].get(str(item_id))
        if item_data:
            value = item_data[4]
            item_values[item_id] = value

    sorted_inventory = sorted(inventory, key=lambda item_id: item_values.get(item_id, 0), reverse=True)
    return sorted_inventory[:4]


# Uses the Rolimons API to create a trade ad and send a request
def send():
    global sent, failed
    offer_items = sort_inv(get_inv())
    request_tags = ["any", "upgrade", "downgrade"]
    r = requests.post(
        'https://api.rolimons.com/tradeapi/v1/create',

        cookies={
            '_RoliVerification': roli_verification,
            '_RoliData': roli_data
        },

        json={
            "player_id": user_id,
            "offer_item_ids": offer_items,
            "request_item_ids": [],
            "request_tags": request_tags
        }
    )

    if r.json()['success'] == True:
        print("Trade ad created")
        sent += 1
    else:
        print("Failed to create trade ad")
        failed += 1


def overall():
    while True:
        send()
        time.sleep(60 * interval)


def title():
    while True:
        ctypes.windll.kernel32.SetConsoleTitleW(f'Sent: {sent} | Failed: {failed}')
        time.sleep(1)


Thread(target=title).start()
overall()
