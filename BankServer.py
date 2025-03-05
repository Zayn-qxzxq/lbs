import socket
import pickle
import os

# File for storing bank data
DATA_FILE = "bank_data.pkl"

# Load bank data if available
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        bank_data = pickle.load(f)
else:
    bank_data = {}

admins = {"admin": "password123"}  # Default admin

class BankServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print("Bank server started...")
    
    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    break
                request = pickle.loads(data)
                response = self.process_request(request)
                conn.send(pickle.dumps(response))
            except:
                break
        conn.close()
    
    def process_request(self, request):
        action = request.get("action")
        if action == "register":
            return self.register_client(request)
        elif action == "balance":
            return self.get_balance(request)
        elif action == "deposit":
            return self.deposit_money(request)
        elif action == "admin":
            return self.admin_action(request)
        return {"status": "error", "message": "Invalid action"}
    
    def register_client(self, request):
        user = request["user"]
        if user in bank_data:
            return {"status": "error", "message": "Account already exists"}
        bank_data[user] = {"balance": 0, "password": request["password"]}
        self.save_data()
        return {"status": "success", "message": "Account created"}
    
    def get_balance(self, request):
        user, password = request["user"], request["password"]
        if user in bank_data and bank_data[user]["password"] == password:
            return {"status": "success", "balance": bank_data[user]["balance"]}
        return {"status": "error", "message": "Invalid credentials"}
    
    def deposit_money(self, request):
        user, amount = request["user"], request["amount"]
        if user in bank_data:
            bank_data[user]["balance"] += amount
            self.save_data()
            return {"status": "success", "message": "Money added"}
        return {"status": "error", "message": "User not found"}
    
    def admin_action(self, request):
        admin, password = request["admin"], request["password"]
        if admin not in admins or admins[admin] != password:
            return {"status": "error", "message": "Invalid admin credentials"}
        action = request["admin_action"]
        if action == "modify":
            user, new_balance = request["user"], request["new_balance"]
            if user in bank_data:
                bank_data[user]["balance"] = new_balance
                self.save_data()
                return {"status": "success", "message": "User balance updated"}
        elif action == "delete":
            user = request["user"]
            if user in bank_data:
                del bank_data[user]
                self.save_data()
                return {"status": "success", "message": "Account deleted"}
        elif action == "export":
            return {"status": "success", "data": bank_data}
        return {"status": "error", "message": "Invalid admin action"}
    
    def save_data(self):
        with open(DATA_FILE, "wb") as f:
            pickle.dump(bank_data, f)
    
    def run(self):
        while True:
            conn, _ = self.server.accept()
            self.handle_client(conn)
            
if __name__ == "__main__":
    server = BankServer()
    server.run()
