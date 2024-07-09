# Audio Generation and Management Module

This Python module provides functions to interact with a backend service for generating and managing audio files based on provided prompts and other parameters.

## Requirements

- Python 3.x
- `requests` library

Install the required library using:
```sh
pip install requests
```

## Base URL Configuration

Replace the `base_url` with your Vercel domain:

```python
base_url = "http://localhost:3000"
```

## Functions

### `custom_generate_audio(payload)`

Sends a request to generate custom audio based on the provided payload.

- **Parameters:**
  - `payload` (dict): The data to send in the request body.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  data = custom_generate_audio({
      "prompt": "Your song lyrics here",
      "tags": "genre, mood",
      "title": "Song Title",
      "make_instrumental": False,
      "wait_audio": False,
  })
  ```

### `extend_audio(payload)`

Sends a request to extend existing audio based on the provided payload.

- **Parameters:**
  - `payload` (dict): The data to send in the request body.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  data = extend_audio({
      "audio_id": "existing_audio_id",
      "extension_params": {}
  })
  ```

### `generate_audio_by_prompt(payload)`

Sends a request to generate audio based on a text prompt.

- **Parameters:**
  - `payload` (dict): The data to send in the request body.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  data = generate_audio_by_prompt({
      "prompt": "Your song lyrics here",
      "tags": "genre, mood"
  })
  ```

### `get_audio_information(audio_ids)`

Fetches information about the specified audio IDs.

- **Parameters:**
  - `audio_ids` (str): Comma-separated string of audio IDs.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  data = get_audio_information("audio_id_1,audio_id_2")
  ```

### `get_quota_information()`

Fetches information about the current quota.

- **Returns:**
  - `response.json()` (dict): The JSON response from the server.

- **Example:**
  ```python
  quota_info = get_quota_information()
  ```

### `download_audio(url, directory, filename)`

Downloads audio from the specified URL to the given directory and filename.

- **Parameters:**
  - `url` (str): The URL to download the audio from.
  - `directory` (str): The directory to save the audio file.
  - `filename` (str): The name of the audio file.

- **Returns:**
  - `filepath` (str): The path to the downloaded audio file.

- **Example:**
  ```python
  filepath = download_audio("http://example.com/audio.mp3", "downloads", "audio.mp3")
  ```

## Usage Example

The following script demonstrates how to generate custom audio, check its status, and retrieve the audio URLs once available.

```python
if __name__ == "__main__":
    data = custom_generate_audio(
        {
            "prompt": "[Verse 1]\nCruel flames of war engulf this land\nBattlefields filled with death and dread\nInnocent souls in darkness, they rest\nMy heart trembles in this silent test\n\n[Verse 2]\nPeople weep for loved ones lost\nBattered bodies bear the cost\nSeeking peace and hope once known\nOur grief transforms to hearts of stone\n\n[Chorus]\nSilent battlegrounds, no birds' song\nShadows of war, where we don't belong\nMay flowers of peace bloom in this place\nLet's guard this precious dream with grace\n\n[Bridge]\nThrough the ashes, we will rise\nHand in hand, towards peaceful skies\nNo more sorrow, no more pain\nTogether, we'll break these chains\n\n[Chorus]\nSilent battlegrounds, no birds' song\nShadows of war, where we don't belong\nMay flowers of peace bloom in this place\nLet's guard this precious dream with grace\n\n[Outro]\nIn unity, our strength will grow\nA brighter future, we'll soon know\nFrom the ruins, hope will spring\nA new dawn, we'll together bring",
            "tags": "pop metal male melancholic",
            "title": "Silent Battlefield",
            "make_instrumental": False,
            "wait_audio": False,
        }
    )

    ids = f"{data[0]['id']},{data[1]['id']}"
    print(f"ids: {ids}")

    for _ in range(60):
        data = get_audio_information(ids)
        if data[0]["status"] == "streaming":
            print(f"{data[0]['id']} ==> {data[0]['audio_url']}")
            print(f"{data[1]['id']} ==> {data[1]['audio_url']}")
            break
        # sleep 5s
        time.sleep(5)

```