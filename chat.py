import openai
import streamlit as st
from deta import Deta
from datetime import datetime

# load & inject style sheet
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# open files
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
# check and create user
def user_auth(username):

    # check for username
    user_check = db.fetch({"name": username})
    user_response = user_check.items

    # if valid return True
    if user_response:
        return True

    # empty username field, skip creation
    elif username == "":
        pass
    
    # else create user
    else:
        db.put({"name": username, "conversations": {"motoko": {"messages": {"New chat": []}}, 
                                                    "summarise": {"messages": {"New chat": []}}, 
                                                    "explain": {"messages": {"New chat": []}}, 
                                                    "rewrite": {"messages": {"New chat": []}}, 
                                                    "stories": {"messages": {"New chat": []}}, 
                                                    "describe": {"messages": {"New chat": []}}, 
                                                    "code": {"messages": {"New chat": []}}}}, username)
        return True
        
def message_history(content):

    col1, col2 = st.columns([2, 1])

    check = False

    # take username and verify / create
    logged_in = user_auth(user)
        
    with col1:

        if logged_in:

            if content == "motoko":
                # get the messages linked to a specific title
                conversation_titles = db.get(user)['conversations']['motoko']['messages'].keys()
                conversation_select_motoko = st.selectbox("Chat history:", reversed(list(conversation_titles)), key="motoko_select")

                # return the messages matching the title index and username
                messages  = db.get(user)["conversations"]["motoko"]["messages"].get(conversation_select_motoko)

                check = True

            elif content == "summarise":
                # get the messages linked to a specific title
                conversation_titles = db.get(user)['conversations']['summarise']['messages'].keys()
                conversation_select_summarise = st.selectbox("Chat history:", reversed(list(conversation_titles)), key="summarise_select")

                # return the messages matching the title index and username
                messages  = db.get(user)["conversations"]["summarise"]["messages"].get(conversation_select_summarise)

                check = True

            elif content == "explain":
                # get the messages linked to a specific title
                conversation_titles = db.get(user)['conversations']['explain']['messages'].keys()
                conversation_select_explain = st.selectbox("Chat history:", reversed(list(conversation_titles)), key="explain_select")

                # return the messages matching the title index and username
                messages  = db.get(user)["conversations"]["explain"]["messages"].get(conversation_select_explain)

                check = True

            elif content == "rewrite":
                # get the messages linked to a specific title
                conversation_titles = db.get(user)['conversations']['rewrite']['messages'].keys()
                conversation_select_rewrite = st.selectbox("Chat history:", reversed(list(conversation_titles)), key="rewrite_select")

                # return the messages matching the title index and username
                messages  = db.get(user)["conversations"]["rewrite"]["messages"].get(conversation_select_rewrite)

                check = True

            elif content == "stories":
                # get the messages linked to a specific title
                conversation_titles = db.get(user)['conversations']['stories']['messages'].keys()
                conversation_select_stories = st.selectbox("Chat history:", reversed(list(conversation_titles)), key="stories_select")

                # return the messages matching the title index and username
                messages  = db.get(user)["conversations"]["stories"]["messages"].get(conversation_select_stories)

                check = True

            elif content == "describe":
                # get the messages linked to a specific title
                conversation_titles = db.get(user)['conversations']['describe']['messages'].keys()
                conversation_select_describe = st.selectbox("Chat history:", reversed(list(conversation_titles)), key="describe_select")

                # return the messages matching the title index and username
                messages  = db.get(user)["conversations"]["describe"]["messages"].get(conversation_select_describe)

                check = True

            elif content == "code":

                # get the messages linked to a specific title
                conversation_titles = db.get(user)['conversations']['code']['messages'].keys()
                conversation_select_code = st.selectbox("Chat history:", reversed(list(conversation_titles)), key="code_select")

                # return the messages matching the title index and username
                messages  = db.get(user)["conversations"]["code"]["messages"].get(conversation_select_code)

                check = True
        else:

            st.selectbox("Chat history:", ("",), key=f"{content}_select")
    
    with col2:
            if st.button("Delete", key=f"{content}_button"):

                data = db.get(user)

                if content == "motoko" and data["conversations"]["motoko"]["messages"][conversation_select_motoko]:
                    del data["conversations"]["motoko"]["messages"][conversation_select_motoko]

                elif content == "summarise" and data["conversations"]["summarise"]["messages"][conversation_select_summarise]:
                    del data["conversations"]["summarise"]["messages"][conversation_select_summarise]
                
                elif content == "explain" and data["conversations"]["explain"]["messages"][conversation_select_explain]:
                    del data["conversations"]["explain"]["messages"][conversation_select_explain]

                elif content == "rewrite" and data["conversations"]["rewrite"]["messages"][conversation_select_rewrite]:
                    del data["conversations"]["rewrite"]["messages"][conversation_select_rewrite]

                elif content == "stories" and data["conversations"]["stories"]["messages"][conversation_select_stories]:
                    del data["conversations"]["stories"]["messages"][conversation_select_stories]

                elif content == "describe" and data["conversations"]["describe"]["messages"][conversation_select_describe]:
                    del data["conversations"]["describe"]["messages"][conversation_select_describe]

                elif content == "code" and data["conversations"]["code"]["messages"][conversation_select_code]:
                    del data["conversations"]["code"]["messages"][conversation_select_code]

                db.put(data, user)

    if check:

        check = False
        
        if content == "motoko":
            return messages, conversation_select_motoko
        elif content == "summarise":
            return messages, conversation_select_summarise
        elif content == "explain":
            return messages, conversation_select_explain
        elif content == "rewrite":
            return messages, conversation_select_rewrite
        elif content == "stories":
            return messages, conversation_select_stories
        elif content == "describe":
            return messages, conversation_select_describe
        elif content == "code":
            return messages, conversation_select_code
    
    else:
        return False, False
        

