import sqlite3
import datetime
import os

def get_db_connection() -> sqlite3.Connection:
    """
    建立並回傳 SQLite 資料庫連線。
    如果 bokelai.db 不存在，會自動建立並初始化 books 資料表。
    """
    try:
        db_file = 'bokelai.db'
        db_exists = os.path.exists(db_file)

        conn = sqlite3.connect(db_file) # 建立連線
        conn.row_factory = sqlite3.Row  # 設定 row_factory 回傳字典形式的列

        if not db_exists:# 沒有資料庫檔案，則建立資料表
            # 初始化資料表
            create_table_sql = """
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT,
                price INTEGER NOT NULL,         
                publish_date TEXT,                
                isbn TEXT,
                cover_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """       # 建立資料表的 SQL 指令
             
            conn.execute(create_table_sql) # 執行建立資料表的 SQL
            conn.commit() # 提交變更
        

        return conn

    except Exception as e:
        print(f"資料庫連線錯誤：{e}")
        return None


        
    

def get_all_books(skip: int, limit: int) -> list[dict]:
    """
    取得所有書籍，支援分頁功能。
    參數: skip - 跳過的書籍數量
          limit - 回傳的書籍數量上限    
    """
    conn = get_db_connection() # 取得連線
    if conn is None: # 防呆
        return []
        
    try:
        cursor = conn.cursor() # 建立 cursor
        cursor.execute('SELECT * FROM books LIMIT ? OFFSET ?', (limit, skip)) # 執行查詢
        rows = cursor.fetchall()# 取得所有結果
        
        # 因為在 get_db_connection 設定了 row_factory = sqlite3.Row
        # 所以直接轉 dict，不用 zip 欄位名稱
        books = [dict(row) for row in rows] 
        return books
        
    except Exception as e:
        print(f"查詢錯誤：{e}")
        return []
        
    finally:
        conn.close() # 2. 確保一定會關閉連線
   
    
def get_book_by_id(book_id: int) -> dict | None:
    """
    根據書籍 ID 取得單一書籍資料。
    """
    conn = get_db_connection()  # 取得連線
    if conn is None: # 防呆
        return None
    
    try:
        cursor = conn.cursor() # 建立 cursor
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,)) # 執行查詢
        row = cursor.fetchone() # 取得單一結果
        
        if row: 
            # 因為 row_factory = sqlite3.Row，直接用 dict() 轉換
            return dict(row)
        else:
            return None

    except Exception as e:
        print(f"查詢書籍時發生錯誤：{e}")
        return None
        
    finally:
        # 關閉連線
        conn.close()


def create_book(title: str, author: str, publisher: str | None, price: int, 
                publish_date: str | None, isbn: str | None, cover_url: str | None) -> int:
    """
    新增一本書籍到資料庫，並回傳新書籍的 ID。
    """
    conn = get_db_connection() # 取得連線
    if conn is None: # 防呆
        return -1

    try:
        cursor = conn.cursor() # 建立 cursor
        cursor.execute("""  
            INSERT INTO books (title, author, publisher, price, publish_date, isbn, cover_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, author, publisher, price, publish_date, isbn, cover_url)) # 執行插入
        
        conn.commit() # 提交變更
        return cursor.lastrowid  # 回傳新插入的 ID
        
    except Exception as e:
        print(f"新增書籍時發生錯誤：{e}")
        return -1
        
    finally:
        conn.close() # 關閉連線


def update_book(book_id: int, title: str, author: str, publisher: str | None, 
                price: int, publish_date: str | None, isbn: str | None, cover_url: str | None) -> bool:
    """
    更新指定 ID 的書籍資料。
    """
    conn = get_db_connection() # 取得連線
    if conn is None: # 防呆 
        return False

    try:
        cursor = conn.cursor() # 建立 cursor
        cursor.execute("""
            UPDATE books 
            SET title = ?, author = ?, publisher = ?, price = ?, 
                publish_date = ?, isbn = ?, cover_url = ? 
            WHERE id = ?
        """, (title, author, publisher, price, publish_date, isbn, cover_url, book_id)) # 執行更新
        
        conn.commit() # 提交變更
        
        if cursor.rowcount > 0: # 有更新到資料
            return True
        else: # 沒有更新到資料 (ID不存在）
            return False
            
    except Exception as e:
        print(f"更新書籍時發生錯誤：{e}")
        return False
        
    finally:
        conn.close()# 關閉連線


def delete_book(book_id: int) -> bool:
    """
    刪除指定 ID 的書籍。
    """
    conn = get_db_connection()  # 取得連線
    if conn is None: # 防呆
        return False

    try:
        cursor = conn.cursor() # 建立 cursor
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,)) # 執行刪除
        
        conn.commit() # 提交變更
        
        if cursor.rowcount > 0: # 有刪除資料
            return True
        else:
            return False
            
    except Exception as e:
        print(f"刪除書籍時發生錯誤：{e}")
        return False
        
    finally:
        conn.close() # 關閉連線