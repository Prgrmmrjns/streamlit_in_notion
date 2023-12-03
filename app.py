import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import requests

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
journal_streak = 0
for page in pages:
    page_id = page["id"]
    props = page["properties"]
    page_type = props['Type']['select']['name']
    if page_type == "Journée":
        score = props["Score des habitudes"]['formula']['number']
        reading_streak += 1 if props["Lire un livre"]['checkbox'] else 0
        sleeping_streak += 1 if props["Dormir avant minuit"]['checkbox'] else 0
        objective_streak += 1 if props["Objectifs atteints"]['checkbox'] else 0
        journal_streak += 1 if props["Journaling"]['checkbox'] else 0
        scores.append(score)

# Function to create the barplot
def create_barplot(data):
    plt.figure(figsize=(20, 12)) 
    sns.barplot(x=list(range(len(data))), y=data, color="blue")
    plt.xlabel('Day')
    plt.ylabel('Habit score')
    st.pyplot(plt)


st.title("Habit tracker")

st.header(f":fire: Reading streak: {reading_streak}")
st.header(f":fire: Sleeping streak: {sleeping_streak}")
st.header(f":fire: Objectifs streak: {objective_streak}")
st.header(f":fire: Journaling streak: {journal_streak}")

st.header("Habit scores")
create_barplot(scores)




