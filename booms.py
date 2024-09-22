import requests
import datetime
import time
from colorama import init, Fore, Style

def get_new_token(query_id):
    import json

    # Example payload; adjust based on actual input values
    payload = {
        "start_parameter": "bro1580490871",  # Replace with the actual start parameter
        "telegram_init_data": query_id  # This should be the telegram_init_data you have
    }

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://booms.io",
        "priority": "u=1, i",
        "referer": "https://booms.io/"
    }

    url = "https://api.booms.io/v1/auth/create-session"

    for attempt in range(3):
        print(f"\r{Fore.YELLOW+Style.BRIGHT}Mendapatkan token...", end="", flush=True)
        response = requests.post(url, headers=headers, json=payload)  # Use json=payload instead of data=json.dumps(payload)
        if response.status_code == 200:
            print(f"\r{Fore.GREEN+Style.BRIGHT}Token berhasil dibuat", end="", flush=True)
            response_json = response.json()
            return response_json['token']  # Change to the correct key for your token if needed
        else:
            print(response.json())
            print(f"\r{Fore.RED+Style.BRIGHT}Gagal mendapatkan token, percobaan {attempt + 1}", flush=True)
    print(f"\r{Fore.RED+Style.BRIGHT}Gagal mendapatkan token setelah 3 percobaan.", flush=True)
    return None


