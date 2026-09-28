# Voice Assistant

A Streamlit voice chatbot that transcribes recorded English speech, sends the conversation to an OpenAI model, and reads the response aloud.

The app combines local speech recognition with Faster Whisper, conversational responses through the OpenAI API, and local text-to-speech using pyttsx3.

## Features

- Record a message using the browser microphone.
- Preview the recorded audio before submitting it.
- Transcribe English speech using the `base.en` Whisper model on CPU with INT8 computation.
- Enable voice activity detection during transcription.
- Maintain conversation history across Streamlit reruns using session state.
- Display the transcription and assistant response.
- Read the assistant response aloud on the computer running Python.
- Cache the Whisper model across reruns to avoid repeatedly loading it.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit interface, transcription, chat, and speech output |
| `.env` | Local OpenAI API key; excluded from Git |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Excludes credentials, environments, and caches |
| `README.md` | Setup and usage instructions |

Place these files in the main `VoiceAssistant` folder.

## How it works

1. The user records audio with `st.audio_input` at a requested sample rate of 48,000 Hz.
2. Clicking **Respond** passes the recording to Faster Whisper.
3. Transcribed segments are combined into one message and appended to session history.
4. The complete conversation is sent to the configured OpenAI model, `gpt-5.4-mini`.
5. The assistant's response is added to history, displayed, and spoken using pyttsx3.

Conversation history is kept in `st.session_state`, not in a database or file. It survives ordinary Streamlit reruns within the session, but should not be treated as persistent storage across browser refreshes or new sessions. The application does not render a complete chat transcript on every rerun.

## Setup

### 1. Create a virtual environment

From the `VoiceAssistant` folder:

```bash
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Or in macOS/Linux:

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

Use a Python version supported by the installed dependencies. Package versions are unpinned because a tested environment was not provided. The Streamlit version must support `st.audio_input` and its `sample_rate` parameter.

The first use of `base.en` may download the speech-recognition model. Allow internet access and sufficient disk space for its cache. Speech output requires a working system speech engine and installed voices.

### 3. Configure your API key

Create `.env` beside `app.py`:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

The app calls `load_dotenv('.env')`, and `OpenAI()` reads `OPENAI_API_KEY` from the environment. Start the app from the project folder so the relative `.env` path resolves correctly.

Keep your actual key out of source code and Git. Your API account needs access to the configured model. Model requests require internet access and may incur API charges. If the model is unavailable to your account, update the model setting to one you can access and verify its supported parameters.

### 4. Start the app

```bash
python -m streamlit run app.py
```

Open the local address shown in the terminal, allow microphone access, record a message, and click **Respond**. Wait for transcription and the response to finish before submitting another message.

## Dependencies

| Package | Role |
| --- | --- |
| `streamlit` | Interface, audio recording, caching, and session state |
| `faster-whisper` | Local speech transcription |
| `python-dotenv` | Loading API credentials |
| `openai` | Chat Completions API client |
| `pyttsx3` | Local speech output |

`io.BytesIO` is part of Python's standard library and needs no separate installation.

## Known limitations

- Clicking **Respond** without recording audio causes an error because `audio` is `None`.
- Empty transcriptions are not checked before sending a request.
- `voices[1]` assumes at least two installed voices; computers with fewer voices may raise an error.
- Transcription, API calls, and speech run synchronously. The button handler waits for these operations to finish.
- pyttsx3 speaks on the host computer, not through browser audio. A remotely hosted version needs a different approach to deliver speech to visitors.
- The complete conversation is resent with each request, so long chats use more tokens and eventually need history management.
- No reset button, persistent history, or explicit handling of API/transcription/speech errors is included.
- Clicking **Respond** repeatedly on the same recording submits it again.
- `base.en` and the transcription setting are configured for English.

### Suggested input guard

At the beginning of the existing button handler, check the recording before starting transcription:

```python
if st.button("Respond"):
    if audio is None:
        st.warning("Please record a message first.")
        st.stop()

    # Existing transcription and response code follows here.
```

To avoid assuming a second voice exists, replace the explicit voice selection with:

```python
if voices:
    selected_voice = voices[1] if len(voices) > 1 else voices[0]
    engine.setProperty("voice", selected_voice.id)
```

These are suggested edits; generating this README does not change `app.py`.

## Data flow

Audio travels from the browser to the Streamlit process and is transcribed there by Faster Whisper. The supplied code sends the transcribed conversation text to OpenAI, not the audio recording. It does not explicitly save recordings or chat history to disk.

## Verification

This documentation is based on the supplied source. The microphone, model download, API request, and speech output have not been run as part of preparing these files.

## Uploading to GitHub

Keep `.gitignore` in the project root and name it exactly `.gitignore`, including the first dot. Before committing, use `git status` to confirm that `.env` and virtual-environment files are not staged. An ignore rule does not remove files already tracked by Git.
