import requests
from bs4 import BeautifulSoup
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load GPT-2 model and tokenizer
model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)


def generate_bookmark_description(url):
    try:
        # print("fetching")
        response = requests.get(url)
        # print("received")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch page: {str(e)}")

    # Parse the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    
    meta_description = soup.find('meta', attrs={'name': 'description'})
    # print(meta_description)
    if meta_description and meta_description.get('content'):
        return meta_description['content']
    else:
        return generate_summary_using_gpt2(soup.get_text())


def generate_summary_using_gpt2(page_text):
    # Limit the input size for GPT-2 (since it's not trained for long contexts)
    max_input_length = 512
    input_text = page_text[:max_input_length] if len(page_text) > max_input_length else page_text

    inputs = tokenizer.encode(input_text, return_tensors="pt")

    # Generate description using GPT-2
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1, no_repeat_ngram_size=2)
    
    # Decode generated text
    return tokenizer.decode(outputs[0], skip_special_tokens=True)



















# import requests
# from bs4 import BeautifulSoup
# from langchain.llms import HuggingFaceHub


# def generate_description_from_url(url):
#     # Step 1: Get the web page content
#     try:
#         response = requests.get(url)
#     except requests.exceptions.RequestException as e:
#         raise ValueError(f"Failed to fetch page: {str(e)}") from e
#     # Step 2: Parse the page using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')

#     # Step 3: Try to find the meta description
#     meta_description = soup.find('meta', attrs={'name': 'description'})
#     if meta_description and meta_description.get('content'):
#         return meta_description['content']
#     else:
#         # If no meta description is found, summarize the page content
#         return generate_summary(soup.get_text())
    
# def generate_summary(page_text):
#     # You can customize this to use a smaller, faster model if needed
#     model = HuggingFaceHub(repo_id="facebook/bart-large-cnn", model_kwargs={"temperature": 0.7})
    
#     # Pass the page content to the model to generate a summary
#     return model.generate(page_text)
   

