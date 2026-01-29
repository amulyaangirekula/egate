import mysql.connector
from mysql.connector import Error
import datetime
from backend.config import DB_CONFIG  # Import the config

class FaceRecognitionDB:
    def __init__(self, host, user, password, database):
        """Initialize database connection"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.initialize_database()
        
    def connect(self):
        """Create a connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            return self.connection
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return None
    
    def initialize_database(self):
        """Create database and tables if they don't exist"""
        try:
            conn = mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            cursor = conn.cursor()
            
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            conn.close()
            
            conn = self.connect()
            if conn is None:
                return
                
            cursor = conn.cursor()
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                id_number VARCHAR(20) NOT NULL,
                email VARCHAR(100) NOT NULL,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS gate_access (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                date DATE NOT NULL,
                time TIME NOT NULL,
                status VARCHAR(20) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                faces_count INT,
                status VARCHAR(20)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS gate_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE NOT NULL,
                time TIME NOT NULL,
                users_recognized INT,
                duration FLOAT
            )
            ''')
            
            conn.commit()
            conn.close()
            print("Database and tables initialized successfully")
            
        except Error as e:
            print(f"Error initializing database: {e}")
    
    def add_user(self, name, id_number, email):
        """Add a new user and return the user ID"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute("SELECT id FROM users WHERE id_number = %s", (id_number,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                return existing_user[0] 
            
            cursor.execute(
                "INSERT INTO users (name, id_number, email) VALUES (%s, %s, %s)",
                (name, id_number, email)
            )
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            
            return user_id
            
        except Error as e:
            print(f"Error adding user: {e}")
            return None

    def get_user_details(self, user_id):
        """Get user details by ID"""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            
            conn.close()
            return user
            
        except Error as e:
            print(f"Error getting user details: {e}")
            return None

    def record_gate_access(self, user_id, date, time_str, status):
        """Record user gate access"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO gate_access (user_id, date, time, status) VALUES (%s, %s, %s, %s)",
                (user_id, date, time_str, status)
            )
            conn.commit()
            conn.close()
            return True
            
        except Error as e:
            print(f"Error recording gate access: {e}")
            return False

    def get_access_count(self, user_id):
        """Get the number of times a user has accessed the gate"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT COUNT(*) FROM gate_access WHERE user_id = %s AND status = 'Granted'",
                (user_id,)
            )
            count = cursor.fetchone()[0]
            
            conn.close()
            return count
            
        except Error as e:
            print(f"Error getting access count: {e}")
            return 0
 

    def log_training(self, faces_count, status="Completed"):
        """Log training session"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO training_log (faces_count, status) VALUES (%s, %s)",
                (faces_count, status)
            )
            
            conn.commit()
            conn.close()
            return True
            
        except Error as e:
            print(f"Error logging training: {e}")
            return False
    
    def log_gate_session(self, date, time_str, users_recognized, duration):
        """Log gate monitoring session"""
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            cursor.execute(
                "INSERT INTO gate_sessions (date, time, users_recognized, duration) VALUES (%s, %s, %s, %s)",
                (date, time_str, users_recognized, duration)
            )
            
            conn.commit()
            conn.close()
            return True
            
        except Error as e:
            print(f"Error logging gate session: {e}")
            return False

    def get_all_users(self):
        """Get all users"""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users ORDER BY name")
            users = cursor.fetchall()
            
            conn.close()
            return users
            
        except Error as e:
            print(f"Error getting users: {e}")
            return []
    
    def get_user_gate_access(self, user_id, start_date=None, end_date=None):
        """Get gate access records for a specific user"""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM gate_access WHERE user_id = %s"
            params = [user_id]
            
            if start_date:
                query += " AND date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND date <= %s"
                params.append(end_date)
                
            query += " ORDER BY date DESC, time DESC"
            
            cursor.execute(query, params)
            access_records = cursor.fetchall()
            
            conn.close()
            return access_records
            
        except Error as e:
            print(f"Error getting gate access records: {e}")
            return []

    def get_all_gate_access(self, date=None):
        """Get all gate access records, optionally filtered by date"""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT ga.*, u.name, u.id_number, 
                (SELECT COUNT(*) FROM gate_access WHERE user_id = ga.user_id AND status = 'Granted') as access_count
                FROM gate_access ga
                LEFT JOIN users u ON ga.user_id = u.id
            """
            
            params = []
            if date:
                query += " WHERE ga.date = %s"
                params.append(date)
                
            query += " ORDER BY ga.date DESC, ga.time DESC"
            
            cursor.execute(query, params)
            access_records = cursor.fetchall()
            
            conn.close()
            return access_records
            
        except Error as e:
            print(f"Error getting all gate access records: {e}")
            return []

    def get_filtered_gate_access(self, start_date=None, end_date=None, search_term=None, status=None):
        """Get filtered gate access records"""
        try:
            conn = self.connect()
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT ga.*, u.name, u.id_number,
                (SELECT COUNT(*) FROM gate_access WHERE user_id = ga.user_id AND status = 'Granted') as access_count
                FROM gate_access ga
                LEFT JOIN users u ON ga.user_id = u.id
                WHERE 1=1
            """

            params = []

            if start_date:
                query += " AND ga.date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND ga.date <= %s"
                params.append(end_date)
            
            if search_term:
                query += " AND (u.name LIKE %s OR u.id_number = %s)"
                params.append(f"%{search_term}%")
                params.append(search_term)
            
            if status and status != "All":
                query += " AND ga.status = %s"
                params.append(status)

            query += " ORDER BY ga.date DESC, ga.time DESC"

            cursor.execute(query, params)
            access_records = cursor.fetchall()

            conn.close()
            return access_records

        except Error as e:
            print(f"Error fetching filtered gate access records: {e}")
            return []
