import os
import json


def get_files(group_id: str) -> list[str]:
    """
    A method to get all files within a given group

    Parameters
    ----------
    group_id : str
        The group in which we want content from

    Returns
    -------
    list[str]
        Ffile names within a given group
    """

    path = f'files/{group_id}'
    elements = os.listdir(path)

    files = []
    for element in elements:
        if os.path.isfile(os.path.join(path, element)):
            files.append(element)

    return files


def get_group_ids(user_id: str) -> list[str]:
    """
    A method to get all groups of a user

    Parameters
    ----------
    user_id : str
        The id of the user we want to get the groups from

    Returns
    -------
    list[str]
        The ids of the groups the user are part of
    """

    with open('data/groups.json', 'r') as file:
        data = json.load(file)
        groups = []

        if user_id not in data:
            return groups

        for group in data[user_id]:
            groups.append(group['id'])

        return groups


def get_permissions(user_id: str, group_id: str) -> dict:
    """
    A method to get all group permissions of a user

    Parameters
    ----------
    user_id : str
        The id of the user we want to get the group permissions from
    group_id : str
        The id of the group we want to get permissions from

    Returns
    -------
    dict
        The given permissions for the user withihn the given group
    """

    with open('data/groups.json', 'r') as file:
        data = json.load(file)
        permissions = {}

        if user_id not in data:
            return permissions

        for group in data[user_id]:
            if group['id'] == group_id:
                permissions = group['permissions']
                break

        return permissions
