from __future__ import annotations

from typing import Dict, Set


class PermissionManager:
    """
    Permission system for LIAO AI Assistant.

    Controls which user can execute which actions.
    """

    def __init__(self):
        # role-based permissions
        self.roles: Dict[str, Set[str]] = {
            "admin": {
                "open_app",
                "system_action",
                "file_create",
                "file_delete",
                "network_access",
                "automation_full"
            },
            "user": {
                "open_app",
                "system_action",
                "file_create",
                "network_access"
            },
            "guest": {
                "open_app",
                "network_access"
            }
        }

        # default role
        self.user_roles: Dict[str, str] = {}

    # --------------------------------------------------
    # Role Management
    # --------------------------------------------------
    def set_role(self, user: str, role: str) -> None:
        if role not in self.roles:
            raise ValueError(f"Invalid role: {role}")

        self.user_roles[user] = role

    def get_role(self, user: str) -> str:
        return self.user_roles.get(user, "guest")

    # --------------------------------------------------
    # Permission Check
    # --------------------------------------------------
    def has_permission(
        self,
        user: str,
        action: str
    ) -> bool:

        role = self.get_role(user)
        allowed = self.roles.get(role, set())

        return action in allowed

    # --------------------------------------------------
    # Safe Execution Gate
    # --------------------------------------------------
    def authorize(
        self,
        user: str,
        action: str
    ) -> bool:

        if self.has_permission(user, action):
            return True

        print(
            f"[PERMISSION DENIED] {user} → {action}"
        )

        return False

    # --------------------------------------------------
    # Role Utilities
    # --------------------------------------------------
    def add_permission(
        self,
        role: str,
        permission: str
    ) -> None:

        if role not in self.roles:
            self.roles[role] = set()

        self.roles[role].add(permission)

    def remove_permission(
        self,
        role: str,
        permission: str
    ) -> None:

        if role in self.roles:
            self.roles[role].discard(permission)

    def list_permissions(
        self,
        role: str
    ) -> Set[str]:

        return self.roles.get(role, set())

    # --------------------------------------------------
    # Debug / Info
    # --------------------------------------------------
    def debug_roles(self) -> Dict[str, Set[str]]:
        return self.roles


# ------------------------------------------------------
# Singleton instance
# ------------------------------------------------------
permission_manager = PermissionManager()


# ------------------------------------------------------
# Local Test
# ------------------------------------------------------
if __name__ == "__main__":
    pm = PermissionManager()

    pm.set_role("Sadik", "admin")
    pm.set_role("guest_user", "guest")

    print(pm.has_permission("Sadik", "system_action"))
    print(pm.has_permission("guest_user", "system_action"))

    pm.authorize("guest_user", "open_app")
    pm.authorize("guest_user", "system_action")