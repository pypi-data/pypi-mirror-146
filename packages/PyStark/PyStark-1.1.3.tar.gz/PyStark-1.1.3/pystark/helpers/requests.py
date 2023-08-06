# # PyStark - Python add-on extension to Pyrogram
# # Copyright (C) 2021-2022 Stark Bots <https://github.com/StarkBotsIndustries>
# #
# # This file is part of PyStark.
# #
# # PyStark is free software: you can redistribute it and/or modify
# # it under the terms of the GNU General Public License as published by
# # the Free Software Foundation, either version 3 of the License, or
# # (at your option) any later version.
# #
# # PyStark is distributed in the hope that it will be useful,
# # but WITHOUT ANY WARRANTY; without even the implied warranty of
# # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# # GNU General Public License for more details.
# #
# # You should have received a copy of the GNU General Public License
# # along with PyStark. If not, see <https://www.gnu.org/licenses/>.
#
#
# import httpx
#
#
# class HTTPError(Exception):
#     """Raised if HTTP Request to the url fails"""
#     pass
#
#
# class Requests:
#     """Send asynchronous or synchronous requests to any url (generally api) which returns json response using Httpx"""
#
#     def sync_get(self, url: str, params: dict = None) -> dict[str]:
#         """
#         Do a synchronous get request to any url using Httpx.
#
#         Parameters:
#
#         url (str) - The url to which you want to request.
#
#         Returns:
#
#         dict - JSON type response from the url
#
#         Raises:
#
#         HTTPError - Raised if the client is unable to interact with the API
#         """
#         return self._sync_request(url, "get")
#
#     def sync_post(self, url: str, params: dict = None) -> dict[str]:
#         """
#         Do a synchronous post request to any url using Httpx.
#
#         Parameters:
#
#         url (str) - The url to which you want to request.
#
#         Returns:
#
#         dict - JSON type response from the url
#
#         Raises:
#
#         HTTPError - Raised if the client is unable to interact with the API
#         """
#         return self._sync_request(url, "post")
#
#     @staticmethod
#     def _sync_request(url: str, method: str, params: dict = None) -> dict[str]:
#         with httpx.Client() as client:
#             if method == "get":
#                 response = client.get(url, params=params)
#             elif method == "post":
#                 response = client.post(url)
#             else:
#                 print("Only GET or POST requests are allowed")
#                 return {}
#             if not response.is_success:
#                 raise HTTPError(response)
#             return response.json()
#
#     @staticmethod
#     async def async_request(url: str) -> dict[str]:
#         """
#         Do an asynchronous request to any url using HTTPX.
#
#         Parameters:
#
#         url (str) - The url to which you want to request.
#
#         Returns:
#
#         dict - JSON type response from the url
#
#         Raises:
#
#         HTTPError - Raised if the client is unable to interact with the API
#         """
#         async with httpx.AsyncClient() as client:
#             client: httpx.AsyncClient
#             response = await client.get(url)
#             if not response.is_success:
#                 raise HTTPError(response)
#             return response.json()
#
#     @staticmethod
#     async def request(url: str) -> dict[str]:
#         """Alias of `pystark.helpers.Requests.async_request`"""
#         return await Requests.async_request(url)


# INIT

# from .requests import Requests


# Future Roadmap/Features

# ➥ admins_only decorator to allow only admins to use some commands
#
# ➥ List commands in help message.
#
# ➥ Userbot support (maybe)
#
# ➥ Log to TG in real-time with multiple facilities
#
# ➥ Special functions to execute shell commands properly
#
# ➥ Both synchronous and asynchronous http requests functions using httpx to ease things even more.
#
# ➥ Ease Inline Queries
#
# ➥ Ease buttons creation
#
# ➥ Buttons in default plugins
#
# ➥ Default inline queries
#
# ➥ MongoDB support (probably not)
#
# ➥ Paginate buttons
#
# ➥ pystark.helpers for more such useful helpers
#
# ➥ Your opinion (can be provided in @StarkBotsChat)


# mkdocs.yml
# - helpers / requests.md

# changelog
#     - Added helpers for sync and async http requests in `pystark.helpers.requests`

# docs/
# <br>
#
# - **requests** - Send http requests synchronously or asynchronously. [Read More Here](/helpers/requests)
