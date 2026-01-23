import requests, os, random, time
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# To add to this visit the Spotify podcast in your browser
# You can find the corresponding ID in the url link
#
# For example, the url for The Foundry is
# `https://open.spotify.com/show/5vgKgOA9MZhS0ptiibaaKI`
# Note: the ID is at the end, after the `/show/`
podcast_mapping = {
    "1": "2X40qLyoj1wQ2qE5FVpA7x", # Distractible
    "2": "2xcn5dkvU3zlAOWvyz8nLI", # Markiplier // PowerWash Pals
    "3": "0nLkmjQn71TDBSeGx0KFVn", # That's a Good Card
    "4": "5vgKgOA9MZhS0ptiibaaKI", # The Foundry
    "5": "5uYWauEX01Ixr9NVU8PMaH", # Easy Spanish
    "6": "2KYyAGSPNJKUKCuqURpDuV" # How to Spanish
}

# The prompt the user sees in the CLI
# Ensure it matches with your mapping above!!
input_string = """
What podcast?
    1) Distractable
    2) PowerWash Pals
    3) That's A Good Card | CEDH Podcast
    4) The Foundry - A Transcend UW Podcast
    5) Easy Spanish: Learn Spanish with everyday conversations
    6) How To Spanish Podcast
                        
Input: """

# The main function that prompts the user and then calls the Spotify API
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
        podcast = input(input_string)
        if podcast_mapping.get(podcast):
            choosing = False
            podcast_id = podcast_mapping.get(podcast)
        else: 
            print("Invalid Choice")
            time.sleep(1)
    
    try: # Retrieves podcast episode count and returns random episode
        res = requests.get(f"https://api.spotify.com/v1/shows/{podcast_id}", # type: ignore
                            headers={"Authorization": f"Bearer {access_token}"})
        res.raise_for_status()
        tot_eps = res.json()['total_episodes']
        
        res = requests.get(f"https://api.spotify.com/v1/shows/{podcast_id}/episodes", # type: ignore
                            params={"offset":random.randint(0, tot_eps-1), "limit":1},
                            headers={"Authorization": f"Bearer {access_token}"})
        res.raise_for_status()
        ep = res.json()['items'][0]
    except Exception as e:
        return print(f"An unexpected eror occurred: {e}")
    
    print(f"""
Try this episode: {ep['name']}
          
Link: {ep['external_urls']['spotify']}

Description: {ep['description']}""")

if __name__ == "__main__":
    main()
