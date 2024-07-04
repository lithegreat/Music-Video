# DeepLearningDudes_Music_Video

## Install and Run

### 1. Clone the repo
```bash
git clone https://gitlab.lrz.de/00000000014BAF53/music-video-dld.git
cd DeepLearningDudes_Music_Video
git submodule update --init --recursive
```
### 2. Install the requirements
Obtain the cookie of your app.suno.ai account

1. Head over to [app.suno.ai](https://app.suno.ai) using your browser.
2. Open up the browser console: hit `F12` or access the `Developer Tools`.
3. Navigate to the `Network tab`.
4. Give the page a quick refresh.
5. Identify the request that includes the keyword `client?_clerk_js_version`.
6. Click on it and switch over to the `Header` tab.
7. Locate the `Cookie` section, hover your mouse over it, and copy the value of the Cookie.
```bash
conda create --name nlp
conda activate nlp
cd DreamMachineAPI
pip install -r requirements.txt
cd ..
cd suno-api
npm install
```
Add the following to your `.env` file:

```
SUNO_COOKIE=<your-cookie>
```
Then run this in terminal:
```bash
npm run dev
```
Then new a terminal, run:
```bash
pip install moviepy matplotlib aiofiles aiohttp
```
### 3. Run
```bash
python src/main.py
```