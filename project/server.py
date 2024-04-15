import logging
from contextlib import asynccontextmanager
from typing import Optional

import project.authenticate_user_service
import project.convert_text_to_speech_service
import project.create_user_preferences_service
import project.delete_user_preferences_service
import project.get_user_preferences_service
import project.refresh_token_service
import project.retrieve_speech_output_service
import project.update_user_preferences_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Text-to-Speech API",
    lifespan=lifespan,
    description="Based on the questions and responses during the interview, the task involves creating a text-to-speech (TTS) endpoint with specific requirements: 1. **Input Handling**: The endpoint must accept both plain text and SSML (Speech Synthesis Markup Language) formatted input. This dual-input capability allows for a broader range of speech expressions, from simple text conversion to complex speech patterns that include pauses, emphasis, and audio adjustments. 2. **Speech Conversion**: The core functionality is to convert the provided input text into natural-sounding speech audio. It involves selecting a TTS library that can handle both input types efficiently and produce high-quality audio output. Based on the interview, potential libraries include `gTTS` for simplicity and access to Google's TTS engine, `pyttsx3` for offline capabilities, or `aws-polly` for advanced features and natural voice options. 3. **Customization Features**: The endpoint must offer customization options for voice (e.g., gender, accent), speed, pitch, and other parameters. This level of customization allows users to tailor the speech output to match their preferences or application requirements, enhancing the overall user experience. 4. **Output Format**: The generated audio should be returned in a specified format, with MP3 being the preferred format due to its balance of sound quality and file size. This flexibility ensures that the TTS service can be used in a variety of applications, including those that require specific audio formats for compatibility or quality reasons. **Technical Implementation**: The service will be implemented using Python and FastAPI, leveraging FastAPI's asynchronous capabilities to handle speech synthesis operations efficiently. PostgreSQL, in conjunction with Prisma as the ORM, will be used to store and manage user preferences and possibly cache generated speech files for frequent requests. Special consideration will be given to security, error handling, and integration with the frontend to ensure a robust and scalable service.",
)


@app.post(
    "/auth/refresh", response_model=project.refresh_token_service.RefreshTokenResponse
)
async def api_post_refresh_token(
    existing_token: str,
) -> project.refresh_token_service.RefreshTokenResponse | Response:
    """
    Refresh user's JWT token
    """
    try:
        res = await project.refresh_token_service.refresh_token(existing_token)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user/preferences",
    response_model=project.create_user_preferences_service.CreateUserPreferencesResponse,
)
async def api_post_create_user_preferences(
    userId: str, voice: str, speed: float, pitch: float, language: str
) -> project.create_user_preferences_service.CreateUserPreferencesResponse | Response:
    """
    Create new user preferences
    """
    try:
        res = await project.create_user_preferences_service.create_user_preferences(
            userId, voice, speed, pitch, language
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/user/preferences",
    response_model=project.delete_user_preferences_service.DeleteUserPreferencesResponse,
)
async def api_delete_delete_user_preferences(
    user_id: str,
) -> project.delete_user_preferences_service.DeleteUserPreferencesResponse | Response:
    """
    Delete user's preferences
    """
    try:
        res = await project.delete_user_preferences_service.delete_user_preferences(
            user_id
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/preferences",
    response_model=project.update_user_preferences_service.UpdateUserPreferencesOutput,
)
async def api_put_update_user_preferences(
    voice: str, speed: float, pitch: float, language: str
) -> project.update_user_preferences_service.UpdateUserPreferencesOutput | Response:
    """
    Update existing user preferences
    """
    try:
        res = await project.update_user_preferences_service.update_user_preferences(
            voice, speed, pitch, language
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/login",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Authenticate user and return JWT token
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/speech/convert",
    response_model=project.convert_text_to_speech_service.SpeechSynthesisResponse,
)
async def api_post_convert_text_to_speech(
    user_id: str,
    text: str,
    language: str,
    voice_preference: str,
    input_format: str,
    speed: Optional[float],
    pitch: Optional[float],
) -> project.convert_text_to_speech_service.SpeechSynthesisResponse | Response:
    """
    Convert provided text to speech and return audio file
    """
    try:
        res = await project.convert_text_to_speech_service.convert_text_to_speech(
            user_id, text, language, voice_preference, input_format, speed, pitch
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/speech/output/{fileId}",
    response_model=project.retrieve_speech_output_service.RetrieveSpeechOutputResponse,
)
async def api_get_retrieve_speech_output(
    fileId: str,
) -> project.retrieve_speech_output_service.RetrieveSpeechOutputResponse | Response:
    """
    Retrieve generated speech file
    """
    try:
        res = await project.retrieve_speech_output_service.retrieve_speech_output(
            fileId
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/preferences",
    response_model=project.get_user_preferences_service.UserPreferencesResponse,
)
async def api_get_get_user_preferences() -> project.get_user_preferences_service.UserPreferencesResponse | Response:
    """
    Retrieve user's saved preferences
    """
    try:
        res = await project.get_user_preferences_service.get_user_preferences()
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