# gpt request
def gpt_completion(messages):

    # fetch response
    response = openai.ChatCompletion.create(model="gpt-4", messages=messages)

    response_length = response["usage"]["total_tokens"]
    response = response["choices"][0]["message"]["content"]
    
    # return response & token length
    return response, response_length

# limit prompt length 
def prompt_limit(conversation_type, prompt_length):

    if prompt_length > 7500:

        if conversation_type == "motoko":

            del st.session_state.conversation["motoko"][1:5]

        elif conversation_type == "summarise":

            del st.session_state.conversation["summarise"][1:5]

        elif conversation_type == "explain":
            
            del st.session_state.conversation["explain"][1:5]
        
        elif conversation_type == "rewrite":
            
            del st.session_state.conversation["rewrite"][1:5]
        
        elif conversation_type == "stories":
            
            del st.session_state.conversation["stories"][1:5]

        elif conversation_type == "describe":
            
            del st.session_state.conversation["describe"][1:5]

        elif conversation_type == "code":
            
            del st.session_state.conversation["code"][1:5]

# see info box
def info_box():

    # create an info box
    with st.expander("See info"):

        st.write("### Thanks for visiting Chatty!")

        st.write("""
            This website was made using Python, you can view the source [here](https://github.com/dylnbk/chat-bot).

            The responses are generated by using OpenAI's GPT-4 model. 
            
            To show support, please consider ☕ [buying me a coffee](https://www.buymeacoffee.com/dylnbk).
            """)

        st.write("***")

        st.write("""
            ##### Chat
            - An AI assistant that you can have a conversation with!
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
            ##### Describe
            - Descriptions for things such as items, products, services.
            """)
        st.write("***")

        st.write("""
            ##### Story
            - Provide some details & a story will be written about them.
            """)
        st.write("***")

        st.write("""
            ##### Code
            - A programming assistant, create and debug code.
            """)

        st.write("")
        st.write("")

