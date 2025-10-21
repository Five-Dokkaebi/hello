import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

# book_registration.py에 정의된 클래스를 import (파일이 존재한다고 가정)
from book_registration import BookRegistrationWindow
import oracledb

# -----------------------------
# 오라클 DB 연결 및 쿼리용 클래스
# -----------------------------
class OracleDB:
    def __init__(self):
        # DB 정보
        self.dbUser = "fusers"
        self.dbPW   = "skyfive"
        self.dbHost = "deu.duraka.shop"
        self.dbPort = 4265
        self.dbSID  = "xe"
        self.conn   = None

    def connect(self):
        """데이터베이스에 연결합니다."""
        if self.conn is None:
            dsn = oracledb.makedsn(self.dbHost, self.dbPort, sid=self.dbSID)
            self.conn = oracledb.connect(user=self.dbUser, password=self.dbPW, dsn=dsn)
        return self.conn

    def fetch_all_books(self):
        """데이터베이스에서 모든 도서 정보를 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        sql = "SELECT Tracking_num, Title, Author, Publisher, ISBN FROM Books_Info ORDER BY Title"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def search_books_by_keyword(self, keyword):
        """키워드로 제목 또는 저자를 검색하여 도서 정보를 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        search_term = f'%{keyword}%'
        sql = """
            SELECT Tracking_num, Title, Author, Publisher, ISBN
            FROM Books_Info 
            WHERE Title LIKE :1 OR Author LIKE :2
            ORDER BY Title
        """
        cur.execute(sql, (search_term, search_term))
        rows = cur.fetchall()
        cur.close()
        return rows

    def insert_book(self, data):
        """새로운 도서 정보를 데이터베이스에 추가합니다."""
        conn = self.connect()
        cur = conn.cursor()
        # Tracking_num은 시퀀스(예: BOOKS_INFO_SEQ.NEXTVAL)로, Db_date는 SYSDATE로 처리한다고 가정합니다.
        sql = """
            INSERT INTO Books_Info (Tracking_num, ISBN, Title, Author, Publisher, Price, Link, Image_path, Info, Db_date)
            VALUES (BOOKS_INFO_SEQ.NEXTVAL, :1, :2, :3, :4, :5, :6, :7, :8, SYSDATE)
        """
        cur.execute(sql, data)
        conn.commit()
        cur.close()    

# -----------------------------
# 메인 GUI
# -----------------------------
class BookManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("도서 관리 프로그램")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        style = ttk.Style()
        style.configure(
            "Gray.TButton",
            background="#696969",
            foreground="black",
            padding=5
        )

        # DB 클래스 인스턴스 생성
        self.db = OracleDB()

        self.create_main_ui()

    def create_main_ui(self):
        title_font = Font(family="Arial", size=18, weight="bold")
        ttk.Label(self.root, text="도서 관리 프로그램", font=title_font).pack(pady=10)

        # 검색 영역
        search_frame = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        search_frame.pack(fill=tk.X)
        ttk.Label(search_frame, text="제목 또는 저자를 입력하십시오:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        ttk.Button(search_frame, text="검색", command=self.search_books).pack(side=tk.LEFT)

        # 버튼 프레임
        tab_frame = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        tab_frame.pack(fill=tk.X)
        ttk.Button(tab_frame, text="도서관리", style="Gray.TButton").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tab_frame, text="회원관리").pack(side=tk.LEFT)
        ttk.Button(tab_frame, text="도서등록", command=self.open_book_registration_window).pack(side=tk.RIGHT)

        # 도서 목록 테이블
        columns = ("관리번호", "제목", "저자", "출판사", "ISBN", "정보")
        self.book_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.book_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 각 컬럼의 너비를 설정하여 가로 스크롤이 생기지 않도록 합니다.
        col_widths = {
            "관리번호": 80,
            "제목": 180,
            "저자": 100,
            "출판사": 100,
            "ISBN": 120,
            "정보": 100
        }

        for col, width in col_widths.items():
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=width, anchor=tk.CENTER)

        # 프로그램 시작 시 도서 목록을 불러옵니다.
        self.load_book_data()

    def load_book_data(self, keyword=None):
        """DB에서 도서 정보를 가져와 테이블에 표시합니다. 키워드가 있으면 필터링합니다."""
        # 기존 테이블의 모든 항목을 삭제합니다.
        for item in self.book_tree.get_children():
            self.book_tree.delete(item)
        
        try:
            # 키워드가 있는지 여부에 따라 다른 DB 메서드를 호출합니다.
            if keyword:
                book_list = self.db.search_books_by_keyword(keyword)
            else:
                book_list = self.db.fetch_all_books()

            for book in book_list:
                self.book_tree.insert('', tk.END, values=book)
        except Exception as e:
            messagebox.showerror("DB 오류", f"도서 목록을 불러오는 데 실패했습니다: {e}")

    def search_books(self):
        """검색창의 키워드로 도서 목록을 필터링합니다."""
        keyword = self.search_entry.get().strip()
        self.load_book_data(keyword if keyword else None)

    def open_book_registration_window(self):
        """도서등록 창을 엽니다."""
        register_window = tk.Toplevel(self.root)
        # BookRegistrationWindow 클래스가 DB 객체를 인자로 받는다고 가정합니다.
        BookRegistrationWindow(register_window, self.db)
        self.root.wait_window(register_window)  # 등록 창이 닫힐 때까지 기다립니다.
        self.load_book_data()  # 창이 닫히면 데이터를 새로고침합니다.

# -----------------------------
# 실행부
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerApp(root)
    root.mainloop()

