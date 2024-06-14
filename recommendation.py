
import streamlit as st
import os
import openai
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from azure.search.documents.models import VectorizableTextQuery
from azure.search.documents.models import RawVectorQuery
from azure.search.documents.models import RawVectorQuery
from azure.core.credentials import AzureKeyCredential


import json
import pandas as pd



#Load user credentials from JSON file
with open("credentials.json", "r") as f:
    credentials = json.load(f)

# Function to authenticate user
def authenticate(username, password):
    if username in credentials:
        if credentials[username]["password"] == password:
            return credentials[username]["role"]
    return None

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.role = None
    st.experimental_rerun()

# Login Page
login = st.sidebar.checkbox("Login")
logout_button = st.sidebar.button("Logout")

if logout_button:
    logout()

if login and not st.session_state.logged_in:
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        role = authenticate(username, password)
        if role:
            st.session_state.logged_in = True
            st.session_state.role = role
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid username or password")

# Check if the user is logged in before proceeding
if not st.session_state.logged_in:
    st.warning("Please log in to use the application.")
    st.stop()

# Assign the retrieved role to the ROLE variable
ROLE = st.session_state.role





############################################################## Log-IN Module ##########################################################    

st.title("H.B. Fuller ChatGPT 🚀")


OPENAI_API_KEY = "f1b014707f03408d90487d939f6a4afd"
OPENAI_API_ENDPOINT = "https://openai-leap.openai.azure.com/"
OPENAI_API_VERSION = "2024-02-15-preview"

AZURE_COGNITIVE_SEARCH_SERVICE_NAME = "others"
AZURE_COGNITIVE_SEARCH_API_KEY = "2oesXYJbWbYwVkfc2ltLNdfaEttwNs98qNMwLNLAXIAzSeCf4CS7"
AZURE_COGNITIVE_SEARCH_ENDPOINT = "https://others.search.windows.net"
azure_credential = AzureKeyCredential(AZURE_COGNITIVE_SEARCH_API_KEY)

AZURE_COGNITIVE_SEARCH_INDEX_NAME = "role_hbf"


logo_url = "data:image/png;base64,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"
logo_html = f'<img src="{logo_url}" alt="Logo" height="150" width="200">'
st.sidebar.markdown(f'<div class="logo-container">{logo_html}</div>', unsafe_allow_html=True)

################################ define role ################################################
#ROLE = role_name
################################ define role ################################################



dropdown_3_prompt = " "

# role_to_domain = {
#     "Product_Manager": "Product Manager",
#     "HR": "HR",
#     "Sales_Executive": "Sales Executive",
#     "Accountant": "Accountant"
# }

# # Get the user's role from the session or login system
#   # Implement this function to retrieve the user's role

# if ROLE == "Product_Manager":
#     domain = role_to_domain.get(ROLE, "Product_Manager")
#     st.sidebar.markdown(f"**Domain:** {domain}")
# elif ROLE == "HR":
#     domain = role_to_domain.get(ROLE, "HR")
#     st.sidebar.markdown(f"**Domain:** {domain}")
# elif ROLE == "Sales_Executive":
#     domain = role_to_domain.get(ROLE, "Sales Executive")
#     st.sidebar.markdown(f"**Domain:** {domain}")
# elif ROLE == "Accountant":
#     domain = role_to_domain.get(ROLE, "Accountant")
#     st.sidebar.markdown(f"**Domain:** {domain}")
# else:
#     st.sidebar.markdown("**Domain:** General")

import streamlit as st

role_to_domain = {
    "Product_Manager": "Product Manager",
    "HR": "HR",
    "Sales_Executive": "Sales Executive",
    "Accountant": "Accountant"
}

# Get the user's role from the session or login system
# Implement this function to retrieve the user's role
st.sidebar.markdown("   ")
st.sidebar.markdown("**Domain**")

if ROLE == "Product_Manager":
    domain = role_to_domain.get(ROLE, "Product_Manager")
    st.sidebar.markdown(f'<div style="background-color: #ff6347; padding: 10px; border-radius: 5px; color: white; font-weight: bold;">{domain}</div>', unsafe_allow_html=True)
