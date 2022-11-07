import openai
import streamlit as st

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def gpt3_completion(prompt, engine='text-davinci-002', temp=0.8, top_p=1, tokens=1000, freq_pen=0.0, pres_pen=0.0, stop=['You:']):
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    text = response['choices'][0]['text'].strip()
    return text

st.set_page_config(
    page_title="chatty",
    page_icon="💬",
    menu_items={
        'Report a bug': "mailto:dyln.bk@gmail.com",
        'About': "Chat to the AI!"
    }
)

local_css("style.css")
openai.api_key = st.secrets["openaiapikey"]

if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if __name__ == '__main__':                                       
    form = st.form("input", clear_on_submit=True)
    user_input = form.text_area('Input', label_visibility="hidden")
    form.form_submit_button("Send")
    st.markdown('***')
    st.session_state.conversation.append(f'You: {user_input}')
    text_block = '\n'.join(st.session_state.conversation)
    prompt = open_file('promptchat.txt').replace('<<BLOCK>>', text_block)
    prompt = prompt + '\nMotoko: '
    response = gpt3_completion(prompt)
    st.write(f'{response}')
    st.session_state.conversation.append(f'Motoko: {response}')