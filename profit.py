import asyncio
import requests
import json
import aiohttp
import matplotlib.pyplot as plt
from datetime import datetime

# Function to fetch real-time cryptocurrency price from the CoinGecko API
async def fetch_real_time_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
            return data[coin_id]["usd"]
    '''response = await requests.get(url, params=params)
    data = json.loads(response.text)
    return data[coin_id]["usd"]'''
def make_decision(real_time_price):
    if real_time_price < 10000:
        return "Buy"
    else:
        return "Hold off"

# Function to calculate profit or loss for a trade
def calculate_profit_loss(buy_price, sell_price, quantity):
    buy_cost = buy_price * quantity
    sell_cost = sell_price * quantity

    profit_loss = sell_cost - buy_cost
    percent_profit_loss = (profit_loss / buy_cost) * 100

    return profit_loss, percent_profit_loss

# Main function to interact with the user and fetch real-time data
prices = []
timestamps = []
# Use a global variable to track whether the loop should continue
running = True
async def main():
    global running  # Use the global running variable
    coin_id = "bitcoin"
    quantity = 2.5
    buy_price = 5000.0

    print("Crypto Decision Maker - Real-Time Version")
    print("Press 'q' to quit.")
    print("Fetching real-time data...\n")
    while running:
        try:
            # Fetch real-time price
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.coingecko.com/api/v3/simple/price", params={"ids": coin_id, "vs_currencies": "usd"}) as response:
                    data = await response.json()

            sell_price = data[coin_id]["usd"]

            # Calculate profit or loss
            profit_loss, percent_profit_loss = calculate_profit_loss(buy_price, sell_price, quantity)

            # Store data for plotting
            prices.append(sell_price)
            timestamps.append(datetime.now())

            # Plot a line graph
            plt.figure(figsize=(10, 6))
            plt.plot(timestamps, prices, marker='o')
            plt.xlabel("Timestamp")
            plt.ylabel("Price (USD)")
            plt.title("Real-Time Price of Bitcoin")
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            

            # Display real-time data and profit/loss
            print(f"Cryptocurrency: {coin_id.upper()}")
            print(f"Real-Time Price: ${sell_price:.2f}")
            print(f"Buy Price: ${buy_price:.2f}")
            print(f"Profit/Loss: ${profit_loss:.2f} ({percent_profit_loss:.2f}%)")
            print(f"Decision: {decision}\n")

            # Wait for 5 seconds before fetching data again
            await asyncio.sleep(5)

        except KeyboardInterrupt:
            print("\nExiting the program.")
            running = False  # Set running to False to stop the loop
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying...\n")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())





    '''while True:
        try:
            # Fetch real-time price
            sell_price = await fetch_real_time_price(coin_id)

            # Calculate profit or loss
            profit_loss, percent_profit_loss = calculate_profit_loss(buy_price, sell_price, quantity)

            # Display real-time data and profit/loss
            print(f"Cryptocurrency: {coin_id.upper()}")
            print(f"Real-Time Price: ${sell_price:.2f}")
            print(f"Buy Price: ${buy_price:.2f}")
            print(f"Profit/Loss: ${profit_loss:.2f} ({percent_profit_loss:.2f}%)")

            # Wait for 5 seconds before fetching data again
            await asyncio.sleep(5)

        except KeyboardInterrupt:
            print("\nExiting the program.")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying...\n")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())'''
