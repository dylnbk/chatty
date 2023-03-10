import openai
import streamlit as st

# load & inject style sheet
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# open files
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# GPT3 request
def gpt3_completion(derp):

    # fetch response
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=derp)
    
    # return response
    return response["choices"][0]["message"]["content"]

# count words
def word_count(string):

    # if total count of words > 1000
    if len(string.strip().split(" ")) > 1000:

        # slice/delete the last entries from the conversation
        st.session_state.conversation["motoko"] = st.session_state.conversation["motoko"][:-4 or None]

# see info box
def info_box():

    # create an info box
    with st.expander("See info"):

        st.write("### Thanks for visiting Chatty!")

        st.write("""
            This website was made using Python, you can view the source [here](https://github.com/dylnbk/chat-bot).

            The responses are generated by using OpenAI's GPT-3 model. 
            
            To show support, please consider ☕ [buying me a coffee](https://www.buymeacoffee.com/dylnbk).
            """)

        st.write("***")

        st.write("""
            ##### Chat
            - A friendly AI that simply wants to have a conversation!
            """)
        
        st.write("***")

        st.write("""
            ##### Summarize
            - Converts text into a summarized numbered list.
            """)

        st.write("***")

        st.write("""
            ##### Explain
            - Will attempt to simplify & explain the text.
            - Works for code snippets!
            """)
        st.write("***")

        st.write("""
            ##### Rewrite
            - Paraphrase a piece of text.
            """)
        st.write("***")

        st.write("""
            ##### Story
            - Provide some details & a story will be written about them.
            """)

        st.write("")
        st.write("")

# chat tab
def chat_menu():

    # create a form  
    with st.form("input_motoko", clear_on_submit=True):     

        # text area for user input limited to 500 chars
        user_input = st.text_area('Enter a message:', max_chars=1000)

        # submit button with onclick that makes session_state.check = True
        st.form_submit_button("Submit", on_click=check_true_motoko)

        # see info box
        info_box()

        # if the form is submitted session_state.check will be True
        # create and write the response to the screen and store conversation
        if st.session_state.check["motoko"]:

            # clean prompt of unsupported characters
            user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
            prompt = {"role": "user", "content": user_input}

            # get user input and append to the conversation list
            st.session_state.conversation["motoko"].append(prompt)

            # request and store GPT completetion 
            response = gpt3_completion(st.session_state.conversation["motoko"])

            # append chatbot response
            st.session_state.conversation["motoko"].append({"role": "assistant", "content": response})
            
            # reverse the list so that last message displays at the top
            reverse_iterator = reversed(st.session_state.conversation["motoko"])
            history = list(reverse_iterator)

            # iterate through the messages
            for count, message in enumerate(history[:-1]):
                
                if count % 2 != 0:
                    # write the response to the screen
                    st.markdown("_You:_")
                    st.write(message['content'])
                    st.write("")

                else:
                    st.markdown("_Motoko:_")
                    st.write(message['content'])
                    st.write("")

            # reset the session state
            st.session_state.check["motoko"] = False

# summarize menu
def summary_menu():

    # create a form  
    with st.form("input_summarise", clear_on_submit=True):   

        # text area for user input limited to 1.5k chars
        user_input = st.text_area('Enter a message:', max_chars=2000)

        # submit button with onclick that makes session_state.check = True
        st.form_submit_button("Submit", on_click=check_true_summarise)

        # see info box
        info_box()

        # if the form is submitted session_state.check will be True - create and write the response
        if st.session_state.check["summarise"]:

            # clean prompt of unsupported characters
            user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
            prompt = {"role": "user", "content": user_input}

            # get user input and append to the conversation list
            st.session_state.conversation["summarise"].append(prompt)

            # request and store GPT completetion 
            response = gpt3_completion(st.session_state.conversation["summarise"])

            # append chatbot response
            st.session_state.conversation["summarise"].append({"role": "assistant", "content": response})
            
            # reverse the list so that last message displays at the top
            reverse_iterator = reversed(st.session_state.conversation["summarise"])
            history = list(reverse_iterator)

            # iterate through the messages
            for count, message in enumerate(history[:-1]):
                
                if count % 2 != 0:
                    # write the response to the screen
                    st.markdown("_You:_")
                    st.write(message['content'])
                    st.write("")

                else:
                    st.markdown("_Motoko:_")
                    st.write(message['content'])
                    st.write("")

            # reset the session state
            st.session_state.check["summarise"] = False

# explain menu
def explain_menu():

    # create a form  
    with st.form("input_explain", clear_on_submit=True):   

        # text area for user input limited to 1.5k chars
        user_input = st.text_area('Enter a message:', max_chars=2000)

        # submit button with onclick that makes session_state.check = True
        st.form_submit_button("Submit", on_click=check_true_explain)

        # see info box
        info_box()

        # if the form is submitted session_state.check will be True - create and write the response
        if st.session_state.check["explain"]:

            # clean prompt of unsupported characters
            user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
            prompt = {"role": "user", "content": user_input}

            # get user input and append to the conversation list
            st.session_state.conversation["explain"].append(prompt)

            # request and store GPT completetion 
            response = gpt3_completion(st.session_state.conversation["explain"])

            # append chatbot response
            st.session_state.conversation["explain"].append({"role": "assistant", "content": response})
            
            # reverse the list so that last message displays at the top
            reverse_iterator = reversed(st.session_state.conversation["explain"])
            history = list(reverse_iterator)

            # iterate through the messages
            for count, message in enumerate(history[:-1]):
                
                if count % 2 != 0:
                    # write the response to the screen
                    st.markdown("_You:_")
                    st.write(message['content'])
                    st.write("")

                else:
                    st.markdown("_Motoko:_")
                    st.write(message['content'])
                    st.write("")

            # reset the session state
            st.session_state.check["explain"] = False

