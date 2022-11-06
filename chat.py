import openai
import streamlit as st

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['Djin:', 'You:']):
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

local_css("style.css")
openai.api_key = st.secrets["openaiapikey"]

if __name__ == '__main__':
    conversation = []
    form = st.form("input", clear_on_submit=True)
    user_input = form.text_area('Input', label_visibility="hidden")
    form.form_submit_button("Send")
    st.markdown('***')
    conversation.append(f'You: {user_input}')
    text_block = '\n'.join(conversation)
    prompt = open_file('promptchat.txt').replace('<<BLOCK>>', text_block)
    prompt = prompt + '\nDjin: '
    response = gpt3_completion(prompt)
    st.subheader(f'{response}')
    conversation.append(f'Djin: {response}')