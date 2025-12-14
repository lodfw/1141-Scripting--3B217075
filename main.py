from fastapi import FastAPI, HTTPException, status
from typing import List
import database
import models

app = FastAPI()

@app.get("/")
def root():
    """
    API 根路徑，確認服務是否運作。
    """
    return {"message": "AI Books API"} # 回傳簡單訊息確認服務運作

@app.get("/books", response_model=List[models.BookResponse]) # 指定回傳型別為書籍列表
def get_books(skip: int = 0, limit: int = 0):
    """
    取得書籍列表，支援分頁 (skip, limit)。
    """
    books = database.get_all_books(skip, limit) # 從資料庫取得書籍列表
    return books # 回傳書籍列表

@app.get("/books/{book_id}", response_model=models.BookResponse) # 指定回傳型別為單一書籍
def get_book(book_id: int):
    """
    根據 ID 取得特定書籍詳情。
    若找不到書籍，回傳 404。
    """
    book = database.get_book_by_id(book_id) # 從資料庫取得書籍
    if not book: # 找不到書籍
        raise HTTPException(status_code=404, detail="Book not found") # 回傳 404 錯誤
    return book # 回傳書籍詳情 

@app.post("/books", response_model=models.BookResponse, status_code=201) # 指定回傳型別為單一書籍，並設定狀態碼為 201 Created
def create_book(book: models.BookCreate):
    """
    新增一本書籍。
    成功回傳 201 Created。
    """
    # 呼叫資料庫函式新增書籍
    new_id = database.create_book(
        book.title, book.author, book.publisher,
        book.price, book.publish_date, book.isbn, book.cover_url
    )
    # 檢查是否成功新增
    if new_id == -1:# 假設 -1 代表新增失敗
        raise HTTPException(status_code=400, detail="Create book failed. Check required fields.")

    new_book = database.get_book_by_id(new_id)
    return new_book

@app.put("/books/{book_id}", response_model=models.BookResponse)# 指定回傳型別為單一書籍
def update_book(book_id: int, book: models.BookCreate):
    """
    更新書籍資料。
    若 ID 不存在，回傳 404。
    """
    # 呼叫資料庫函式更新書籍
    success = database.update_book(
        book_id, book.title, book.author, book.publisher,
        book.price, book.publish_date, book.isbn, book.cover_url
    )
    # 檢查是否成功更新
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    # 取得更新後的書籍資料並回傳
    updated_book = database.get_book_by_id(book_id)
    return updated_book

@app.delete("/books/{book_id}", status_code=204) # 設定狀態碼為 204 No Content
def delete_book(book_id: int):
    """
    刪除書籍。
    成功回傳 204 No Content (無 Response Body)。
    若 ID 不存在，回傳 404。
    """
    # 呼叫資料庫函式刪除書籍
    success = database.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None