# paraphrase menu
def rewrite_menu():

    # create a form  
    with st.form("input_rewrite", clear_on_submit=True):   

        # text area for user input limited to 1.5k chars
        user_input = st.text_area('Enter a message:', max_chars=2000)

        # submit button with onclick that makes session_state.check = True
        st.form_submit_button("Submit", on_click=check_true_rewrite)

        # see info box
        info_box()

        # if the form is submitted session_state.check will be True - create and write the response
        if st.session_state.check["rewrite"]:

            # clean prompt of unsupported characters
            user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
            prompt = {"role": "user", "content": user_input}

            # get user input and append to the conversation list
            st.session_state.conversation["rewrite"].append(prompt)

            # request and store GPT completetion 
            response = gpt3_completion(st.session_state.conversation["rewrite"])

            # append chatbot response
            st.session_state.conversation["rewrite"].append({"role": "assistant", "content": response})
            
            # reverse the list so that last message displays at the top
            reverse_iterator = reversed(st.session_state.conversation["rewrite"])
            history = list(reverse_iterator)

            # iterate through the messages
            for count, message in enumerate(history[:-1]):
                
                if count % 2 != 0:
                    # write the response to the screen
                    st.markdown("_You:_")
                    st.write(message['content'])
                    st.write("")

                else:
                    st.markdown("_Motoko:_")
                    st.write(message['content'])
                    st.write("")

            # reset the session state
            st.session_state.check["rewrite"] = False

# create stories menu
def story_menu():

    # create a form  
    with st.form("input_stories", clear_on_submit=True):   

        # text area for user input limited to 1.5k chars
        user_input = st.text_area('Enter a message:', max_chars=2000)

        # submit button with onclick that makes session_state.check = True
        st.form_submit_button("Submit", on_click=check_true_stories)

        # see info box
        info_box()

        # if the form is submitted session_state.check will be True - create and write the response
        if st.session_state.check["stories"]:

            # clean prompt of unsupported characters
            user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
            prompt = {"role": "user", "content": user_input}

            # get user input and append to the conversation list
            st.session_state.conversation["stories"].append(prompt)

            # request and store GPT completetion 
            response = gpt3_completion(st.session_state.conversation["stories"])

            # append chatbot response
            st.session_state.conversation["stories"].append({"role": "assistant", "content": response})
            
            # reverse the list so that last message displays at the top
            reverse_iterator = reversed(st.session_state.conversation["stories"])
            history = list(reverse_iterator)

            # iterate through the messages
            for count, message in enumerate(history[:-1]):
                
                if count % 2 != 0:
                    # write the response to the screen
                    st.markdown("_You:_")
                    st.write(message['content'])
                    st.write("")

                else:
                    st.markdown("_Motoko:_")
                    st.write(message['content'])
                    st.write("")

            # reset the session state
            st.session_state.check["stories"] = False

# seperated as the onclick func does not accept an argument
# state session check for form submission
def check_true_motoko():
    st.session_state.check["motoko"] = True

# state session check for form submission
def check_true_summarise():
    st.session_state.check["summarise"] = True

# state session check for form submission
def check_true_explain():
    st.session_state.check["explain"] = True

# state session check for form submission
def check_true_rewrite():
    st.session_state.check["rewrite"] = True

# state session check for form submission
def check_true_stories():
    st.session_state.check["stories"] = True

# create session state to save the conversation
# user input and GPT output will be stored here
if 'conversation' not in st.session_state:
    st.session_state.conversation = {
        "motoko": [
            {"role": "system", "content": "You are a sarcastic robot assistant, you like to make bad jokes but eventually give the correct answer."},
        ],

        "summarise": [
            {"role": "system", "content": "You are a helpful assistant that summerizes text into a numbered list"},
        ],

        "explain": [
            {"role": "system", "content": "You are a helpful assistant that explains text in a simplified manner, easy enough for a child to understand (ELI5)."},
        ],

        "rewrite": [
            {"role": "system", "content": "You are a helpful assistant that rewrites text using other words."},
        ],

        "stories": [
            {"role": "system", "content": "You are a helpful assistant that writes an entire story based on whatever the user provides"},
        ],
    }
    

# create session state for form submission 
# this stops streamlit from submiting a prompt when the page loads
if 'check' not in st.session_state:
    st.session_state.check = {

        "motoko": False,
        "summarise": False,
        "explain": False,
        "rewrite": False,
        "stories": False
    }

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

if __name__ == '__main__':

    st.title('Ask it.')    

    # define tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Chat", "Summarize", "Explain", "Rewrite", "Story"])

    try:

        # chatbot
        with tab1:

            chat_menu()

        # summarise
        with tab2:

            summary_menu()

        # explain
        with tab3:

            explain_menu()

        # re-write
        with tab4:

            rewrite_menu()

        # stories
        with tab5:

            story_menu()

    # pain
    except Exception as e:
                st.error(f"Something went wrong...\n{e}", icon="💔")