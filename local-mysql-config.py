import mysql.connector
from mysql.connector import Error
import os

def setup_local_mysql():
    """配置本地MySQL连接"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='root',
            password='rootpassword'  # 替换为你的MySQL root密码
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # 创建数据库
            cursor.execute("CREATE DATABASE IF NOT EXISTS ai_platform")
            cursor.execute("USE ai_platform")
            
            # 创建表
            tables_sql = [
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    title VARCHAR(200),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    session_id INT,
                    role ENUM('user', 'assistant', 'system'),
                    content TEXT,
                    tokens_used INT,
                    model_used VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES chat_sessions(id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS projects (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    name VARCHAR(100),
                    description TEXT,
                    git_repo_url VARCHAR(200),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS code_snippets (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    project_id INT,
                    prompt TEXT,
                    generated_code TEXT,
                    language VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (project_id) REFERENCES projects(id)
                )
                """
            ]
            
            for sql in tables_sql:
                cursor.execute(sql)
            
            # 创建应用用户
            cursor.execute("""
                CREATE USER IF NOT EXISTS 'ai_user'@'%' IDENTIFIED BY 'ai_password'
            """)
            cursor.execute("""
                GRANT ALL PRIVILEGES ON ai_platform.* TO 'ai_user'@'%'
            """)
            cursor.execute("FLUSH PRIVILEGES")
            
            print("✅ 本地MySQL数据库配置完成!")
            
    except Error as e:
        print(f"❌ 数据库配置错误: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    setup_local_mysql()