elif ROLE == "HR":
    domain = role_to_domain.get(ROLE, "HR")
    st.sidebar.markdown(f'<div style="background-color: #ff6347; padding: 10px; border-radius: 5px; color: white; font-weight: bold;">{domain}</div>', unsafe_allow_html=True)
elif ROLE == "Sales_Executive":
    domain = role_to_domain.get(ROLE, "Sales Executive")
    st.sidebar.markdown(f'<div style="background-color: #ff6347; padding: 10px; border-radius: 5px; color: white; font-weight: bold;">{domain}</div>', unsafe_allow_html=True)
elif ROLE == "Accountant":
    domain = role_to_domain.get(ROLE, "Accountant")
    st.sidebar.markdown(f'<div style="background-color: #ff6347; padding: 10px; border-radius: 5px; color: white; font-weight: bold;">{domain}</div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div style="background-color: #ff6347; padding: 10px; border-radius: 5px; color: white; font-weight: bold;">General</div>', unsafe_allow_html=True)





# import pandas as pd
# import streamlit as st

# # Read the CSV file
# df = pd.read_csv('prompt.csv')

# # Create a sidebar selectbox for the user to choose the prompt
# promptt = st.sidebar.selectbox('Select Prompt', ("All", 'Product Manager', 'HR', 'Sales Executive', 'Accountant', 'Custom Prompt'))

# # Define the prompts based on the user's selection
# if promptt == "All":
#     row = df.loc[df['Role'] == 'All']
#     if not row.empty:
#         prompt_to_use = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"

# elif promptt == "Product Manager":
#     row = df.loc[df['Role'] == 'Product Manager']
#     if not row.empty:
#         prompt_to_use = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"
#     else:
#         prompt_to_use = None

# elif promptt == "HR":
#     row = df.loc[df['Role'] == 'HR']
#     if not row.empty:
#         prompt_to_use = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"
#     else:
#         prompt_to_use = None

# elif promptt == "Sales Executive":
#     row = df.loc[df['Role'] == 'Sales Executive']
#     if not row.empty:
#         prompt_to_use = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"
#     else:
#         prompt_to_use = None

# elif promptt == "Accountant":
#     row = df.loc[df['Role'] == 'Accountant']
#     if not row.empty:
#         prompt_to_use = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"
#     else:
#         prompt_to_use = None



# elif promptt == "Custom Prompt":
#     custom_prompt = st.sidebar.text_area("Enter your custom prompt:")
#     # custom_prompt = custom_prompt.strip()  # Remove leading/trailing whitespace
#     if custom_prompt:
#         prompt_to_use = custom_prompt
#     else:
#         prompt_to_use = ""

# # Print the prompt_to_use variable
# if prompt_to_use is not None:
#     print(prompt_to_use)
# else:
#     print("No prompt found for the selected option.")


import pandas as pd
import streamlit as st

# Read the CSV file
df = pd.read_csv('prompt.csv')

# Create a sidebar selectbox for the user to choose the prompt
#promptt = st.sidebar.selectbox('Select Prompt', ("All", 'Product Manager', 'HR', 'Sales Executive', 'Accountant', 'Custom Prompt'))

# Define the prompts based on the user's selection
st.sidebar.markdown("   ")
st.sidebar.markdown("**Prompt**")

if ROLE == "Product_Manager":
    row = df.loc[df['Role'] == 'Product Manager']
    if not row.empty:
        default_prompt = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"
    else:
        default_prompt = None
elif ROLE == "HR":
    row = df.loc[df['Role'] == 'HR']
    if not row.empty:
        default_prompt = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"
    else:
        default_prompt = None
elif ROLE == "Sales_Executive":
    row = df.loc[df['Role'] == 'Sales Executive']
    if not row.empty:
        default_prompt = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"
    else:
        default_prompt = None
elif ROLE == "Accountant":
    row = df.loc[df['Role'] == 'Accountant']
    if not row.empty:
        default_prompt = f"Role: {row['Role'].values[0]}\nObjective: {row['Objective'].values[0]}\nGuidelines: {row['Guidelines'].values[0]}"
    else:
        default_prompt = None
