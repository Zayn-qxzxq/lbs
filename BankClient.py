import socket  
import pickle
import tkinter as tk
from tkinter import messagebox, simpledialog

class BankClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
    
    def send_request(self, request):
        self.client.send(pickle.dumps(request))
        return pickle.loads(self.client.recv(4096))

    def register(self, user, password):
        return self.send_request({"action": "register", "user": user, "password": password})

    def get_balance(self, user, password):
        return self.send_request({"action": "balance", "user": user, "password": password})
    
    def admin_action(self, admin, password, action, **kwargs):
        request = {"action": "admin", "admin": admin, "password": password, "admin_action": action}
        request.update(kwargs)
        return self.send_request(request)

def register():
    username = simpledialog.askstring("Register", "Enter username:")
    password = simpledialog.askstring("Register", "Enter password:", show='*')
    if username and password:
        response = client.register(username, password)
        messagebox.showinfo("Response", response["message"])

def check_balance():
    username = simpledialog.askstring("Balance", "Enter username:")
    password = simpledialog.askstring("Balance", "Enter password:", show='*')
    if username and password:
        response = client.get_balance(username, password)
        if response["status"] == "success":
            messagebox.showinfo("Balance", f"Your balance: {response['balance']}")
        else:
            messagebox.showerror("Error", response["message"])

def admin_actions():
    admin = simpledialog.askstring("Admin", "Admin username:")
    password = simpledialog.askstring("Admin", "Admin password:", show='*')
    action = simpledialog.askstring("Admin", "Enter action (modify/delete/export):")
    if action == "modify":
        user = simpledialog.askstring("Modify", "Enter username to modify:")
        new_balance = simpledialog.askfloat("Modify", "Enter new balance:")
        response = client.admin_action(admin, password, "modify", user=user, new_balance=new_balance)
    elif action == "delete":
        user = simpledialog.askstring("Delete", "Enter username to delete:")
        response = client.admin_action(admin, password, "delete", user=user)
    elif action == "export":
        response = client.admin_action(admin, password, "export")
        messagebox.showinfo("Export", f"Data: {response['data']}")
        return
    else:
        messagebox.showerror("Error", "Invalid admin action")
        return
    messagebox.showinfo("Response", response["message"])

client = BankClient()
root = tk.Tk()
root.title("Bank Client")

# Adding the text to the GUI
label = tk.Label(root, text="220103389 220103352 220103146 220103081 220103119", font=("Arial", 12, "bold"))
label.pack(pady=10)

tk.Button(root, text="Register", command=register).pack(pady=5)
tk.Button(root, text="Check Balance", command=check_balance).pack(pady=5)
tk.Button(root, text="Admin Actions", command=admin_actions).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit).pack(pady=5)

root.mainloop()
