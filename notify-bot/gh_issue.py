#!/usr/bin/env python3
# Extract Message from GH Issue

import requests
from datetime import datetime
import re


def get_issue(issue_number):
    """ Returns formatted description and label from an issue

    Args:
        issue_number: GitHub Issue Number

    Returns:
        description: Notification Body
        label: Issue Label
    """
    # TODO: Type hinting for the function
    endpoint = "https://api.github.com/repos/kalagiri-bot/status/issues/"
    gh_issue = requests.get(f"{endpoint}{issue_number}").json()

    labels = []
    for val in gh_issue["labels"]:
        labels.append(val["name"])

    if "maintenance" in labels:
        to_format, from_format = "%d-%b-%Y %I:%M %p", "%Y-%m-%dT%H:%M:%S%z"
        comment = re.findall(
            r"(<!--.*?-->)", gh_issue["body"], flags=re.DOTALL)[0]
        message = re.sub(r"(<!--.*?-->)", "",
                         gh_issue["body"], flags=re.DOTALL).strip()
        comment = comment.replace(
            "<!--\r\n", "").replace("\r\n-->", "").split("\r\n")
        start = re.sub(r"\.[0-9][0-9][0-9]", "",
                       comment[0].replace("start: ", ""), flags=re.DOTALL).strip()
        end = re.sub(r"\.[0-9][0-9][0-9]", "",
                     comment[1].replace("end: ", ""), flags=re.DOTALL).strip()
        expectedDown = comment[2].replace("expectedDown: ", "")
        start = datetime.strptime(start, from_format).strftime(to_format)
        end = datetime.strptime(end, from_format).strftime(to_format)
        description = f"**`{expectedDown}`** will be down from `{start}` \
            to `{end}`\n{message}"
        label = "maintenance"

    elif "status" in labels:
        description = gh_issue["body"]
        label = "status"

    else:
        description = gh_issue["body"]
        label = "others"

    # TODO: This could've been a dictionary
    return (gh_issue["title"],
            gh_issue["created_at"],
            description,
            label)