elif ROLE == "Custom Prompt":
    custom_prompt = st.sidebar.text_area("Enter your custom prompt:")
    if custom_prompt:
        default_prompt = custom_prompt
    else:
        default_prompt = ""

# Display the role in a styled box
if ROLE != "Custom Prompt":
    st.sidebar.markdown(f'<div style="background-color: #ff6347; padding: 10px; border-radius: 5px; color: white; font-weight: bold;">{ROLE}</div>', unsafe_allow_html=True)

st.sidebar.markdown("   ")
# Display the prompt for the selected role in a text area
if default_prompt is not None:
    edited_prompt = st.sidebar.text_area("Edit the prompt:", value=default_prompt, height=200)

    # Check if the user has pressed Enter
    if st.sidebar.button("Apply"):
        # Use the edited prompt for the chatbot
        final_prompt = edited_prompt
        print(f"Using the following prompt:\n{final_prompt}")
        # Add your chatbot code here
else:
    st.sidebar.write("No prompt found for the selected option.")

st.sidebar.markdown("   ")

modell = st.sidebar.selectbox('**Select Model**',("Azure OpenAI GPT-3.5",'Azure OpenAI GPT-4'))

if modell == "Azure OpenAI GPT-3.5" :
    model_to_use = "gpt3516k"
    
if modell == "Azure OpenAI GPT-4" :
    model_to_use = "gpt4-pre-leap"

# language = st.sidebar.selectbox('Select language',("English","German","French"))

# if language == "English" :
#     lang_to_use = "English"
    
# if language == "German" :
#     lang_to_use = "German"

# if language == "French" :
#     lang_to_use = "French"


language = st.sidebar.selectbox('**Select language**', ("English", "German", "French"))

if language == "English":
    lang_to_use = "strictly give responses in English only, even if the user asks questions in any language."

if language == "German":
    lang_to_use = "strictly give responses in German only, even if the user asks questions in any language."

if language == "French":
    lang_to_use = "strictly give responses in French only, even if the user asks questions in any language."


# prompt_files="""
# Strictly give all the file names present in the particular domain knowledge base in the side bar for that particular domain which is selected from drop down by the user.
# """

pmt="""
You are an AI assistant for the {ROLE} role. Your responses should be based strictly on the content or documents marked with the '{ROLE}' role in your knowledge base. If a user asks a question that is not related to the '{ROLE}' role, you should politely inform them that you cannot answer questions outside of your designated role.

If the response is not present in the source documents of the particular {ROLE} then simply respond like "I cannot answer questions outside of the designated role.". Don't make up answer by your own. Answer only what is written in the source documents of the particular role {ROLE} selected.

For case like "[Source: None]" then don't make answer by your own simply say I dodn't know.

You are an AI assistant with strict role-based access control. Your responses should be based exclusively on the content or documents marked with the specific role assigned to you. You are not permitted to answer any questions or provide any information that falls outside of your designated role.
When a user asks a question that is unrelated to your assigned role, you must politely decline to answer and inform the user that their query is outside your designated scope. You should use a consistent and professional tone in your response, something like:
"I apologize, but I cannot provide any information on that topic as it falls outside the scope of my designated role as the {ROLE} assistant. My knowledge is limited to content and documents specifically marked for the {ROLE} role. If you have a query related to {ROLE}, I'd be happy to assist with that."
Under no circumstances should you attempt to generate an answer or provide information on topics that are not directly related to your assigned role. Doing so would violate the strict access control guidelines you must adhere to.
Your assigned role is: {ROLE}
You will only respond to queries directly related to the {ROLE} role. Any queries outside this scope will be politely declined with the standard response provided above. Stick to this protocol strictly without any exceptions


Be concise in your responses, sticking strictly to the facts from the listed sources below. Do not make up answers. If information is insufficient, indicate that you don't know.

Please always answer exactly what the user asks, and avoid unnecessary details. Reference sources by including at least 2 new line characters followed by the source in square brackets, like this: "\n\n [ Source : info.txt]". 

I am capable of understanding and responding in multiple languages. I will strictly provide responses in the language you select from the "Select Language" dropdown, regardless of the language you ask your question in. For English, French, and German, my responses will be the same accurate translation based on the information I have. If I am given information in English, I will convert that into the language you select. To get started, please choose your desired language from the dropdown menu.

Don't include reference source document information when "General" domain is selected from drop down.

Strictly provide friendly and appropriate responses to common greeting questions like "Hi", "Hello", "How are you?", "What is your name?"". Strictly don't include any reference sources or source document information for such type of questions.

For Example:

Question: Hi
Response: Hello! How can I assist you today?

Question: How are you?
Response: I'm doing well, thank you. How about yourself?

For "What is your role?" strictly give the role information of that particular role selected and strictly don't include reference source for "What is your role?" question.

For Example:

when Product manager role is selected:

Question: What is your role?
Answer: My role is that of a product manager. As a product manager, I analyze market trends, customer feedback, and usage data to identify opportunities. Based on customer value, technical feasibility and business impact, I prioritize features. I work with agile methodologies such as sprints, retrospectives, and continuous delivery. Success is measured by metrics such as customer adoption, customer retention, and revenue. 


IMPORTANT NOTE :
After the user's query, generate three related and insightful follow-up questions that could potentially expand the user's understanding of the topic or explore related concepts.
These follow-up questions should be based on the content and context of the user's original query and the information you have access to in your knowledge base.
Ensure that the follow-up questions are clear, concise, and relevant to the topic at hand.

"""


