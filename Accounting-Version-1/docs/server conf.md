### **Backend Deployment Instructions**

1. **Update the System**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Required Packages**:
   Install Python, pip, and virtualenv:
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

3. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd Lifeline-Accounting-Software/Accounting-Version-1/backend
   ```

4. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

5. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

6. **Set Up the Database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Collect Static Files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

8. **Run the Backend Server**:
   Replace `<your_server_ip>` with your server's IP address:
   ```bash
   python manage.py runserver <your_server_ip>:8000
   ```

---

### **Frontend Deployment Instructions**

1. **Install Node.js and npm**:
   ```bash
   sudo apt install nodejs npm -y
   ```

2. **Navigate to the Frontend Directory**:
   ```bash
   cd Lifeline-Accounting-Software/Accounting-Version-1/frontend
   ```

3. **Install Dependencies**:
   ```bash
   npm install
   ```

4. **Build the Frontend**:
   ```bash
   npm run build
   ```

5. **Serve the Frontend**:
   Install a static file server (e.g., `serve`):
   ```bash
   npm install -g serve
   serve -s dist -l 80
   ```

---

### **Optional: Use a Process Manager (e.g., PM2) for Backend and Frontend**

1. **Install PM2**:
   ```bash
   npm install -g pm2
   ```

2. **Run the Backend with PM2**:
   ```bash
   pm2 start "python manage.py runserver <your_server_ip>:8000" --name backend
   ```

3. **Run the Frontend with PM2**:
   ```bash
   pm2 start "serve -s dist -l 80" --name frontend
   ```

4. **Save PM2 Process List**:
   ```bash
   pm2 save
   ```

5. **Set PM2 to Start on Boot**:
   ```bash
   pm2 startup
   ```

---

### **Additional Notes**
- Replace `<repository_url>` with the URL of your Git repository.
- Replace `<your_server_ip>` with your server's IP address.
- Ensure ports `8000` (backend) and `80` (frontend) are open in your firewall.