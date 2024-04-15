---
date: 2024-04-15T13:22:45.798062
author: AutoGPT <info@agpt.co>
---

# Text-to-Speech API

Based on the questions and responses during the interview, the task involves creating a text-to-speech (TTS) endpoint with specific requirements: 1. **Input Handling**: The endpoint must accept both plain text and SSML (Speech Synthesis Markup Language) formatted input. This dual-input capability allows for a broader range of speech expressions, from simple text conversion to complex speech patterns that include pauses, emphasis, and audio adjustments. 2. **Speech Conversion**: The core functionality is to convert the provided input text into natural-sounding speech audio. It involves selecting a TTS library that can handle both input types efficiently and produce high-quality audio output. Based on the interview, potential libraries include `gTTS` for simplicity and access to Google's TTS engine, `pyttsx3` for offline capabilities, or `aws-polly` for advanced features and natural voice options. 3. **Customization Features**: The endpoint must offer customization options for voice (e.g., gender, accent), speed, pitch, and other parameters. This level of customization allows users to tailor the speech output to match their preferences or application requirements, enhancing the overall user experience. 4. **Output Format**: The generated audio should be returned in a specified format, with MP3 being the preferred format due to its balance of sound quality and file size. This flexibility ensures that the TTS service can be used in a variety of applications, including those that require specific audio formats for compatibility or quality reasons. **Technical Implementation**: The service will be implemented using Python and FastAPI, leveraging FastAPI's asynchronous capabilities to handle speech synthesis operations efficiently. PostgreSQL, in conjunction with Prisma as the ORM, will be used to store and manage user preferences and possibly cache generated speech files for frequent requests. Special consideration will be given to security, error handling, and integration with the frontend to ensure a robust and scalable service.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Text-to-Speech API'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
