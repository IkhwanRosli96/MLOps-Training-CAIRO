# Google Machine Learing API - Hands-On

> For all the examples - show on using Gcloud only except Google Vision API

## Google Vision API - [Documentation](https://cloud.google.com/vision/docs/features-list)

### 1. Preparation For Using Cloud Shell (Console in GCP)

- **Make a new project**
- Open GCP console
- Click "My First Project"
- Click "Make New Project"
- After that select the project

### 2. **Copy Training File Into the Cloud Shell**

- Activate Cloud Shell
- Run “gcloud config set project [Project ID]” on terminal (Project ID can be get from list of project)
- If it asks for authorization, click authorize
- Click on more (3dots above the console), click upload and upload folder "Google_ML_API" from training folder

### 3. **Image Detection**

> **For different type of detection use different image.** For landmark detection use image like Eiffel Tower or Taj Mahal.For logo detection use image like Apple Inc. and so on

1.  **Using raw API (CURL)**

    - Activate Cloud Shell
    - Open Editor and Go to /01_Google_ML_API/Google_Vision/Object_Detection/01_Curl
    - Copy curl.sh content
    - Open back terminal - CD into /01_Google_ML_API/Google_Vision/Object_Detection/01_Curl
    - Paste the copied curl, change the PROJECT_ID with your own project_id and enter it will return the result
    - Try playing around with the content of request.json file
      - imageUri = image url
      - maxResults = how much results it will show
      - type = type of detection

2.  **Using Gcloud -** [Documentation](https://cloud.google.com/vision/docs/features-list)

- gcloud ml vision detect-labels "[IMG_URI]"
- gcloud ml vision detect-landmarks "[IMG_URI]"
- gcloud ml vision detect-logos "[IMG_URI]"
- For more detection
  - gcloud ml vision --help

3.  **Using Python**

- CD to /01_Google_ML_API/Google_Vision/Object_Detection/02_Python
- There are 4 python code to run different detection
  1. detect_labels.py
  2. detect_landmarks.py
  3. detect_logos.py
  4. detect_objects.py
- If possible try to replicate the python code on face detection (from documentation) - copy the main code on the "main.py" and create new "detect_faces.py"

## Natural Language Processing API - [Documentation](https://cloud.google.com/natural-language/docs/setup)

> **For different type of detection use different text. Used gcloud only for the rest of the hands-on**

1. ## **Entity Analysis**
   > **Example of text can be taken from a paragraph of any articles**
   - gcloud ml language analyze-entities --content="[TEXT]"
   - For help use -- "gcloud ml language analyze-entities --help"
   - Task is to categories text into entities
     - Text are seperated into tokens
     - This token categories into entities
     - Same token will be in on entities
     - The are some properties in this properties such as
       - salience which indicated how important the entities is for the block of text
       - type indicate whether the entities are proper nouns, normal nous, adjective and so on
2. ## **Sentiment Analysis**
   > **Example of text can be taken from a paragraph of any articles or just use example in documentation**
   - gcloud ml language analyze-sentiment --content="[TEXT]"
   - Get the score value of the sentences
     - More than 1 is positive
     - 0 is neutral
     - Less than 0 is negative
3. ## **Sentiment Entity Analysis**
   > **Example of text can be taken from a paragraph of any articles or just use example in documentation**
   - gcloud ml language analyze-entity-sentiment --content="[TEXT]"
   - combination of both of approach
     - Entity Analysis
     - Sentiment Analysis
   - To detect the sentiment analysis on each entities
     - If there are 2 or more mentions in a entities, you can see the sentiment score is different
     - This is because of the score calculated based on the string where the entities located
4. ## **Syntax Analysis**
   > **Example of text can be taken from a paragraph of any articles or just use example in documentation**
   - gcloud ml language analyze-syntax --content="[TEXT]"
   - Breaks up the given text into a series of sentences and tokens (generally, words) and provides linguistic information about those tokens.
   - More deep information about the linguistic information of each token
   -
5. ## **Content Classification**
   > **Open the documentation to see all of the categories offered.** For example, can take paragraph from travel blog / entertainment blog
   - gcloud ml language classify-text --content="[TEXT]"
   - There are 2 version
     - V1
     - v2 - covered categories in version 1 and more categoreis added
   - Gcloud only use v1. Other platform like python can use v2 API

## Speech-to-Text & Text-to-Speech Recognition - [Documentation](https://cloud.google.com/speech-to-text/docs/speech-to-text-requests)

1. ## **Speech-to-Text Recognition**

   - gcloud ml speech recognize "[PATH_OF_AUDIO] --language-code='en-US'
     - For the path of audio, 01_Google_ML_API/Google_Vision/Speech2Text/test.flac
   - Refer gcloud ml speech recognize --help for more info
   - Use demo page to show live stream speech-to-text example - [DEMO](https://cloud.google.com/speech-to-text#)

2. ## **Text-to-Speech Recognition**
   - Use demo page as it is more easy - [DEMO](https://cloud.google.com/text-to-speech#)
