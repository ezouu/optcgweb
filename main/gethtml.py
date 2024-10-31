import requests

url = 'https://www.tcgplayer.com/categories/trading-and-collectible-card-games/one-piece-card-game/price-guides/romance-dawn'

response = requests.get(url)

if response.status_code == 200:
    # Save the HTML content to a file
    with open('downloaded_page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("HTML downloaded and saved as 'downloaded_page.html'")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
