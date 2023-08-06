import json
from typing import Tuple

import requests
from requests import Response
from requests.exceptions import HTTPError

from .logger import Logger


class SoozAccess(object):
    host = ""
    verbose = None

    def __init__(self, name: str, token: str, force_create: bool = True):
        if SoozAccess.host == "":
            raise ValueError(
                "Please provide a host before instanciating with 'SoozAccess.host=\"http://<host>\"'"
            )
        if SoozAccess.verbose == None:
            raise ValueError(
                "Please provide a boolean value to 'verbose' attribute before instanciating"
            )

        self.name = name
        self.token = token
        self.force_create = force_create
        self.session = requests.session()
        Logger.display = SoozAccess.verbose

    def __enter__(self):
        _, r = self.login()
        if r.status_code == 200:
            return self

        if not self.force_create:
            return None

        _, r = self.create_user()

        if r.status_code == 200:
            self.login()
            return self

        return None

    def __exit__(self, *args, **kwargs):
        self.logout()

    @property
    def user_id(self):
        _, r = self.login()
        if r.status_code == 200:
            id = json.loads(r.content.decode("utf-8"))["id"]
            r = self.logout()
            return id

        _, r = self.create_user()
        if r.status_code == 200:
            id = json.loads(r.content.decode("utf-8"))["id"]
            return id

        return None

    def create_user(self, entreprise_id: int = 1) -> Tuple[dict, Response]:
        content = {
            "firstName": self.name,
            "lastName": self.name,
            "sex": "m",
            "username": self.name,
            "email": f"{self.name}@test",
            "enterpriseId": entreprise_id,
            "token": self.token,
            "activatePopup": True,
            "points": 0,
        }
        try:
            r = self.session.post(f"{SoozAccess.host}/users", json=content)
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Create User", r)

        return content, r

    def login(self) -> Tuple[dict, Response]:
        content = {"user": {"identifier": self.name, "token": self.token}}

        try:
            r = self.session.post(f"{SoozAccess.host}/users/login", json=content)
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status(f"*{self.name}* Login", r)

        return content, r

    def logout(self) -> Tuple[dict, Response]:
        try:
            r = self.session.post(f"{SoozAccess.host}/users/logout")
            r.raise_for_status()
        except HTTPError as e:
            pass
        finally:
            self.show_status(f"*{self.name}* Logout", r)

        return {}, r

    def get_themes(self) -> Tuple[dict, Response]:
        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/themes")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Themes", r)

        return content, r

    def get_factors(self, id: int) -> Tuple[dict, Response]:
        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/themes/{id}/factors")
            r.raise_for_status()
        except HTTPError as e:
            SoozAccess.show_error(e)
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Factor", r)

        return content, r

    def put_response(
        self, theme: int, factor: int, value: int, date: str
    ) -> Tuple[dict, Response]:
        content = {
            "responseOptionId": value,
            "roomId": None,
            "period": "day",
            "date": date,
        }

        try:
            r = self.session.put(
                f"{SoozAccess.host}/themes/{theme}/factors/{factor}/responses",
                json=content,
            )
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Insert Response", r)

        return content, r

    def get_responses(self) -> Tuple[dict, Response]:
        content = {}
        try:
            r = self.session.get(f"{SoozAccess.host}/oneshot/responses")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Responses", r)

        return content, r

    def get_groups(self) -> Tuple[dict, Response]:
        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/groups")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Groups", r)

        return content, r

    def post_group(self, name: str, description: str) -> Tuple[dict, Response]:
        if name in [g["group"]["name"] for g in self.get_groups()[0]]:
            Logger.write("Group already exists")
            return None, None

        content = {"name": name, "description": description}

        try:
            r = self.session.post(f"{SoozAccess.host}/groups", json=content)
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Insert Group", r)

        return content, r

    def delete_group(self, id: int) -> Tuple[dict, Response]:
        if id not in [g["group"]["id"] for g in self.get_groups()[0]]:
            Logger.write("Group does not exist")
            return None

        try:
            r = self.session.delete(f"{SoozAccess.host}/groups/{id}")
            r.raise_for_status()
        except HTTPError as e:
            pass
        finally:
            self.show_status("    Remove Group", r)

        return {}, r

    def post_group_invite(self, group: int, ids: list[int]) -> Tuple[dict, Response]:
        content = {"userIds": ids}

        try:
            r = self.session.post(
                f"{SoozAccess.host}/groups/{group}/invite", json=content
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Invite to Group", r)

        return content, r

    def put_group_invitation(self, group: int) -> Tuple[dict, Response]:
        content = {"status": "accepted"}

        try:
            r = self.session.put(
                f"{SoozAccess.host}/groups/{group}/invitation", json=content
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        finally:
            self.show_status("    Accept Group Invitation", r)

        return {}, r

    def get_oneshot(self) -> Tuple[dict, Response]:
        content = {}
        try:
            r = self.session.get(f"{SoozAccess.host}/oneshot")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    One Shot", r)

        return content, r

    def remove_groups(self):
        for g in self.get_groups()[0]:
            self.delete_group(g["group"]["id"])

    def show_status(self, text: str, r: Response):
        Logger.write(f"[{'API':10s}] {text:30s} [{r.status_code}] {r.reason}")

    @classmethod
    def prepare_users(cls, group_name: str, users: list[str]):
        id_list = [SoozAccess(name, name).user_id for name in users]

        # create group invitations from admin account
        with SoozAccess("admin_dev", "admin_dev") as admin:
            admin.remove_groups()

            content, _ = admin.post_group(group_name, "")
            group_id = content["groupId"]
            admin.post_group_invite(group_id, id_list)

        # accepts invitations from admin
        for name in users:
            with SoozAccess(name, name) as user:
                user.put_group_invitation(group_id)
