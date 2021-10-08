#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel,  QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout

import json

app = QApplication([])

notes = {
    "Добро пожаловать!" : {
        "text" : "Это самое лучшее приложение для заметок в мире!",
        "tags" : ["добро","инструкция"]
    },
    "Заметка 2" : {
        "text" : "sdfghjkl;lkjhgfdsxdfghjkl;lkjhgfdsdfghj",
        "tags" : ["Текстовый тег"]
    }
}
with open("notes_data.json", "w") as file:
    json.dump(notes, file)



notes_win = QWidget()
notes_win.setWindowTitle('Умные заметки')
notes_win.resize(900,600)

list_notes = QListWidget()
list_notes_label = QLabel('Список заметок')

button_note_create = QPushButton('Создать заметку')
button_note_del = QPushButton('Удалить заметку')
button_note_save = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()
button_tag_add = QPushButton('Добавить к заметке')
button_tag_del = QPushButton('Открепить от заметки')
button_tag_search = QPushButton('Искать заметки по тегу')
list_tags = QListWidget()
list_tags_label = QLabel('Список тегов')

layout_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

gor_1 = QHBoxLayout()
gor_1.addWidget(button_note_create)
gor_1.addWidget(button_note_del)
gor_2 = QHBoxLayout()
gor_2.addWidget(button_note_save)
gor_3 = QHBoxLayout()
gor_3.addWidget(button_tag_add)
gor_3.addWidget(button_tag_del)
gor_4 = QHBoxLayout()
gor_4.addWidget(button_tag_search)

col_2.addLayout(gor_1)
col_2.addLayout(gor_2)
col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)
col_2.addLayout(gor_3)
col_2.addLayout(gor_4)

layout_notes.addLayout(col_1)
layout_notes.addLayout(col_2)

notes_win.setLayout(layout_notes)
'''Функционал'''
'''Текст'''

def add_note():
    note_name, ok = QInputDialog.getText(notes_win, 'Добавить заметку', 'Название заметки:')
    if ok and note_name != '':
        notes[note_name] = {'текст':'','теги':[]}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])
        print(notes)

def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    #text = notes[key]['text']
    field_text.setText("text")
    list_tags.clear()
    tags = notes[key]['tags']
    list_tags.addItems(tags)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст']= field_text.toPlainText()
        with open('notes_data.json','w') as file:
            json.dump(notes,file,sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для сохранения не выбрана!')

def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open("notes_data.json","w") as file:
            json.dump(notes, file, sort_keys= True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для удаления не выбрана!')

        '''Теги'''
def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["tags"]:
            notes[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file , sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('Заметка для добавления тега не выбрана!')

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['tags'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
            print('Тег для удаления не выбран!')

def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()
    if button_tag_search.text() == "Искать заметки по тегу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['tags']:
                notes_filtered[note]=notes[note]
        button_tag_search.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(button_tag_search.text())
    elif button_tag_search.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')
        print(button_tag_search.text())
    else:
        pass

'''Запуск'''
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)

list_notes.itemClicked.connect(show_note)
with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)

notes_win.show()
app.exec_()







