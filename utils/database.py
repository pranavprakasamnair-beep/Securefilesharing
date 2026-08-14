from flask_mysqldb import MySQL

mysql = MySQL()

class Database:
    @staticmethod
    def init_app(app):
        mysql.init_app(app)
    
    @staticmethod
    def get_user_by_username(username):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id, username, email, password_hash FROM users WHERE username = %s",
            (username,)
        )
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        # If DictCursor is working
        if isinstance(row, dict):
            return row

        # If MySQL returned a tuple
        return {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'password_hash': row[3]
        }
    
    @staticmethod
    def get_user_by_email(email):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id, username, email, password_hash FROM users WHERE email = %s",
            (email,)
        )
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        # If DictCursor is working
        if isinstance(row, dict):
            return row

        # If MySQL returned a tuple
        return {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'password_hash': row[3]
        }

    @staticmethod
    def get_user_by_id(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id, username, email, password_hash FROM users WHERE id = %s",
            (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()

        if row is None:
            return None

        # If DictCursor is working
        if isinstance(row, dict):
            return row

        # If MySQL returned a tuple
        return {
            'id': row[0],
            'username': row[1],
            'email': row[2],
            'password_hash': row[3]
        }

    @staticmethod
    def create_user(username, email, password_hash):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, password_hash)
        )
        mysql.connection.commit()
        user_id = cursor.lastrowid
        cursor.close()
        return user_id
    
    @staticmethod
    def save_file_metadata(filename, original_filename, file_hash, encryption_key, owner_id, file_size):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO files (filename, original_filename, file_hash, encryption_key, owner_id, file_size)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (filename, original_filename, file_hash, encryption_key.decode(), owner_id, file_size)
        )
        mysql.connection.commit()
        file_id = cursor.lastrowid
        cursor.close()
        return file_id
    
    @staticmethod
    def get_user_files(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM files WHERE owner_id = %s ORDER BY upload_date DESC", (user_id,))
        files = cursor.fetchall()
        cursor.close()
        return files
    
    @staticmethod
    def get_file_by_id(file_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM files WHERE id = %s", (file_id,))
        file = cursor.fetchone()
        cursor.close()
        return file
    
    @staticmethod
    def share_file(file_id, shared_with_user_id, shared_by_user_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO shared_files (file_id, shared_with_user_id, shared_by_user_id)
               VALUES (%s, %s, %s)""",
            (file_id, shared_with_user_id, shared_by_user_id)
        )
        mysql.connection.commit()
        cursor.close()
    
    @staticmethod
    def get_shared_files(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT f.*, u.username as owner_username, sf.shared_date
               FROM files f
               JOIN shared_files sf ON f.id = sf.file_id
               JOIN users u ON f.owner_id = u.id
               WHERE sf.shared_with_user_id = %s
               ORDER BY sf.shared_date DESC""",
            (user_id,)
        )
        files = cursor.fetchall()
        cursor.close()
        return files
    
    @staticmethod
    def log_file_access(file_id, user_id, access_type, ip_address):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO file_access_logs (file_id, user_id, access_type, ip_address)
               VALUES (%s, %s, %s, %s)""",
            (file_id, user_id, access_type, ip_address)
        )
        mysql.connection.commit()
        cursor.close()
    
    @staticmethod
    def delete_file(file_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM files WHERE id = %s", (file_id,))
        mysql.connection.commit()
        cursor.close()
    
    @staticmethod
    def check_file_access(file_id, user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM files WHERE id = %s AND owner_id = %s", (file_id, user_id))
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.execute("SELECT id FROM shared_files WHERE file_id = %s AND shared_with_user_id = %s", (file_id, user_id))
        result = cursor.fetchone()
        cursor.close()
        return result is not None