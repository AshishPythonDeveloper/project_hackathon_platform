from rest_framework.permissions import BasePermission


class OrganizerUserPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        if not request.user.is_authenticated:
            return False
        if request.method in ["POST", "PUT", "PATCH"]:
            return request.user.user_profile.type == "ORGANIZER"
        if request.method == "DELETE":
            return False
        return True
