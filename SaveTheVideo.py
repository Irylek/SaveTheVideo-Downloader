import requests
import time

headers = {
    'accept': 'application/json',
    'accept-language': 'pl-PL,pl;q=0.6',
    'content-type': 'application/json',
    'origin': 'https://www.savethevideo.com',
    'priority': 'u=1, i',
    'referer': 'https://www.savethevideo.com/',
    'sec-ch-ua': '"Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}

def send_request(url):
    api_url = "https://api.v01.savethevideo.com/tasks"
    payload = {"type": "info", "url": url}

    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code in [200, 202]:
        data = response.json()
        task_id = data.get('id')
        task_href = data.get('href')
        print(f"INFO: The task has been created successfully! ID: {task_id}")

        state = data.get('state')
        if state == 'completed':
            print("SUCCESS: The task was already done. Viewing results....")
            display_results(data)
        else:
            print("INFO: I am starting to monitore the task...")
            monitor_task(task_href)
    else:
        print(f"ERROR: I don't recognize the response. Code: {response.status_code}")
        print(response.text)

def monitor_task(task_href):
    task_url = f"https://api.v01.savethevideo.com{task_href}"

    while True:
        response = requests.get(task_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            state = data.get('state')
            
            if state == 'completed':
                print("SUCCESS: The task is done!")
                display_results(data)
                break
            elif state == 'failed':
                error_message = data.get('error', {}).get('message', 'Nieznany błąd')
                print(f"ERROR: A error occured: {error_message}")
                break
            else:
                print(f"INFO: State: {state} - Waiting....")
                time.sleep(1)
        else:
            print(f"ERROR: There was an error while monitoring the task: {response.status_code}")
            print(response.text)
            break

def display_results(data):
    result = data.get('result', [])

    if not result:
        print("ERROR: No results found for some reason.")
        return

    formats = result[0].get('formats', [])
    
    video_with_audio_found = False
    
    for fmt in formats:
        if fmt.get('vcodec') != 'none' and fmt.get('acodec') != 'none' and fmt.get('ext') == 'mp4':
            if not video_with_audio_found:
                print("\nVideos with audio:\n")
                video_with_audio_found = True
            resolution = fmt.get('resolution', 'Unknown quality')
            url = fmt['url']
            print(f"{resolution}: {url}")
    
    if not video_with_audio_found:
        print("INFO: No videos with audio found. Searching for video without audio...\n")
        for fmt in formats:
            if fmt.get('vcodec') != 'none' and fmt.get('acodec') == 'none' and fmt.get('ext') == 'mp4':
                resolution = fmt.get('resolution', 'Unknown quality')
                url = fmt['url']
                print(f"{resolution}: {url}")

def main():
    url = input("URL: ")
    print()
    
    if url:
        send_request(url)
    else:
        print("That is not a URL.")

if __name__ == "__main__":
    main()