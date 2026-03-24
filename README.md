# 💌 FastAPI Mail Tracker

![Project Logo](./tracker/assets/media/logo.jpg)

## Introduction

Python Mail Tracker is a powerful tool for tracking emails and website views, providing detailed information such as IP addresses, locations, headers, devices, browsers, timestamps, and more. This FastAPI-based application is designed to help you monitor and analyze user interactions with your emails or website, giving you valuable insights into user behavior.

## Features

- Track emails and website views with ease.
- Collect comprehensive information about each interaction.
- Analyze user data to improve your communication and website content.
- FastAPI backend for high-performance tracking.
- Easy-to-use API for integrating tracking into your applications.

## Table of Contents

- [💌 Python Mail Tracker](#-python-mail-tracker)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [Usage](#usage)
    - [API Documentation](#api-documentation)
    - [Configuration](#configuration)
    - [Contributing](#contributing)
    - [License](#license)

## Installation

To get started with Python Mail Tracker, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/MohammadrezaAmani/MailTracker.git
cd MailTracker
```
1- Install the required dependencies:
```bash
pip install -r requirements.txt
```

1. Configure your settings (see Configuration below).

2. Run the FastAPI application:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Vercel Deployment

This project is now Vercel-ready for MVP use.

How storage works:

- Local development: trackers are stored in `tracker/database/data.json`
- Vercel: if `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` are set, the app automatically switches to Upstash Redis

Deployment steps:

1. Push this project to GitHub.
2. Create a new Vercel project and import the repository.
3. Add these environment variables in the Vercel dashboard:

```text
UPSTASH_REDIS_REST_URL=...
UPSTASH_REDIS_REST_TOKEN=...
UPSTASH_REDIS_PREFIX=mailtracker
```

4. Deploy.
5. In Vercel, attach your custom domain such as `seemail.live`.
6. Open your deployed site and create trackers from the dashboard.

After deployment, tracker snippets will use your live domain instead of `127.0.0.1`.

### Usage
Once the application is running, open the dashboard in your browser:

```text
http://127.0.0.1:8000/
```

From there you can:

1. Create a tracker.
2. Copy the generated HTML image snippet.
3. Paste it into the HTML version of your email.
4. Refresh the dashboard to see recorded opens.

If you want to work with the raw API instead, here is a basic example:

```python
import requests

# Replace with your server's address
base_url = 'http://localhost:8000'

# Create a tracker
response = requests.post(f'{base_url}/content', json={
    'name': 'Important News',
    'recipient': 'recipient@example.com',
    'subject': 'Important News',
})

print(response.json())
```
For more advanced usage and API endpoints, please refer to the API Documentation section below.

### API Documentation
For detailed information on available API endpoints and how to use them, please check the API Documentation.

### Configuration
To customize the behavior of Python Mail Tracker, you can edit the config.py file. Here, you can configure database settings, logging, and other application-specific options.

### Contributing
We welcome contributions to make Python Mail Tracker even better! If you'd like to contribute, please follow our Contribution Guidelines.

### License
This project is licensed under the MIT License - see the LICENSE file for details.
