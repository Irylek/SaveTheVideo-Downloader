# SaveTheVideo Downloader
A tool designed to use SaveTheVideo's API to fetch videos from it.

# How it works?

1. You input an URL
2. The tool sends a request to their API with that URL.
3. We receive a ID (for monitoring the task).
4. We are checking the status of the task by sending a request to their API with the ID every second.
5. When it is done instead of the 'active' status, we will receive a JSON response with all the video links fetched.

# What sites are supported?
You can find a full list here: https://savethevideo.com/sites
