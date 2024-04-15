import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserPreferencesResponse(BaseModel):
    """
    Confirms the creation of user voice customization preferences with a summary of the saved settings.
    """

    preferenceId: str
    message: str


async def create_user_preferences(
    userId: str, voice: str, speed: float, pitch: float, language: str
) -> CreateUserPreferencesResponse:
    """
    Create new user preferences in the database and returns a response with the creation details.

    Args:
        userId (str): The unique identifier of the user setting preferences.
        voice (str): The preferred voice type (e.g., gender, accent).
        speed (float): The speed of the speech output.
        pitch (float): The pitch level of the speech output.
        language (str): The language of the speech output.

    Returns:
        CreateUserPreferencesResponse: Confirms the creation of user voice customization preferences with a summary of the saved settings.
    """
    new_preference = await prisma.models.UserPreference.prisma().create(
        data={
            "userId": userId,
            "voice": voice,
            "speed": speed,
            "pitch": pitch,
            "language": language,
        }
    )
    response = CreateUserPreferencesResponse(
        preferenceId=new_preference.id, message="User preference created successfully."
    )
    return response
