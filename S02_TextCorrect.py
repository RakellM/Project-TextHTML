# %%
#!pip install openai
#!pip install tiktoken

# %%
# LIBRARY
import openai
from openai import OpenAI, RateLimitError
import tiktoken
from bs4 import BeautifulSoup
import re
import time

# %%
# FUNCTION
#Read HTML or EPUB file content
def read_file(file_path):
    """
    Read the file content ans return a string.
    
    Args:
        file_path (str): Path of the file to be read.
    
    Returns:
        str: File content.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# %%
# FUNCTION
#Correct text using API from OpenAI
def openAi_text_process(text):
    prompt = f"""
    Corrija o texto a seguir, ajustando apenas:
    1. Hífens mal colocados devido a quebras de linha (ex.: "le- vadiça" deve virar "levadiça").
    2. Espaços duplos (ex.: "texto  espaço" deve virar "texto espaço").
    3. Parágrafos cortados indevidamente (unifique parágrafos que pertencem à mesma frase ou ideia, mantendo a estrutura HTML).
    Não altere ortografia, legibilidade ou hífens legítimos (ex.: "arrastou-se" deve permanecer como está).
    Preserve a formatação HTML e parágrafos vazios (<p class="calibre2"> </p>).
    Retorne o texto corrigido no formato HTML.

    Texto:
    {text}
    """

    # Usar a nova sintaxe da API
    client = openai.OpenAI(api_key=openai.api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Ou "gpt-4o" se disponível
        messages=[
            {"role": "system", "content": "Você é um assistente que corrige textos mantendo fidelidade ao conteúdo original."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=4096,
        temperature=0.3  # Baixa temperatura para respostas precisas
    )

    return response.choices[0].message.content

# %%
# Função para processar um arquivo HTML ou EPUB
def process_file(input_file, output_file):
    content = input_file

    # Parsear HTML with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Process complete text
    text_complete = str(soup)
    text_corrected = corrigir_texto(text_complete)

    # Salve corrected text
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text_corrected)

# %%
#Function to preprocess text locally
def preprocess_text(text):
    """
    Performs local automatic corrections on the text:
    - Replaces </i> <i class="calibre3"> with a single space.
    - Removes <p class="calibre2"> </p> (empty paragraphs).
    - Replaces multiple spaces with a single space.
    
    Args:
        text (str): Input HTML text.
    
    Returns:
        str: Preprocessed text.
    """
    # First do the string replacement before parsing with BeautifulSoup
    text = re.sub(r'</i> <i class="calibre3">', ' ', text)
    text = re.sub(r'<i class="calibre3">', '<i>', text)
    #text = re.sub(r'<p class="calibre2">', '<p>', text)

    # Parse the text with BeautifulSoup
    soup = BeautifulSoup(text, 'html.parser')
    
    # Replace <i class="calibre3"> </i> with a space
    for i_tag in soup.find_all('i'): #, class_='calibre3'):
        if not i_tag.get_text().strip():  # Check if the tag is empty
            i_tag.replace_with(' ')
    
    # Remove <p class="calibre2"> </p> (empty paragraphs)
    for p_tag in soup.find_all('p'): #, class_='calibre2'):
        if not p_tag.get_text().strip():
            p_tag.decompose()
    
    # Convert back to string
    preprocessed_text = str(soup)
    
    # Replace multiple spaces with a single space
    preprocessed_text = re.sub(r'\s{2,}', ' ', preprocessed_text)
    
    return preprocessed_text

# %%
# FUNCTION
#Count tolkens in a text file using tiktoken
def count_tokens(text, model="gpt-3.5-turbo"):
    """
    Count the number of tokens of a file using tiktoken.
    
    Args:
        text (str): Text to be analysed.
        model (str): Modelo da OpenAI (eg.: 'gpt-3.5-turbo' or 'gpt-4o').
    
    Returns:
        int: Estimate number of tokens.
    """
    # Carregar o codificador de tokens para o modelo especificado
    encoding = tiktoken.encoding_for_model(model)

    # Count tokens
    tokens = encoding.encode(text)
    return len(tokens)

# Exemplo de uso
# num_tokens = count_tokens(arquivo_entrada, model="gpt-3.5-turbo")
# print(f"O arquivo contém aproximadamente {num_tokens} tokens.")

# %%
# FUNCTION
#This function divides a text into smaller parts, each with a maximum number of characters.
def divide_text(text, max_caracteres=40000):
    parts = []
    while text:
        parts.append(text[:max_caracteres])
        text = text[max_caracteres:]
    return parts

# %%
# DATA
## API Key
#Configurar a chave da API da OpenAI
openai.api_key = read_file("./OpenAI_API_Key.txt").strip()

## Original file
original_file = read_file("./output_files/part_018.txt")

## Output file path
output_file_path = "./output_files/part_018_corrigido.txt"

# %%
local_process_file = preprocess_text(original_file)

# %%
num_tokens = count_tokens(local_process_file, model="gpt-3.5-turbo")
print(f"O arquivo contém aproximadamente {num_tokens} tokens.")

# %%
BeautifulSoup(local_process_file, 'html.parser')

# %%
# texto muito grande
#final_text = openAi_text_process(local_process_file)

# %%