# chat tab
def chat_menu():

    messages, conversation_title = message_history("motoko")

    # create a form  
    with st.form("input_motoko", clear_on_submit=True):     

        # text area for user input limited to 500 chars
        user_input = st.text_area('Enter a message:', max_chars=20000)

        # submit button with onclick that makes session_state.check = True
        st.form_submit_button("Submit", on_click=check_true_motoko)

        # see info box
        info_box()

        if messages:
            
            if not st.session_state.check["motoko"]:

                reverse_messages = reversed(messages)
                sorted_messages = list(reverse_messages)

                for count, message in enumerate(sorted_messages[:-1]):

                    if count % 2 != 0:
                        # write the response to the screen
                        st.markdown(f"_{user}:_")
                        st.write(message['content'])
                        st.write("")

                    else:
                        st.markdown("_Motoko:_")
                        st.write(message['content'])
                        st.write("")

        # if the form is submitted session_state.check will be True
        # create and write the response to the screen and store conversation
        if st.session_state.check["motoko"]:

            # if logged in
            if user:

                # get date
                current_date = datetime.now().strftime("%d/%m/%y %H:%M")

                # clean prompt of unsupported characters
                user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
                prompt = {"role": "user", "content": user_input}
                
                try:
                    
                    data = db.get(user)

                    if not messages:

                        # create title
                        conversation_title = f"{current_date} - {user_input}"
                        init_messages = [{"role": "system", "content": "You are a sarcastic robot assistant, you like to make bad jokes but eventually give the correct answer."}]

                        # Retrieve the existing messages dictionary, update 
                        code_messages_dict = data['conversations']['motoko']['messages']
                        code_messages_dict[conversation_title] = init_messages

                        db.put(data, user)

                    
                    target_prompt = data["conversations"]["motoko"]["messages"].get(conversation_title)
                    target_prompt.append(prompt)
                    db.put(data, user)

                    # request and store GPT completetion 
                    complete_prompt = db.get(user)["conversations"]["motoko"]["messages"].get(conversation_title)
                    response, response_length = gpt_completion(complete_prompt)

                    # prompt_limit("code", response_length) <------------------------------------------------ need to create a new function to handle logged in users
                    assistant = {"role": "assistant", "content": response}
                    target_response = data['conversations']['motoko']['messages'].get(conversation_title)
                    target_response.append(assistant)
                    db.put(data, user)

                    complete_messages = db.get(user)["conversations"]["motoko"]["messages"].get(conversation_title)

                    reverse_complete_messages = reversed(complete_messages)
                    sorted_complete_messages = list(reverse_complete_messages)

                    for count, message in enumerate(sorted_complete_messages[:-1]):

                        if count % 2 != 0:
                            # write the response to the screen
                            st.markdown(f"_{user}:_")
                            st.write(message['content'])
                            st.write("")

                        else:
                            st.markdown("_Motoko:_")
                            st.write(message['content'])
                            st.write("")

                    # reset the session state
                    st.session_state.check["motoko"] = False
                    
                # pain
                except Exception as e:
                            st.error(f"DB2\n{e}", icon="💔")

            else:

                # clean prompt of unsupported characters
                user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
                prompt = {"role": "user", "content": user_input}

                # get user input and append to the conversation list
                st.session_state.conversation["motoko"].append(prompt)

                # request and store GPT completetion 
                response, response_length = gpt_completion(st.session_state.conversation["motoko"])

                prompt_limit("motoko", response_length)

                assistant = {"role": "assistant", "content": response}

                # append chatbot response
                st.session_state.conversation["motoko"].append(assistant)
                
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
        user_input = st.text_area('Enter a message:', max_chars=20000)

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
            response, response_length = gpt_completion(st.session_state.conversation["summarise"])

            prompt_limit("summarise", response_length)

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
        user_input = st.text_area('Enter a message:', max_chars=20000)

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
            response, response_length = gpt_completion(st.session_state.conversation["explain"])
            
            prompt_limit("explain", response_length)

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
        user_input = st.text_area('Enter a message:', max_chars=20000)

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
            response, response_length = gpt_completion(st.session_state.conversation["rewrite"])
            
            prompt_limit("rewrite", response_length)

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
        user_input = st.text_area('Enter a message:', max_chars=20000)

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
            response, response_length = gpt_completion(st.session_state.conversation["stories"])
            
            prompt_limit("stories", response_length)

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

# create stories menu
def describe_menu():

    # create a form  
    with st.form("input_describe", clear_on_submit=True):   

        # text area for user input limited to 1.5k chars
        user_input = st.text_area('Enter a message:', max_chars=20000)

        # submit button with onclick that makes session_state.check = True
        st.form_submit_button("Submit", on_click=check_true_describe)

        # see info box
        info_box()

        # if the form is submitted session_state.check will be True - create and write the response
        if st.session_state.check["describe"]:

            # clean prompt of unsupported characters
            user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
            prompt = {"role": "user", "content": user_input}

            # get user input and append to the conversation list
            st.session_state.conversation["describe"].append(prompt)

            # request and store GPT completetion 
            response, response_length = gpt_completion(st.session_state.conversation["describe"])
            
            prompt_limit("describe", response_length)

            # append chatbot response
            st.session_state.conversation["describe"].append({"role": "assistant", "content": response})
            
            # reverse the list so that last message displays at the top
            reverse_iterator = reversed(st.session_state.conversation["describe"])
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
            st.session_state.check["describe"] = False