def get_user_info(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://booms.io',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get('https://api.booms.io/v1/profiles/self', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        hasil = response.json()
        if hasil['message'] == 'Token is invalid':
            print(f"{Fore.RED+Style.BRIGHT}Token salah, mendapatkan token baru...")
            new_token = get_new_token()  # Provide query_id as needed
            if new_token:
                print(f"{Fore.GREEN+Style.BRIGHT}Token baru diperoleh, mencoba lagi...")
                return get_user_info(new_token)
            else:
                print(f"{Fore.RED+Style.BRIGHT}Gagal mendapatkan token baru.")
                return None
        else:
            print(f"{Fore.RED+Style.BRIGHT}Gagal mendapatkan informasi user")
            return None

def get_balance(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://booms.io/v1/balances',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    for attempt in range(3):
        try:
            response = requests.get('https://api.booms.io/v1/balances', headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"\r{Fore.RED+Style.BRIGHT}Gagal mendapatkan saldo, percobaan {attempt + 1}. Response: {response.json()}", flush=True)
        except requests.exceptions.ConnectionError:
            print(f"\r{Fore.RED+Style.BRIGHT}Koneksi gagal, mencoba lagi {attempt + 1}", flush=True)
        except Exception as e:
            print(f"\r{Fore.RED+Style.BRIGHT}Error: {str(e)}", flush=True)
    print(f"\r{Fore.RED+Style.BRIGHT}Gagal mendapatkan saldo setelah 3 percobaan.", flush=True)
    return None


def play_tap(token, query_list, current_index):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://booms.io',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    
    while True:
        # Prepare payload for tapping
        payload = {
            "taps_count": 50,
            "tapped_from": datetime.datetime.utcnow().isoformat() + "Z"
        }

        response = requests.post('https://api.booms.io/v1/profiles/tap', headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            energy_current_value = result.get('energy_current_value')
            print(f"Added Coins: {result['added_coins']}, New Balance: {result['balance_amount']}, Current Energy: {energy_current_value}")

            if energy_current_value < 5:
                print(f"{Fore.YELLOW}Energy critical ({energy_current_value}), moving to the next query...")
                return current_index + 1  # Move to the next query
            elif energy_current_value < 10:
                print(f"{Fore.YELLOW}Energy low ({energy_current_value}), waiting for 30 seconds...")
                time.sleep(30)  # Wait for 30 seconds
        else:
            print(f"{Fore.RED}Error tapping: {response.json()}")
            break

    return current_index  # Return the current index if there's no energy issue



def clear_task(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://booms.io',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    # Fetch tasks
    response = requests.get('https://api.booms.io/v1/tasks', headers=headers)
    if response.status_code == 200:
        tasks = response.json().get('items', [])
        print("Available Tasks:")
        for task in tasks:
            print(f"ID: {task['id']}, Title: {task['title']}")

        # Example: submit the task with ID 2
        task_id = 2  # Replace this with the desired task ID
        submit_response = requests.post(f'https://api.booms.io/v1/tasks/{task_id}/submit', headers=headers)
        if submit_response.status_code == 200:
            print(f"Task {task_id} submitted successfully.")
            print(f"Response: {submit_response.json()}")
        else:
            print(f"{Fore.RED}Failed to submit task {task_id}: {submit_response.json()}")
    else:
        print(f"{Fore.RED}Failed to retrieve tasks: {response.json()}")

def daily_reward(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://booms.io',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    # Check in for daily reward
    response = requests.post('https://api.booms.io/v1/tasks/daily-reward', headers=headers)
    
    try:
        if response.status_code == 200:
            result = response.json()
            print(f"{Fore.GREEN}Daily reward claimed successfully.")
            print(f"Rewards: {result.get('rewards', 'No rewards')}")
        else:
            # Print the raw response text for debugging
            print(f"Response Code: {response.status_code}")
            print(f"Response Text: {response.text}")  # Print the raw response text

            # Check if the response indicates already checked in
            if response.status_code == 400:  # Adjust based on actual status code for already checked-in
                print(f"{Fore.YELLOW}Already daily check-in.")
            else:
                print(f"{Fore.RED}Failed to claim daily reward: {response.text}")  # Use response.text instead
    except ValueError as e:
        print(f"{Fore.RED}Error parsing JSON: {str(e)}")
        print(f"Raw Response Text: {response.text}")

def upgrade_tap(token, auto_upgrade, auto_refill):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://booms.io',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }

    # Get list of upgrades
    response = requests.get('https://api.booms.io/v1/profiles/boosts', headers=headers)
    
    if response.status_code == 200:
        upgrades = response.json()
        print("Available Upgrades:")
        
        for key, upgrade in upgrades.items():
            if key == "refill_energy":
                print(f"{key.title()}: Current Available: {upgrade['current_available']}, Price: {upgrade['price']} Coins, Cooldown: {upgrade['current_cooldown']} seconds")
            else:
                print(f"{key.title()}: Level {upgrade.get('current_level', 0)}, Price: {upgrade['price']} Coins, Max Level: {upgrade['max_level']}")

        if auto_upgrade:
            # Auto-upgrade energy_limit and multitap
            for upgrade_choice in ['energy_limit', 'multitap']:
                levels_to_upgrade = 1  # Customize the number of levels to upgrade
                if upgrade_choice in upgrades:
                    if 1 <= levels_to_upgrade <= upgrades[upgrade_choice]['max_level'] - upgrades[upgrade_choice]['current_level']:
                        submit_url = f"https://api.booms.io/v1/profiles/boosts/{upgrade_choice}/submit"
                        upgrade_payload = {
                            "levels": levels_to_upgrade
                        }
                        submit_response = requests.post(submit_url, headers=headers, json=upgrade_payload)

                        if submit_response.status_code == 200:
                            print(f"{Fore.GREEN}Successfully upgraded {upgrade_choice} by {levels_to_upgrade} levels.")
                        else:
                            print(f"{Fore.RED}Failed to upgrade {upgrade_choice}: {submit_response.json()}")

        if auto_refill:
            # Auto-refill energy
            if upgrades["refill_energy"]["current_cooldown"] > 0:
                print(f"{Fore.YELLOW}Refill is on cooldown. Wait for {upgrades['refill_energy']['current_cooldown']} seconds.")
            else:
                submit_url = f"https://api.booms.io/v1/profiles/boosts/refill_energy/submit"
                upgrade_payload = {
                    "amount": 1  # Assuming you always refill energy as a single action
                }
                submit_response = requests.post(submit_url, headers=headers, json=upgrade_payload)

                if submit_response.status_code == 200:
                    print(f"{Fore.GREEN}Successfully refilled energy.")
                else:
                    print(f"{Fore.RED}Failed to refill energy: {submit_response.json()}")

    else:
        print(f"{Fore.RED}Failed to retrieve upgrades: {response.json()}")

def countdown_timer(seconds):
    while seconds:
        print(Fore.YELLOW + f"Waiting {seconds} seconds before the next task...", end="\r")
        time.sleep(1)
        seconds -= 1
    print(Fore.YELLOW + "Proceeding to the next task..." + " " * 20)  # Clear line


def main():
    while True:  # Start an infinite loop to rerun the tasks
        # Read query_ids from tgWebAppData.txt
        try:
            with open('tgWebAppData.txt', 'r') as file:
                query_list = [line.strip() for line in file.readlines()]
            print(f"Query List: {query_list}")  # Debug print to check the queries
        except FileNotFoundError:
            print(f"{Fore.RED}File tgWebAppData.txt tidak ditemukan.")
            return

        # Prompt for auto upgrades and refill only once
        auto_upgrade = input("Do you want to automatically upgrade energy_limit and multitap? (y/n): ").strip().lower() == 'y'
        auto_refill = input("Do you want to automatically refill energy? (y/n): ").strip().lower() == 'y'

        for current_index, query_id in enumerate(query_list):
            print(f"Processing query ID: {query_id}")  # Debug print
            
            # Get new token
            token = get_new_token(query_id)
            if token:
                print(f"Token obtained for query ID: {query_id}")  # Debug print
                
                # Get user info
                user_info = get_user_info(token)
                if user_info:
                    print(f"\n{Fore.GREEN}User Info: {user_info}")
                else:
                    print(f"{Fore.RED}Failed to retrieve user info.")

                # Claim daily reward
                daily_reward(token)
                
                # Upgrade tap
                upgrade_tap(token, auto_upgrade, auto_refill)

                # Clear tasks
                clear_task(token)  # Uncomment if you want to clear tasks after claiming daily rewards
                
                # Play tap
                next_index = play_tap(token, query_list, current_index)
                if next_index > current_index:
                    current_index = next_index  # Update to the next index if necessary

            else:
                print(f"{Fore.RED}No token available for query ID: {query_id}, cannot proceed.")

        # Countdown for 1 hour (3600 seconds)
        countdown_timer(3600)  # Call the countdown timer

        # Optional: Ask user if they want to restart the process
        restart = input("Do you want to rerun the automation? (y/n): ").strip().lower()
        if restart != 'y':
            print("Exiting the automation.")
            break  # Exit the loop if the user does not want to restart

if __name__ == "__main__":
    init()  # Initialize colorama
    main()