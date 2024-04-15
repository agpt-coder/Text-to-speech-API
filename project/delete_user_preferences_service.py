import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserPreferencesResponse(BaseModel):
    """
    This response model conveys the outcome of attempting to delete a user's preferences, indicating success or failure with a relevant message.
    """

    status: str
    message: str


async def delete_user_preferences(user_id: str) -> DeleteUserPreferencesResponse:
    """
    Delete user's preferences

    Args:
    user_id (str): The unique identifier of the user whose preferences are to be deleted.

    Returns:
    DeleteUserPreferencesResponse: This response model conveys the outcome of attempting to delete a user's preferences, indicating success or failure with a relevant message.
    """
    try:
        deleted_count = await prisma.models.UserPreference.prisma().delete_many(
            where={"userId": user_id}
        )
        if deleted_count == 0:
            return DeleteUserPreferencesResponse(
                status="error", message="No preferences found for user."
            )
        else:
            return DeleteUserPreferencesResponse(
                status="success", message="Preferences deleted successfully."
            )
    except Exception as e:
        return DeleteUserPreferencesResponse(
            status="error", message="An error occurred while deleting preferences."
        )
