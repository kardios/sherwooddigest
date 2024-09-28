import streamlit as st
import os
import time
import requests
import json
from urlextract import URLExtract
from st_copy_to_clipboard import st_copy_to_clipboard

llama3_api_key = os.environ["PERPLEXITY_API_KEY"]
extractor = URLExtract()

st.set_page_config(page_title="Sherwood Digest", page_icon=":robot_face:",)
st.write("**Sherwood Digest**")
st.write("*Summaries at your fingertips*")

#instruction = st.selectbox("Choose your preferred output format, if necessary:", ("", "Generate a single, concise paragraph on: ", "Generate concise bullet points on: ", "Generate a full report on: "))
instruction = "Generate a single, concise paragraph summary of the weblink: "

input_text = st.text_area("Input your list of URLs:")

if st.button(":rocket:") and input_text.strip != "":
  
  urls = extractor.find_urls(input_text)

  if len(urls) > 0:
    with st.expander("Number of URLs: " + str(len(urls)), expanded = True):
      for url in urls:
        st.write(url)

  combined_output = ""
  for url in urls:
  
    start = time.time()
    
    get_url_perplexity = "https://api.perplexity.ai/chat/completions"
    payload_perplexity = {"model": "llama-3.1-sonar-huge-128k-online",
                          "messages": [{"role": "system", "content": ""},
                                       {"role": "user", "content": instruction + url, "temperature": 0}]}
    headers_perplexity = {"accept": "application/json",
                          "content-type": "application/json",
                          "Authorization": f'Bearer {llama3_api_key}'}    
    response_llama = requests.post(get_url_perplexity, json=payload_perplexity, headers=headers_perplexity)
    data_llama = json.loads(response_llama.text)
    output_text = data_llama['choices'][0]['message']['content'] 
    
    end = time.time()
    
    with st.expander(url, expanded=True):
      st.write(output_text)
      st.write("Time to generate: " + str(round(end-start,2)) + " seconds")
      st_copy_to_clipboard(output_text)

    combined_output = combined_output + url + "\n\n" + output_text + "\n\n"
    
    st.snow()

  st.write("Combined Output:")
  st_copy_to_clipboard(combined_output)
