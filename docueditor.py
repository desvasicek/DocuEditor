from guizero import *
import sys
from PIL import Image
favicon = Image.open("/home/pi/DocuEditor/favicon.ico")
secondary_icon = Image.open("/home/pi/DocuEditor/d.ico")
app = App('Docueditor', 1000, 1000, bg='#2B2B2B')
app.icon = favicon
saves = []
htmltemp = '''
<!DOCTYPE HTML>
<html>
    <head>
        <title></title>
        <meta name="keywords" content="">
        <meta name="description" content="">
        <link rel="stylesheet" href="">
        <script src=""></script>
    </head>
    <body>
        <h1></h1>
        <p></p>
        <p></p>
        <footer></footer>
    </body>
</html>
'''
jstemp = '''
window.onload = function init() {
    console.log("")
}
'''
pytemp = '''
def __init__():
    print('Hello, World')
'''
def get_file():
    file_returned = app.select_file(title='Select a File to Edit', folder="/")
    if file_returned:
        contents = open(file_returned, 'r')
        try:
            file.value = file_returned
            editor.value = contents.read()
            app.title = 'DocuEditor - ' + file_returned
            editor.enabled = True
            saves = []
        except UnicodeDecodeError:
            app.error('Error', 'This file contains unicode this program cannot read...')
            file.value = 'No File Selected'
            editor.value = 'File Contents'
            app.title = 'DocuEditor'
            editor.enabled = False
    else:
        file.value = 'No File Selected'
def select():
    get_file()
def create():
    name = app.question('Name  your File', 'Enter your file name below', 'new.txt')
    path = app.select_folder('Select a Path')
    name = os.path.join(path, name)
    new_file = open(name, 'x')
    new_file.close()
    file.value = name
    this_file = open(name, 'r')
    editor.value = this_file.read()
    editor.enabled = True
def save():
    file_edit = open(file.value, 'w')
    file_edit.write(editor.value)
def clear():
    editor.value = ''
def exitApp():
    close()
def close():
    yesno = app.yesno('Save?', '')
    if yesno:
        save()
        app.destroy()
    else:
        app.destroy()
def html():
    editor.value = htmltemp
def js():
    editor.value = jstemp
def py():
    editor.value = pytemp
menubar = MenuBar(app,
                  toplevel=["File", "Edit", "Templates"],
                  options=[
                      [ ["Exit", exitApp], ["Save", save], ["Select New", select], ["Create New", create] ],
                      [ ["Clear", clear] ],
                      [ ["HTML", html], ["JavaScript", js], ["Python", py], ["None", clear] ]
                  ])
app.text_color = "#B3B3B3"
file = Text(app, 'No File Selected', font='Ubuntu', size=15)
editor = TextBox(app, 'File Contents', width=990, height=980, multiline=True, enabled=False, scrollbar=True)
app.tk.config(cursor="arrow")
menubar.tk.config(cursor="arrow")
editor.tk.config(cursor="arrow")
app.when_closed = close
get_file()
app.display()