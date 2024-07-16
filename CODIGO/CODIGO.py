import telepot
import sqlite3
import os
from TOKEN import TOKEN

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'crud_bot.db')

def create_table():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS items
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 item TEXT)''')
    conn.commit()
    conn.close()

def add_item(item_text):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO items (item) VALUES (?)', (item_text,))
    conn.commit()
    conn.close()

def list_items():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return items

def update_item(item_id, new_text):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE items SET item = ? WHERE id = ?', (new_text, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    if content_type == 'text':
        command = msg['text'].lower()
        
        if command == '/start':
            bot.sendMessage(chat_id, '😀Bem-vindo! Use /add para adicionar um item, /list para ver todos os itens, /update para atualizar um item e /delete para deletar um item.')
        
        elif command.startswith('/add'):
            item_text = command.replace('/add', '').strip()
            if item_text:
                add_item(item_text)
                bot.sendMessage(chat_id, f'Item "{item_text}" adicionado com sucesso.')
            else:
                bot.sendMessage(chat_id, 'Por favor, envie o texto do item após o comando /add.')
        
        elif command == '/list':
            items = list_items()
            if items:
                item_list = '\n'.join(f'{item[0]}. {item[1]}' for item in items)
                bot.sendMessage(chat_id, f'Lista de itens:\n{item_list}')
            else:
                bot.sendMessage(chat_id, 'Nenhum item encontrado.')
        
        elif command.startswith('/update'):
            try:
                item_id, new_text = command.replace('/update', '', 1).strip().split(maxsplit=1)
                item_id = int(item_id)
                update_item(item_id, new_text)
                bot.sendMessage(chat_id, f'Item {item_id} atualizado para "{new_text}".')
            except ValueError:
                bot.sendMessage(chat_id, 'Formato inválido. Use /update ID NOVO_TEXTO.')
            except Exception as e:
                bot.sendMessage(chat_id, f'Ocorreu um erro ao atualizar o item: {str(e)}')
        
        elif command.startswith('/delete'):
            try:
                item_id = int(command.replace('/delete', '').strip())
                delete_item(item_id)
                bot.sendMessage(chat_id, f'Item {item_id} deletado com sucesso.')
            except ValueError:
                bot.sendMessage(chat_id, 'Formato inválido. Use /delete ID.')
            except Exception as e:
                bot.sendMessage(chat_id, f'Ocorreu um erro ao deletar o item: {str(e)}')

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

print('BOT EM EXECUÇÃO...')
create_table()  

while True:
    pass
