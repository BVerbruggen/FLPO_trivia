import streamlit as st
import random
import pandas as pd
import json

st.set_page_config(layout="wide", page_icon="🥳", page_title="FLPO R&S Trivia")
# Initialize session state
if "stocks" not in st.session_state:
    st.session_state.stocks = {
        "FLPO": 0,
        "AAPL": random.randint(400, 500),
        "MSFT": random.randint(400, 500),
        "AMZN": random.randint(300, 400),
        "GOOGL": random.randint(300, 400),
        "TSLA": random.randint(400, 500),
    }
if "stock_history" not in st.session_state:
    st.session_state.stock_history = {
        "Poging": [0],
        "FLPO": [st.session_state.stocks["FLPO"]],
        "AAPL": [st.session_state.stocks["AAPL"]],
        "MSFT": [st.session_state.stocks["MSFT"]],
        "AMZN": [st.session_state.stocks["AMZN"]],
        "GOOGL": [st.session_state.stocks["GOOGL"]],
        "TSLA": [st.session_state.stocks["TSLA"]],
    }

if "stock_colors" not in st.session_state:
    st.session_state.stock_colors = {
        "AAPL": "#FF0000",
        "AMZN": "#FF3333",
        "FLPO": "#F0D66B",
        "GOOGL": "#FF6666",
        "MSFT": "#FF9999",
        "TSLA": "#FFCCCC",
    }

if "trivia_questions" not in st.session_state:
    with open("questions.json") as f:
        trivia_questions = json.load(f)
        random.shuffle(trivia_questions)
        st.session_state.trivia_questions = trivia_questions
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "ranking" not in st.session_state:
    st.session_state.ranking = []
if "attempt" not in st.session_state:
    st.session_state.attempt = 0


def check_answer(answer):
    correct_answer = st.session_state.trivia_questions[
        st.session_state.current_question
    ]["answer"]
    if answer.lower() == correct_answer.lower():
        st.session_state.stocks["FLPO"] += random.randint(200, 300)
        st.toast(
            ":green[Goed gedaan!] 😄",
        )
        st.session_state.current_question += 1
        st.session_state["txt_answer"] = ""
    else:
        st.session_state.stocks["FLPO"] -= random.randint(10, 200)
        st.toast(":red[Fout antwoord!] 😔")
    update_stocks()
    update_ranking()
    update_stock_history()


def update_stocks():
    # increase or decrease the stock points randomly with a maximum of 100, but not FLPO
    for key in st.session_state.stocks.keys():
        if key != "FLPO":
            st.session_state.stocks[key] += random.randint(-100, 100)


def update_ranking():
    st.session_state.ranking = sorted(
        st.session_state.stocks.items(), key=lambda x: x[1], reverse=True
    )


def update_stock_history():
    st.session_state.attempt += 1
    st.session_state.stock_history["Poging"].append(st.session_state.attempt)
    for key in st.session_state.stocks.keys():
        st.session_state.stock_history[key].append(st.session_state.stocks[key])


# Streamlit app layout


col1, col2 = st.columns([3, 1], gap="large")

with col1:
    st.markdown(
        "# <span style='color: #F0D66B;'>🎸📈 Filippo's Rock & Stock Trivia</span>",
        unsafe_allow_html=True,
    )
subcol1, subcol2 = col1.columns(2, vertical_alignment="center")

with subcol1:

    if st.session_state.current_question < len(st.session_state.trivia_questions):
        # Print the current question number and total number of questions
        current_question = st.session_state.current_question + 1
        total_questions = len(st.session_state.trivia_questions)
        st.subheader(f"Vraag {current_question}/{total_questions}")

        # Print the current question
        question = st.session_state.trivia_questions[st.session_state.current_question][
            "question"
        ]
        st.subheader(f"{question}")
        # Print the possible answers (options)
        options = st.session_state.trivia_questions[st.session_state.current_question][
            "options"
        ]

        answer = st.radio("Selecteer het juiste antwoord", options, key="radio_answer")
        st.button("Verstuur", on_click=check_answer, args=(answer,))

    else:
        st.write("Trivia spel voorbij! Bedankt voor het spelen! 🎉")
        st.balloons()
with subcol2:
    if st.session_state.current_question < len(st.session_state.trivia_questions):
        image = st.session_state.trivia_questions[
            st.session_state.current_question
        ].get("image")
        if image:
            st.image(image, width=300)

with col2:
    st.markdown(
        "# <span style='color: #F0D66B;'>Ranglijst</span>",
        unsafe_allow_html=True,
    )
    update_ranking()
    for i, (name, stock) in enumerate(st.session_state.ranking, start=1):
        if name == "FLPO":
            st.markdown(
                f"**<span style='background-color:{st.session_state.stock_colors[name]};color:#252525'>{i}. {name}: {stock} punten</span>**",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"**<span style='color:{st.session_state.stock_colors[name]}'>{i}. {name}: {stock} punten</span>**",
                unsafe_allow_html=True,
            )

with col1:
    # Display the stock points history as a line chart
    if st.session_state.stock_history["FLPO"]:
        df = pd.DataFrame(st.session_state.stock_history)
        st.line_chart(
            df.set_index("Poging"), color=list(st.session_state.stock_colors.values())
        )