######################################################### Neom ##########################################################    
use_memory = st.sidebar.checkbox('**Keep History**')

    #st.session_state.messages = []
if st.sidebar.button(':red[New Topic]'):
    st.session_state.messages = []

######################################################### Neom ##########################################################    
    

######################################################### Neom ##########################################################

######################################################### Neom ##########################################################
import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key = OPENAI_API_KEY,  
  api_version = OPENAI_API_VERSION,
  azure_endpoint = OPENAI_API_ENDPOINT
)

def generate_embeddings_azure_openai(text = " "):
    response = client.embeddings.create(
        input = text,
        model= "ada-002-leap"
    )
    return response.data[0].embedding




def call_gpt_model(model= model_to_use,
                                  messages= [],
                                  temperature=0.1,
                                  max_tokens = 700,
                                  stream = True):

    print("Using model :",model_to_use)

    response = client.chat.completions.create(model=model_to_use,
                                              messages=messages,
                                              temperature = temperature,
                                              max_tokens = max_tokens,
                                              stream= stream)

    return response
    
system_message_query_generation_for_retriver = """
You are a very good text analyzer.
You will be provided a chat history and a user question.
You task is generate a search query that will return the best answer from the knowledge base.
Try and generate a grammatical sentence for the search query.
Do NOT use quotes and avoid other search operators.
Do not include cited source filenames and document names such as info.txt or doc.pdf in the search query terms.
Do not include any text inside [] or <<>> in the search query terms.
"""


def generate_query_for_retriver(user_query = " ",messages = []):

    start = time.time()
    user_message = summary_prompt_template = """Chat History:
    {chat_history}

    Question:
    {question}

    Search query:"""

    user_message = user_message.format(chat_history=str(messages), question=user_query)

    chat_conversations_for_query_generation_for_retriver = [{"role" : "system", "content" : system_message_query_generation_for_retriver}]
    chat_conversations_for_query_generation_for_retriver.append({"role": "user", "content": user_message })

    response = call_gpt_model(messages = chat_conversations_for_query_generation_for_retriver,stream = False ).choices[0].message.content
    print("Generated Query for Retriver in :", time.time()-start,'seconds.')
    print("Generated Query for Retriver is :",response)

    return response
    
    
