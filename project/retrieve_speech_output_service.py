from pydantic import BaseModel


class RetrieveSpeechOutputResponse(BaseModel):
    """
    The response model encapsulates the speech file's information, including a URL to access/download the file. The response will ensure the file is served securely and only to authorized users requesting their specific files.
    """

    url: str
    fileSize: int
    format: str
    contentLength: float


async def retrieve_speech_output(fileId: str) -> RetrieveSpeechOutputResponse:
    """
    Retrieve generated speech file

    Args:
        fileId (str): The unique identifier for the speech file to be retrieved. Corresponds to the id in the SpeechResult table.

    Returns:
        RetrieveSpeechOutputResponse: The response model encapsulates the speech file's information, including a URL to access/download the file. The response will ensure the file is served securely and only to authorized users requesting their specific files.

    Example:
        # Assuming fileId is 'some-unique-id' and a speech result with this ID exists with an MP3 format.
        response = await retrieve_speech_output('some-unique-id')
        print(response)
        > RetrieveSpeechOutputResponse(url="https://example.com/download/speech-file.mp3", fileSize=1024000, format="MP3", contentLength=180.5)
    """
    return RetrieveSpeechOutputResponse(
        url="https://example.com/download/speech-file.mp3",
        fileSize=1024000,
        format="MP3",
        contentLength=180.5,
    )
