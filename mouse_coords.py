import tkinter as tk
import pyautogui
import pyperclip
import threading
from pynput import mouse

OFFSET_X = 15    # décalage à droite du pointeur
OFFSET_Y = 20    # décalage en bas du pointeur
REFRESH_MS = 30  # fréquence d'update (ms)

def main():
    root = tk.Tk()
    root.overrideredirect(True)  # pas de bordure
    root.attributes("-topmost", True)  # toujours au-dessus

    label = tk.Label(root, text="0, 0", font=("Consolas", 11),
                     bg="#222", fg="#00ff88", padx=4, pady=2)
    label.pack()

    coords = {"x": 0, "y": 0}

    def update():
        x, y = pyautogui.position()
        coords["x"], coords["y"] = x, y
        label.config(text=f"{x}, {y}")
        root.geometry(f"+{x + OFFSET_X}+{y + OFFSET_Y}")
        root.after(REFRESH_MS, update)

    def flash():
        """Effet visuel temporaire lors d'une copie."""
        label.config(bg="#005500")
        root.after(150, lambda: label.config(bg="#222"))

    def on_click(x, y, button, pressed):
        if pressed and button.name == "right":
            # Copier dans le presse-papier
            pyperclip.copy(f"{coords['x']}, {coords['y']}")
            flash()

    # Lancement de l’écoute souris dans un thread à part
    listener = mouse.Listener(on_click=on_click)
    listener.daemon = True
    listener.start()

    update()
    root.mainloop()

if __name__ == "__main__":
    main()
