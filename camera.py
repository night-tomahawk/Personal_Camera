import tkinter as tk
import cv2
import re
from tkinter import Label, PhotoImage, simpledialog, messagebox

cam = None
brightness = 50
current_frame = None


def adjust_brightness(val):
    global brightness
    brightness = int(val)


def on_start_camera():
    global cam
    cam = cv2.VideoCapture(0)
    show_frame()


def get_message(title: str, prompt: str):
    return {"title": title, "prompt": prompt}


def show_frame():
    global cam, brightness, current_frame
    _, frame = cam.read()

    beta = brightness - 50
    bright_frame = cv2.convertScaleAbs(frame, beta=beta)

    current_frame = bright_frame
    cv2.imshow("Smile camera", bright_frame)
    if cv2.waitKey(10) & 0xFF != ord('q'):
        window.after(10, show_frame)


def save_frame(current_frame):
    messages = {
        "save": get_message("Сохранить изображение", "Введите имя файла"),
        "error": get_message("Ошибка", "Неверный формат имени"),
        "success": get_message("Готово", "Снимок успешно сохранен!"),
    }

    filename_pattern = r'^[A-Za-z0-9-_]{1,16}$'

    if current_frame is not None:
        filename = simpledialog.askstring(messages["save"]["title"],
                                          messages["save"]["prompt"])

        if filename is None:
            return
        if not re.search(filename_pattern, filename):
            messagebox.showerror(messages["error"]["title"],
                                 messages["error"]["prompt"])
            return

        cv2.imwrite(filename + ".jpg", current_frame)
        messagebox.showinfo(messages["success"]["title"],
                            messages["success"]["prompt"])

    else:
        messagebox.showerror('Не удалось сохранить снимок!')


def on_closing():
    global cam
    if cam is not None:
        cam.release()
    cv2.destroyAllWindows()
    window.destroy()


window = tk.Tk()
window.title('Camera')
window.geometry('800x800')
background_img = PhotoImage(file='821543.png')
background_label = Label(window, image=background_img)
background_label.place(relwidth=1, relheight=1)


def get_button(text: str, bg: str, fg: str, padx: int, pady: int, command):
    return tk.Button(window, text=text, font=('Times New Roman', 24), bg=bg, fg=fg, padx=padx, pady=pady, command=command)


Label = tk.Label(window, text='Добро пожаловать!', font=('Times New Roman', 24))
Label.pack(pady=20)
# button_start = tk.Button(window, text='Начать просмотр', bg='blue', fg='white', padx=30, pady=30,
#                          font=('Times New Roman', 20), command=on_button_click)
button_start = get_button("Начать просмотр", "blue", "white", 30, 30, on_start_camera)
button_start.pack(pady=10)
button_save = get_button("Сохранить снимок", "green", "white", 30, 30, command=lambda: save_frame(current_frame))

# button_save = tk.Button(window, text='Сохранить снимок', bg='green', fg='white', padx=40, pady=40,
#                         font=('Times New Roman', 20), command=lambda: save_frame(current_frame))
button_save.pack(pady=10)

button_stop = tk.Button(window, text='Закрыть приложение', bg='blue', fg='white', padx=50, pady=50,
                        font=('Times New Roman', 20), command=on_closing)
button_stop.pack(pady=10)
brightness_scale = tk.Scale(window, from_=0, to=100, label='Уровень яркости', orient=tk.HORIZONTAL,
                            command=adjust_brightness)
brightness_scale.set(brightness)
brightness_scale.pack(pady=20)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
