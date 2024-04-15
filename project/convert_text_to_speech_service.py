import os
import tempfile
from typing import Optional

import prisma
import prisma.enums
import prisma.models
from gtts import gTTS
from pydantic import BaseModel


class SpeechSynthesisResponse(BaseModel):
    """
    Contains details about the synthesized speech including its accessible path and any metadata.
    """

    speech_file_path: str
    file_format: str
    duration: float
    size: int


async def convert_text_to_speech(
    user_id: str,
    text: str,
    language: str,
    voice_preference: str,
    input_format: str,
    speed: Optional[float] = None,
    pitch: Optional[float] = None,
) -> SpeechSynthesisResponse:
    """
    Convert provided text to speech and return audio file

    Args:
    user_id (str): Unique identifier for the user making the request.
    text (str): The text content to be converted into speech.
    language (str): The language and accent desired for the speech output.
    voice_preference (str): The user's preferred voice setting for the speech.
    input_format (str): The format of the input text, plain text or SSML.
    speed (Optional[float]): The rate of speech to apply to the output.
    pitch (Optional[float]): The pitch adjustment for the speech output.

    Returns:
    SpeechSynthesisResponse: Contains details about the synthesized speech including its accessible path and any metadata.
    """
    tts = gTTS(text=text, lang=language, slow=speed is not None and speed < 0.5)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.save(tmpfile.name)
        tmpfile_path = tmpfile.name
    file_size = os.path.getsize(tmpfile_path)
    duration = 0
    speech_request = await prisma.models.SpeechRequest.prisma().create(
        data={
            "userId": user_id,
            "inputText": text,
            "inputFormat": prisma.enums.InputFormat.SSML
            if input_format.upper() == "SSML"
            else prisma.enums.InputFormat.TEXT,
            "outputFormat": prisma.enums.OutputFormat.MP3,
            "status": prisma.enums.ProcessStatus.COMPLETED,
            "user": {"connect": {"id": user_id}},
            "speechResult": {
                "create": {"audioFilePath": tmpfile_path, "audioFileSize": file_size}
            },
        }
    )
    return SpeechSynthesisResponse(
        speech_file_path=tmpfile_path,
        file_format="MP3",
        duration=duration,
        size=file_size,
    )
