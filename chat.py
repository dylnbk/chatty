import openai
import streamlit as st

# open files
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# load & inject style sheet
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# state session check for form submission
def check_true():
    st.session_state.check = True

# GPT3 request
def gpt3_completion(prompt, engine='text-davinci-002', temp=0.7, top_p=1, tokens=1000, freq_pen=0.3, pres_pen=0.0, stop=['Motoko:', 'You:']):

    # clean prompt of unsupported characters
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()

    # fetch response
    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temp,
        max_tokens=tokens,
        top_p=top_p,
        frequency_penalty=freq_pen,
        presence_penalty=pres_pen,
        stop=stop)
    
    # strip & return motoko response
    text = response['choices'][0]['text'].strip()
    return text

# page configurations
st.set_page_config(
    page_title="Ask it.",
    page_icon="💬",
    menu_items={
        'Report a bug': "mailto:dyln.bk@gmail.com",
        'Get help': None,
        'About': "Made by dyln.bk"
    }
)

# style sheet & openAI API key
local_css("style.css")
openai.api_key = st.secrets["openaiapikey"]

# create session state to save the conversation
if 'conversation' not in st.session_state:
    st.session_state.conversation = {

        "motoko": [],
    }

# create session state for form submission
if 'check' not in st.session_state:
    st.session_state.check = False

if __name__ == '__main__':

    st.title('Ask it.')    

    # create a form                              
    form = st.form("input_motoko", clear_on_submit=True)
    user_input = form.text_area('Input', label_visibility="hidden")
    form.form_submit_button("Submit", on_click=check_true)
    st.markdown('***')

    # if the form is submitted, create and write the response
    if st.session_state.check:

        # get user input and insert into the prompt
        st.session_state.conversation["motoko"].append(f'You: {user_input}')
        text_block = '\n\n\n'.join(st.session_state.conversation["motoko"])
        prompt = open_file('promptchat_motoko.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\n\nMotoko: '

        # request completetion 
        response = gpt3_completion(prompt)

        # append motoko response & write the response
        st.session_state.conversation["motoko"].append(f'Motoko: {response}')
        st.write(response)
