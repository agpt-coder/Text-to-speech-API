import prisma
import prisma.models
from pydantic import BaseModel


class UserPreference(BaseModel):
    """
    Detailed view of the updated preferences.
    """

    voice: str
    speed: float
    pitch: float
    language: str


class UpdateUserPreferencesOutput(BaseModel):
    """
    Confirms the updated user preferences. Echoes back the updated preferences for verification by the client.
    """

    success: bool
    updated_preferences: UserPreference


async def update_user_preferences(
    voice: str, speed: float, pitch: float, language: str
) -> UpdateUserPreferencesOutput:
    """
    Update existing user preferences

    Args:
    voice (str): Preferred voice model for TTS. Eg: 'en-US-Wavenet-F'
    speed (float): Speech speed rate where 1.0 is normal speed. Acceptable range could be between 0.25 and 4.0
    pitch (float): Pitch adjustment. Values might range from -20.0 to 20.0, where 0 is the default.
    language (str): Language code for the speech. Eg: 'en-US'

    Returns:
    UpdateUserPreferencesOutput: Confirms the updated user preferences. Echoes back the updated preferences for verification by the client.
    """
    fake_user_id = "existing-user-uuid-goes-here"
    updated_preference = await prisma.models.UserPreference.prisma().update(
        where={"userId": fake_user_id},
        data={"voice": voice, "speed": speed, "pitch": pitch, "language": language},
    )
    if updated_preference:
        return UpdateUserPreferencesOutput(
            success=True,
            updated_preferences=UserPreference(
                voice=updated_preference.voice,
                speed=updated_preference.speed,
                pitch=updated_preference.pitch,
                language=updated_preference.language,
            ),
        )
    else:
        return UpdateUserPreferencesOutput(
            success=False,
            updated_preferences=UserPreference(
                voice="", speed=0.0, pitch=0.0, language=""
            ),
        )
