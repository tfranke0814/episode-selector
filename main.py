import requests, os, random
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def main():
    try: # Retrieves spotify access token for client
        res = requests.post("https://accounts.spotify.com/api/token",
                            {"grant_type": "client_credentials", 
                                "client_id": CLIENT_ID, 
                                "client_secret": CLIENT_SECRET
                            })
        res.raise_for_status()
        access_token = res.json()['access_token']
    except Exception as e:
        return print(f"An unexpected eror occurred: {e}")

    # Podcast selection
    choosing = True
    while choosing:
        podcast = input("""What podcast?
    1) Distractable
    2) PowerWash Pals
    3) That's A Good Card | CEDH Podcast
    4) The Foundry - A Transcend UW Podcast
    5) Easy Spanish: Learn Spanish with everyday conversations
                        
Input: """)
        if podcast == "1":
            podcast = "2X40qLyoj1wQ2qE5FVpA7x"
            choosing = False
        elif podcast == "2":
            podcast = "2xcn5dkvU3zlAOWvyz8nLI"
            choosing = False
        elif podcast == "3":
            podcast = "0nLkmjQn71TDBSeGx0KFVn"
            choosing = False
        elif podcast == "4":
            podcast = "5vgKgOA9MZhS0ptiibaaKI"
            choosing = False
        elif podcast == "5":
            podcast = "5uYWauEX01Ixr9NVU8PMaH"
            choosing = False
        else:
            print("Invalid Choice")
    
    try: # Retrieves podcast episode count and returns random episode
        res = requests.get(f"https://api.spotify.com/v1/shows/{podcast}", # type: ignore
                            headers={"Authorization": f"Bearer {access_token}"})
        res.raise_for_status()
        tot_eps = res.json()['total_episodes']
        
        res = requests.get(f"https://api.spotify.com/v1/shows/{podcast}/episodes", # type: ignore
                            params={"offset":random.randint(0, tot_eps-1), "limit":1},
                            headers={"Authorization": f"Bearer {access_token}"})
        res.raise_for_status()
        ep = res.json()['items'][0]
    except Exception as e:
        return print(f"An unexpected eror occurred: {e}")
    
    print(f"""Try this episode: {ep['name']}
Link: {ep['external_urls']['spotify']}
Description: {ep['description']}""")

if __name__ == "__main__":
    main()
