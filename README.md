# **🍽️ Streamlit Menu App Backend**  
This is the **FastAPI backend** for the Streamlit-based restaurant menu application.

## **📌 Features**  
✅ **Menu Management**: Add, update, delete menu items  
✅ **Order Handling**: Customers can place and update orders  
<!-- ✅ **Authentication**: JWT-based security for restaurant-side users   -->
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
```
<!-- JWT_SECRET_KEY=your-secret-key -->
<!-- ``` -->

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

Still configuring Swagger for easy API Endpoints documentation
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