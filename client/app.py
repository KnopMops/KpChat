from tkinter import simpledialog
import socket, threading, tkinter, tkinter.scrolledtext

HOST = simpledialog.askstring("IP аддресс", "Пожалуйста, напишите IP аддресс сервера")
PORT = 9090

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.nickname = simpledialog.askstring("Имя", "Пожалуйста, напишите свое имя")

        msg = tkinter.Tk()
        msg.withdraw()

        self.gui_done = False
        self.is_running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg="lightgray")
        self.win.title(f"Kp - Чат {HOST}:{PORT}/{self.nickname}")

        self.chat_label = tkinter.Label(self.win, text="Чат:", bg="lightgray")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state="disabled")

        self.msg_label = tkinter.Label(self.win, text="Сообщение:", bg="lightgray")
        self.msg_label.config(font=("Aria", 12))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win, text="Отправить", command=self.write)
        self.send_button.config(font=("Aria", 12))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.is_running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.is_running:
            try:
                message = self.sock.recv(1024)
                if message == 'Имя':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")
            except ConnectionAbortedError:
                break
            except Exception as _ex:
                print(f"Ошибка: {_ex}")
                self.sock.close()
                break

client = Client(HOST, PORT)