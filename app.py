import streamlit as st
import requests
import pandas as pd

DATABASE_ID = "0ebd7c81e3984846bfe86cc16658026a"
NOTION_TOKEN = "secret_ACWipYLLkakKzVBGixKUEsaLcQjP8C1xMLuUAIGMztH"
url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages
    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
    return results

pages = get_pages()

scores = []
reading_streak = 0
sleeping_streak = 0
objective_streak = 0
exercise_streak = 0
meditation_streak = 0
journal_streak = 0
days = []
for page in reversed(pages):
    props = page["properties"]
    if props['Type']['select']['name'] == "Journée":
        days.append(props["Date"]["date"]["start"][5:10])
        scores.append(props["Score des habitudes"]['formula']['number'])
        if props["Lire un livre"]['checkbox']: 
            reading_streak += 1 
        else: reading_streak = 0
        if props["Dormir avant minuit"]['checkbox']: 
            sleeping_streak += 1 
        else: 
            sleeping_streak = 0
        if props["Objectifs atteints"]['checkbox']: 
            objective_streak += 1 
        else: 
            objective_streak = 0
        if props["Exercise"]["checkbox"]: 
            exercise_streak += 1
        else:
            exercise_streak = 0
        if props["Meditation"]["checkbox"]: 
            meditation_streak += 1
        else:
            meditation_streak = 0
        if props["Journaling"]['checkbox']: 
            journal_streak += 1 
        else: 
            journal_streak = 0
        
st.title("Habit tracker")
col1, col2 = st.columns([2,3])
with col1:
    st.header(":fire: :repeat: Streaks")
    st.markdown(f'<h2 style="font-size: 24px;">✅ Objectifs: {objective_streak}</h2>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-size: 24px;">📚 Reading: {reading_streak}</h2>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-size: 24px;">🛌 Sleeping: {sleeping_streak}</h2>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-size: 24px;">💪 Exercise: {exercise_streak}</h2>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-size: 24px;">🍃 Meditation: {meditation_streak}</h2>', unsafe_allow_html=True)
    st.markdown(f'<h2 style="font-size: 24px;">📓 Journal: {journal_streak}</h2>', unsafe_allow_html=True)

with col2:
    st.header("Habit scores")
    df = pd.DataFrame(scores[len(scores)-14:], index=days[len(days)-14:], columns=['Scores'])
    st.bar_chart(df)




