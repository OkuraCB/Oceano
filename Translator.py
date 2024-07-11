import tkinter as tk
import subprocess, os, time

from tkinter import ttk, messagebox
from PIL import ImageTk, Image
from codecs import open

from googletrans import Translator
from gtts import gTTS
import pyglet

root = tk.Tk()
root.title("Oceano")
root.geometry("620x400")
root.minsize(620, 400)

translator = Translator()

OptionsContainer = tk.Frame(root)
OptionsContainer.pack(expand= 'yes', fill= 'both')

TextContainer = tk.Frame(root)
TextContainer.pack(expand= 'yes', fill= 'both')

OperationsContainer = tk.Frame(root)
OperationsContainer.pack(expand= 'no', fill= 'both')

def resource_path(relative_path):
    try:
        base_path = os.sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def ConvertLang(Lang):
    match Lang:
        case "Portuguese":
            return "pt"
        
        case "English":
            return "en"

        case "Spanish":
            return "es"

        case "French":
            return "fr"

def PronunciationSpeech(TranslatedBox, Lang):
    file = "C:\Applications\_temp.mp3"
    
    audio = gTTS(text= TranslatedBox.get("1.0", tk.END), lang= ConvertLang(Lang), slow= False)
    audio.save(file)

    tts = pyglet.media.load(file, streaming= False)
    tts.play()

    time.sleep(tts.duration)
    os.remove(file)

def copy2clip(TranslatedBox):
    cmd = 'echo ' + TranslatedBox.get("1.0", tk.END).strip() + '|clip'
    return subprocess.check_call(cmd, shell= True)

def toTranslate(Id, Lang, TranslateBox, TranslatedBox, translator, CopyCheck):
    if Id == "Case ID":
        messagebox.showwarning(title= None, message= "Case ID not given")
        return

    Translate = TranslateBox.get("1.0", tk.END)
    Translated = translator.translate(Translate, dest= Lang)

    case_archive = open(Id + ".txt", "a", "utf-8")
    case_archive.write("\n" + Translated.text + "\n" + "===============")
    case_archive.close()

    TranslatedBox.delete("1.0", tk.END)
    TranslatedBox.insert(tk.END, Translated.text)

    if CopyCheck.get() == 1:
        cmd = 'echo ' + TranslatedBox.get("1.0", tk.END).strip() + '|clip'
        return subprocess.check_call(cmd, shell= True)

icon = ImageTk.PhotoImage(Image.open(resource_path("./oceanoicon.png")))
root.iconphoto(False, icon)

CopyCheck = tk.IntVar()
CopyCheckbox = ttk.Checkbutton(OptionsContainer, variable= CopyCheck, onvalue= 1, offvalue= 0)

lang = tk.StringVar()
lang.set("Portuguese")

langOptions = ["Portuguese", "English", "Spanish", "French"]

langMenu = tk.OptionMenu(OptionsContainer, lang, *langOptions)

TranslateBox = tk.Text(TextContainer, height= 1, width= 15)
TranslateBox.insert(tk.END, "Insert here the text to translate")

TranslatedBox = tk.Text(TextContainer, height= 1, width= 15)
TranslatedBox.insert(tk.END, "Aqui está o texto traduzido")

Id = tk.StringVar()
CaseBox = ttk.Entry(OptionsContainer, textvariable= Id)
CaseBox.insert(0, "Case ID")

copyButton = ttk.Button(OptionsContainer, text= "Copy to clipboard", command= lambda: copy2clip(TranslatedBox))
pronunciationButton = ttk.Button(OperationsContainer, text= "How to pronounce it", command= lambda: PronunciationSpeech(TranslatedBox, lang.get()))
translateButton = ttk.Button(OperationsContainer, text= "Translate", command= lambda: toTranslate(Id.get(), lang.get(), TranslateBox, TranslatedBox, translator, CopyCheck))

CaseBox.place(anchor= "e", relx= 0.21, rely= 0.425)
langMenu.place(anchor= "e", relx= 0.45, rely= 0.425)
CopyCheckbox.place(anchor= "e", relx= 0.5325, rely= 0.425)
copyButton.place(anchor= "e", relx= 0.70, rely= 0.425)

TranslateBox.pack(ipadx=85, ipady=150, side= "left", expand= "yes")
TranslatedBox.pack(ipadx=85, ipady=150, side= "left", expand= "yes")

pronunciationButton.pack(side= "right")
translateButton.pack(side= "right")

root.mainloop()