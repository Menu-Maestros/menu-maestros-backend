# **🍽️ Streamlit Menu App Backend**  
This is the **FastAPI backend** for the Streamlit-based restaurant menu application. It manages **menu items, customer orders, and authentication** while connecting to a **Neon PostgreSQL** database.  

## **📌 Features**  
✅ **Menu Management**: Add, update, delete menu items  
✅ **Order Handling**: Customers can place and update orders  
✅ **Authentication**: JWT-based security for restaurant-side users  
✅ **Database**: Uses **Neon PostgreSQL** for serverless storage  
✅ **Asynchronous API**: Powered by FastAPI and SQLAlchemy  

---

## **🚀 Getting Started**  

### **🔹 1. Clone the Repository**  
```bash
git clone https://github.com/your-username/streamlit-menu-app-backend.git
cd streamlit-menu-app-backend
```

### **🔹 2. Set Up Environment Variables**  
Create a `.env` file inside the project folder with:  
```
DATABASE_URL=postgresql+asyncpg://user:password@your-neon-db-url/dbname
JWT_SECRET_KEY=your-secret-key
```

---

## **🐳 Running with Docker**  

### **🔹 3. Build & Run the Docker Container**  
```bash
docker build -t streamlit-menu-backend .
docker run -p 8000:8000 --env-file .env streamlit-menu-backend
```

### **🔹 4. API Documentation (Swagger UI)**  
Once the server is running, visit:  
📌 **[http://localhost:8000/docs](http://localhost:8000/docs)**  

---

## **🔧 Running Locally Without Docker**  
**1️⃣ Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

**2️⃣ Install Dependencies**  
```bash
pip install -r requirements.txt
```

**3️⃣ Start the Server**  
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## **📌 API Endpoints**
| Method | Endpoint         | Description                  | Auth Required? |
|--------|----------------|-----------------------------|---------------|
| `POST` | `/menu/add`     | Add a menu item             | ✅ Yes        |
| `GET`  | `/menu/list`    | Get all menu items          | ❌ No         |
| `POST` | `/order/create` | Create a new customer order | ❌ No         |
| `GET`  | `/orders`       | Get all orders (restaurant) | ✅ Yes        |

---

## **🛠️ Technologies Used**  
- **FastAPI** (Backend Framework)  
- **SQLAlchemy + AsyncPG** (Database ORM)  
- **Neon PostgreSQL** (Serverless DB)  
- **Docker** (Containerization)  

---

### **🚀 Future Enhancements**  
- ✅ WebSockets for real-time order updates  
- ✅ Restaurant dashboard UI with Streamlit  
- ✅ Payment integration  

---

### **👨‍💻 Chat Guides**  
If want to follow the original chat thread that gave rise to all this backend see my [ChatGPT paircoding](https://chatgpt.com/share/67d4888a-fd74-8010-a2a9-00ef00001e44).

---

This README covers **installation, setup, and API usage** while keeping it **concise and developer-friendly**. Let me know if you'd like any tweaks! 🚀🔥

### 