# create code menu
def code_menu():

    messages, conversation_title = message_history("code")
        
    # create a form  
    with st.form("input_code", clear_on_submit=True):   

        # text area for user input
        user_input = st.text_area('Enter a message:', max_chars=20000)

        # submit button with onclick that makes session_state.check = True
        st.form_submit_button("Submit", on_click=check_true_code)

        # see info box
        info_box()

        if messages:
            
            if not st.session_state.check["code"]:

                reverse_messages = reversed(messages)
                sorted_messages = list(reverse_messages)

                for count, message in enumerate(sorted_messages[:-1]):

                    if count % 2 != 0:
                        # write the response to the screen
                        st.markdown(f"_{user}:_")
                        st.write(message['content'])
                        st.write("")

                    else:
                        st.markdown("_Motoko:_")
                        st.write(message['content'])
                        st.write("")
            
        # if the form is submitted session_state.check will be True - create and write the response
        if st.session_state.check["code"]:

            # if logged in
            if user:

                # get date
                current_date = datetime.now().strftime("%d/%m/%y %H:%M")

                # clean prompt of unsupported characters
                user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
                prompt = {"role": "user", "content": user_input}
                
                try:
                    
                    data = db.get(user)

                    if not messages:

                        # create title
                        conversation_title = f"{current_date} - {user_input}"
                        init_messages = [{"role": "system", "content": "You are a helpful assistant that writes and debugs code in different programming languages"}]

                        # Retrieve the existing messages dictionary, update 
                        code_messages_dict = data['conversations']['code']['messages']
                        code_messages_dict[conversation_title] = init_messages

                        db.put(data, user)

                    
                    target_prompt = data["conversations"]["code"]["messages"].get(conversation_title)
                    target_prompt.append(prompt)
                    db.put(data, user)

                    # request and store GPT completetion 
                    complete_prompt = db.get(user)["conversations"]["code"]["messages"].get(conversation_title)
                    response, response_length = gpt_completion(complete_prompt)

                    # prompt_limit("code", response_length) <------------------------------------------------ need to create a new function to handle logged in users
                    assistant = {"role": "assistant", "content": response}
                    target_response = data['conversations']['code']['messages'].get(conversation_title)
                    target_response.append(assistant)
                    db.put(data, user)

                    complete_messages = db.get(user)["conversations"]["code"]["messages"].get(conversation_title)

                    reverse_complete_messages = reversed(complete_messages)
                    sorted_complete_messages = list(reverse_complete_messages)

                    for count, message in enumerate(sorted_complete_messages[:-1]):

                        if count % 2 != 0:
                            # write the response to the screen
                            st.markdown(f"_{user}:_")
                            st.write(message['content'])
                            st.write("")

                        else:
                            st.markdown("_Motoko:_")
                            st.write(message['content'])
                            st.write("")

                    # reset the session state
                    st.session_state.check["code"] = False
                    
                # pain
                except Exception as e:
                            st.error(f"DB2\n{e}", icon="💔")

            else:

                # clean prompt of unsupported characters
                user_input = user_input.encode(encoding='ASCII',errors='ignore').decode()
                prompt = {"role": "user", "content": user_input}
                
                # get user input and append to the conversation list
                st.session_state.conversation["code"].append(prompt)

                # request and store GPT completetion 
                response, response_length = gpt_completion(st.session_state.conversation["code"])
                
                prompt_limit("code", response_length)

                assistant = {"role": "assistant", "content": response}

                # append chatbot response
                st.session_state.conversation["code"].append(assistant)
                
                # reverse the list so that last message displays at the top
                reverse_iterator = reversed(st.session_state.conversation["code"])
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
                st.session_state.check["code"] = False

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

# state session check for form submission
def check_true_describe():
    st.session_state.check["describe"] = True

# state session check for form submission
def check_true_code():
    st.session_state.check["code"] = True

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

        "describe": [
            {"role": "system", "content": "You are a helpful assistant that writes descriptions, particularly aimed at products and services"},
        ],

        "code": [
            {"role": "system", "content": "You are a helpful assistant that writes and debugs code in different programming languages"},
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
        "stories": False,
        "describe": False,
        "code": False
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

# connect with NoSQL API Deta
deta = Deta(st.secrets["deta_key"])

# open database
db = deta.Base("control")

if __name__ == '__main__':

    st.title('Ask it.')    

    try:
        
        # Create a password input field
        PASS = st.secrets["passw"]

        with st.sidebar:

            user = st.text_input("Username:")
            password = st.text_input("Password", type="password")

        if password == PASS:

            # define tabs
            tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Chat", "Summarize", "Explain", "Rewrite", "Describe", "Story", "Code"])

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

            # descriptions
            with tab5:

                describe_menu()

            # stories
            with tab6:

                story_menu()

            # code
            with tab7:

                code_menu()

        else:

            st.header("Password required")

    # pain
    except Exception as e:
                st.error(f"Something went wrong...\n{e}", icon="💔")