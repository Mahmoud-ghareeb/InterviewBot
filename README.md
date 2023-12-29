# streamlit-interview-ai-app

Streamlit app for an llm that helps prepare you for data analyst interview

## Welcome page
Below is a gif that shows the first page that appears to the user (takes a minute to load)

![selecting](https://github.com/Farah-S/InterviewBot/blob/main/assets/selecting.gif)

## Star question
Below is a gif that shows a STAR question and response (takes a minute to load)

![star](https://github.com/Farah-S/InterviewBot/blob/main/assets/star.gif)

## Changing category
Below is a gif that shows changing the type of question and category (takes a minute to load)

![changing_category](https://github.com/Farah-S/InterviewBot/blob/main/assets/changing_category.gif)


## Run instructions

Activate virtual environment
Install the following packages

```sh
pip install -r requirements.txt
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps streamlit_custom_chat
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps streamlit_custom_input
pip install key_generator
```

## Usage instructions

After activating the virtual environment run the following command

```sh
streamlit run router.py
```
