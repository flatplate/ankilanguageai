import json
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, qconnect
from aqt.gui_hooks import editor_did_init_buttons
import requests
from .get_fields_for_words import get_fields_for_word

config = mw.addonManager.getConfig(__name__)
api_key = config["openaiApiKey"]
model = config["openaiModel"]

def fill_out_fields(editor):
    if not editor.note:
        showInfo("No note selected.")
        return

    # Assuming the first field is the German word
    word = editor.note.fields[0]
    
    if not word:
        showInfo("Please enter a German word in the first field.")
        return

    try:
        front, back = get_fields_for_word(word)
        editor.note.fields[0] = front
        editor.note.fields[1] = back
        
        editor.loadNote()
        showInfo("Fields filled out successfully!")
    except Excpetion as e:
        showInfo(str(e))

def add_fill_out_button(buttons, editor):
    button = editor.addButton(
        icon=None,  # You can add an icon file here if you want
        cmd="fill_out",
        func=lambda e=editor: fill_out_fields(e),
        tip="Fill out fields using OpenAI",
        label="Fill out"
    )
    buttons.append(button)

editor_did_init_buttons.append(add_fill_out_button)

