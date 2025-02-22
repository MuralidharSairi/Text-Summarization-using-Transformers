import streamlit as st
from transformers import T5Tokenizer, TFT5ForConditionalGeneration, PegasusTokenizer, TFPegasusForConditionalGeneration, BartTokenizer, TFBartForConditionalGeneration

# Title
st.title("Text Summarization App")

# Introduction
st.write("This app allows you to generate text summaries using T5 (Large/Small), PEGASUS, and BART models in TensorFlow.")

# User Input
user_input = st.text_area("Enter the text you want to summarize:")

# Model Selection Dropdown
model_option = st.selectbox("Select a Summarization Model", ["T5 Large", "T5 Small", "PEGASUS", "BART"])

# Summarization Function
def summarize_text(model_name, input_text):
    if model_name == "T5 Large":
        model = TFT5ForConditionalGeneration.from_pretrained("t5-large")
        tokenizer = T5Tokenizer.from_pretrained("t5-large")
        max_length = 150
    elif model_name == "T5 Small":
        model = TFT5ForConditionalGeneration.from_pretrained("t5-small")
        tokenizer = T5Tokenizer.from_pretrained("t5-small")
        max_length = 50
    elif model_name == "PEGASUS":
        model = TFPegasusForConditionalGeneration.from_pretrained("google/pegasus-large")
        tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-large")
        max_length = 150
    elif model_name == "BART":
        model = TFBartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
        tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
        max_length = 150

    input_text = "summarize: " + input_text
    input_ids = tokenizer.encode(input_text, return_tensors="tf", max_length=512, truncation=True)
    summary_ids = model.generate(input_ids, max_length=max_length, num_beams=2, no_repeat_ngram_size=2)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

# Generate Summary
if st.button("Generate Summary"):
    if user_input:
        summary = summarize_text(model_option, user_input)
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Please enter some text for summarization.")