class retrive_similiar_docs : 

    def __init__(self,query = " ", retrive_fields = ["actual_content", "metadata"],
                      ):
        if query:
            self.query = query

        self.search_client = SearchClient(AZURE_COGNITIVE_SEARCH_ENDPOINT, AZURE_COGNITIVE_SEARCH_INDEX_NAME, azure_credential)
        self.retrive_fields = retrive_fields
    
    def text_search(self,top = 2):
        results = self.search_client.search(search_text= self.query,
                                select=self.retrive_fields,top=top)
        
        return results
        

    def pure_vector_search(self, k = 2, vector_field = 'vector',query_embedding = []):

        vector_query = RawVectorQuery(vector=query_embedding, k=k, fields=vector_field)

        results = self.search_client.search( search_text=None,  vector_queries= [vector_query],
                                            select=self.retrive_fields)

        return results
        
    def hybrid_search(self,top = 2, k = 2,vector_field = "vector",query_embedding = []):
        
        vector_query = RawVectorQuery(vector=query_embedding, k=k, fields=vector_field)
        role_to_use = """Role eq """ +"'"+ ROLE + "'"
        print("Using Role :",role_to_use)
        results = self.search_client.search(search_text=self.query,  vector_queries= [vector_query],
                                                select=self.retrive_fields,top=top,filter = role_to_use)
        #print(pd.DataFrame(results))
        return results



import time
start = time.time()


def get_similiar_content(user_query = " ",
                      search_type = "hybrid",top = 2, k =2):

    #print("Generating query for embedding...")
    #embedding_query = get_query_for_embedding(user_query=user_query)
    retrive_docs = retrive_similiar_docs(query = user_query)

    if search_type == "text":
        start = time.time()
        r = retrive_docs.text_search(top =top)

        sources = []
        similiar_doc = []
        for doc in r:
            similiar_doc.append(doc["metadata"] + ": " + doc["actual_content"].replace("\n", "").replace("\r", ""))
            sources.append(doc["metadata"])
        similiar_docs = "\n".join(similiar_doc)
        print("Retrived similiar documents with text search in :", time.time()-start,'seconds.')
        #print("Retrived Docs are :",sources,"\n")

    if search_type == "vector":
        start = time.time()
        vector_of_search_query = generate_embeddings_azure_openai(user_query)
        print("Generated embedding for search query in :", time.time()-start,'seconds.')

        start = time.time()
        r = retrive_docs.pure_vector_search(k=k, query_embedding = vector_of_search_query)

        sources = []
        similiar_doc = []
        for doc in r:
            similiar_doc.append(doc["metadata"] + ": " + doc["actual_content"].replace("\n", "").replace("\r", ""))
            sources.append(doc["metadata"])
        similiar_docs = "\n".join(similiar_doc)
        print("Retrived similiar documents with text search in :", time.time()-start,'seconds.')
       # print("Retrived Docs are :",sources,"\n")


    if search_type == "hybrid":
        start = time.time()
        vector_of_search_query = generate_embeddings_azure_openai(user_query)
        print("Generated embedding for search query in :", time.time()-start,'seconds.')

        start = time.time()
        r = retrive_docs.hybrid_search(top = top, k=k, query_embedding = vector_of_search_query)

        sources = []
        similiar_doc = []
        for doc in r:
            similiar_doc.append(doc["metadata"] + ": " + doc["actual_content"].replace("\n", "").replace("\r", ""))
            sources.append(doc["metadata"])
        similiar_docs = "\n".join(similiar_doc)
        print("*"*100)
        print("Retrived similiar documents with text search in :", time.time()-start,'seconds.')
        #print("similiar_doc :", similiar_doc)
        #print("Retrived Docs are :",sources,"\n")
        #print("similiar_doc :", similiar_doc)
        #print("*"*100)
    return similiar_docs
    

def stream_response(stream_object):
    full_response = " "
    for chunk in stream_object:
        if len(chunk.choices) >0:
            if str(chunk.choices[0].delta.content) != "None": 
                full_response += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content,end = '')
    return full_response


