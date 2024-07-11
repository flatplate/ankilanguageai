import requests 
import json

# Configure OpenAI API
API_URL = 'https://api.openai.com/v1/chat/completions'

prompt = """
You are a helpful assistant that provides information about German words.
Given a german word by the user, provide the following information:
1. Meaning in English
5. Type of the word (noun, verb, etc.)
2. Article (der/die/das), only if the word is a noun
3. A sample sentence in German. Meaning should not be obvious from the sentence.
4. The sample sentence with the articles omitted with ___
4. Translation of the sample sentence in English
Format the response as JSON with keys: meaning, word_type, article, sample_sentence, sentence_translation, omitted_sentence.
Sample word: Eselbrücke
Sample response: {"meaning": "mnemonic", "word_type": "noun", "article": "die", "sample_sentence": "Ich habe die Formeln mithilfe einer Eselbrucke gelernt", "sentence_translation": "A mnemonic is a memory aid.", "omitted_sentence": "Ich habe die Formeln mithilfe ___ Eselbrucken gelernt"}
"""

def get_fields_for_word(word, api_key):
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-4-turbo',
            'messages': [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Provide information for the German word '{word}'"}
            ],
            "response_format": {
                "type": "json_object"
            }
        }

        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        result = json.loads(response.json()['choices'][0]['message']['content'])
        
        # Assuming your note type has fields named: Word, Meaning, Article, Sample, Translation
        # Update the front field (word and sample sentence)
        front_html = f"""
        <div style="font-size: 1.2em;">
            <strong>{word}</strong>
        </div>
        <div style="margin-top: 10px; font-style: italic; color: #FDFFAB;">
            {result['omitted_sentence']}
        </div>
        """

        # Update the back field (meaning, article, and sentence translation)
        back_html = f"""
        <div style="font-size: 1.1em;">
            <strong>Meaning:</strong> <span style="color: #FFCF81;">{result['meaning']}</span>
        </div>
        <div style="margin-top: 10px;">
            <strong>Article:</strong> <span style="color: #FFB996;">{result['article']}</span>
        </div>
        <div style="margin-top: 10px;">
            <strong>Sample:</strong>
            <div style="margin-left: 20px; font-style: italic; color: #FDFFAB;">
                {result['sample_sentence']}
            </div>
            <div style="margin-left: 20px; color: #FFCF81;">
                {result['sentence_translation']}
            </div>
        </div>
        """
        return front_html, back_html
    except requests.exceptions.RequestException as e:
        raise Exception(f"An error occurred while contacting the API: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("Failed to parse the API response.")
    except KeyError:
        raise Exception("The API response did not contain the expected data.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    print("This is an Anki plugin for filling out fields using OpenAI.")
    print("Starting test")
    word = "Hund"
    front, back = get_fields_for_word(word)
    print(front)
    print(back)
