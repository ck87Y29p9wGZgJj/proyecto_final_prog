import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Gestión de Citas Médicas")
    root.geometry("800x600")

    label = tk.Label(root, text="Bienvenido al Sistema de Gestión de Citas", font=("Arial", 16))
    label.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