def generate_response_without_memory(user_query = " ",stream = True,max_tokens = 512,model = " "):

    similiar_docs = get_similiar_content(user_query = user_query)
    user_content = user_query + " \nSOURCES:\n" + similiar_docs
    chat_conversations = [{"role" : "system", "content" : system_message}]
    chat_conversations.append({"role": "user", "content": user_content })
    response = call_gpt_model(messages = chat_conversations,stream = stream,max_tokens=max_tokens)
    #response = stream_response(response)
    return response


system_message = pmt+default_prompt+lang_to_use 
chat_conversations_global_message = [{"role" : "system", "content" : system_message}]


def generate_response_with_memory(user_query = " ",keep_messages = 10,new_conversation = False,model=model_to_use,stream=False):

    #global chat_conversations_to_send

#    if new_conversation:
#        st.session_state.messages = []

    
    #print(CHAT_CONVERSATION_TO_SEND)
    #print(chat_conversations_to_send)

    query_for_retriver = generate_query_for_retriver(user_query=user_query,messages = st.session_state.messages[-keep_messages:])
    similiar_docs = get_similiar_content(query_for_retriver)
    #print("Query for Retriver :",query_for_retriver)
    similiar_docs = get_similiar_content(query_for_retriver)
    user_content = user_query + " \nSOURCES:\n" + similiar_docs

    chat_conversations_to_send = chat_conversations_global_message + st.session_state.messages[-keep_messages:] + [{"role":"user","content" : user_content}]
    
    response_from_model = call_gpt_model(messages = chat_conversations_to_send)
    #print("Response_from_model :",response_from_model)
    #chat_conversations_to_send = chat_conversations_to_send[1:]
    #st.session_state.messages[-1] = {"role": "user", "content": user_query}
    #st.session_state.messages.append({"role": "assistant", "content": response_from_model})
    #print("*"*100)
    #print("chat_conversations_to_send :", chat_conversations_to_send)
    #print("*"*100)

    return response_from_model


    

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
else:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            avatar = "🤖"
        else:
            avatar = "🧑‍💻"
        with st.chat_message(message["role"],avatar = avatar ):
            st.markdown(message["content"])

# # User input
if prompt := st.chat_input("Ask me anything..."):
    # Display user message in chat message container
    st.chat_message("user",avatar = "🧑‍💻").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    user_query = prompt + dropdown_3_prompt
    if use_memory:
        response = generate_response_with_memory(user_query= user_query,stream=True)
    else :
        response = generate_response_without_memory(user_query= user_query,stream=True)

    with st.chat_message("assistant",avatar = "🤖"):
        message_placeholder = st.empty()
        full_response = " "
        # Simulate stream of response with milliseconds delay
        for chunk in response:
            if len(chunk.choices) >0:
                if str(chunk.choices[0].delta.content) != "None": 
                    full_response += chunk.choices[0].delta.content
                    #message_placeholder.markdown(full_response + "▌")
        full_response = full_response.replace("$", "\$")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})


# User input
# if prompt := st.text_input("Ask me anything..."):
#     st.chat_message("user", avatar="🧑‍💻").markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     user_query = prompt + dropdown_3_prompt

#     if use_memory:
#         response = generate_response_with_memory(user_query=user_query, stream=True)
#     else:
#         response = generate_response_without_memory(user_query=user_query, stream=True)

#     with st.chat_message("assistant", avatar="🤖"):
#         message_placeholder = st.empty()
#         full_response = ""
#         for chunk in response:
#             if len(chunk.choices) > 0:
#                 if str(chunk.choices[0].delta.content) != "None":
#                     full_response += chunk.choices[0].delta.content
#                     message_placeholder.markdown(full_response + "▌")
#         full_response = full_response.replace("$", "\$")
#         message_placeholder.markdown(full_response)

#     st.session_state.messages.append({"role": "assistant", "content": full_response})

#     # Display follow-up questions in the sidebar
#     st.sidebar.header("Follow-up Questions")
#     for i, question in enumerate(follow_up_questions, start=1):
#         question_container = st.sidebar.container()
#         with question_container:
#             st.markdown(f"**{i}. {question}**")
#             if st.button(f"Ask Question {i}", key=f"ask_question_{i}"):
#                 st.text_input("Ask me anything...", value=question)