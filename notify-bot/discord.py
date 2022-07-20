#!/usr/bin/env python3
# Uptime bot for Discord Notification
# Usage: python3 discord.py <gh_issue_number> <discord_webhook_url>
from sys import argv
from gh_issue import get_issue
import requests


def discord_notification(discord_webhook_url: str, gh_issue_number: str) -> None:
    """ Send notification via Discord
    Args:
        discord_webhook_url (str): Discord Webhook URL
        gh_issue_number (str): GitHub Issue Number
    """
    # To generate a Webhook URL in Discord:
    # https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
    title, created_at, description, label = get_issue(gh_issue_number)
    colors = {
        "maintenance": 16763904,
        "status": 14177041,
        "others": 1127128
    }
    Message = {
        "username": "Uptime Bot",
        "embeds": [
            {
                "title": title,
                "description": description,
                "timestamp": created_at,
                "color": colors[label],
            }
        ]
    }
    requests.post(discord_webhook_url, json=Message)


if __name__ == "__main__":
    discord_notification(argv[2], argv[1])
