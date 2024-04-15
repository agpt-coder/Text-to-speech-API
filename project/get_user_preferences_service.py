import prisma
import prisma.models
from pydantic import BaseModel


class UserPreferencesResponse(BaseModel):
    """
    This response model represents the structured information of user preferences including voice, speed, pitch, language, which are essential for providing a personalized text-to-speech experience.
    """

    userId: str
    voice: str
    speed: float
    pitch: float
    language: str


async def get_user_preferences() -> UserPreferencesResponse:
    """
    Retrieve user's saved preferences

    This function asynchronously fetches the user preferences from the 'user_preferences' database table,
    assuming the existence of a mechanism to identify the current user, such as through session authentication.
    It then constructs and returns a UserPreferencesResponse object containing these preferences.

    Returns:
        UserPreferencesResponse: This response model represents the structured
        information of user preferences including voice, speed, pitch, language,
        which are essential for providing a personalized text-to-speech experience.

    Example:
        preferences = await get_user_preferences()
        print(preferences)
        > UserPreferencesResponse(userId='1234', voice='en-US-Wavenet-F', speed=1.0, pitch=0.0, language='en-US')
    """
    current_user_id = "example_user_id"
    preferences = await prisma.models.UserPreference.prisma().find_unique(
        where={"userId": current_user_id}
    )
    if preferences:
        response = UserPreferencesResponse(
            userId=preferences.userId,
            voice=preferences.voice,
            speed=preferences.speed,
            pitch=preferences.pitch,
            language=preferences.language,
        )
    else:
        raise ValueError("No preferences found for the current user.")
    return response
