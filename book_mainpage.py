import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

# book_registration.py에 정의된 클래스를 import 
from book_registration import BookRegistrationWindow
from book_loan_management import BookLoanWindow
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
        sql = "SELECT Tracking_num, Title, Author, Publisher, Isbn FROM Book_Info ORDER BY Title"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def search_books_by_keyword(self, keyword):
        """키워드로 제목 또는 저자를 검색하여 도서 정보를 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        search_term = f'%{keyword}%'
        # :1, :2 대신 :keyword 라는 '이름'을 가진 바인드 변수를 사용합니다.
        sql = """
            SELECT Tracking_num, Title, Author, Publisher, Isbn
            FROM Book_Info 
            WHERE Title LIKE :keyword OR Author LIKE :keyword
            ORDER BY Title
        """
        # 이름이 같은 바인드 변수에는 값을 한 번만 전달할 수 있습니다.
        cur.execute(sql, keyword=search_term)
        rows = cur.fetchall()
        cur.close()
        return rows

    def insert_book(self, data):
        """새로운 도서 정보를 데이터베이스에 추가합니다."""
        conn = self.connect()
        cur = conn.cursor()
        # Db_date는 SYSDATE로 처리한다고 가정합니다.
        sql = """ 
            INSERT INTO Book_Info (Isbn, Title, Author, Publisher, Price, Link, Image_path, Info, Db_date)
            VALUES (:1, :2, :3, :4, :5, :6, :7, :8, SYSDATE)
        """
        cur.execute(sql, data)
        conn.commit()
        cur.close()
#-----------------------------------------------------------------------------------------------------------
    def fetch_book_by_tracking_num(self, tracking_num):
        """관리번호(Tracking_num)로 특정 도서 정보를 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        # 이미지 경로, 책 설명(Info) 등 상세 정보 포함
        sql = "SELECT Title, Author, Publisher, Info, Image_path, Isbn FROM Book_Info WHERE Tracking_num = :1"
        cur.execute(sql, (tracking_num,))
        row = cur.fetchone()
        cur.close()
        return row

    def fetch_users_by_book_loan(self, tracking_num):
        """특정 도서를 대출 중인 회원 목록을 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        # Rent_Management, User_reg 테이블 조인. Return_date가 NULL인 경우만 대출 중으로 간주.
        sql = """
            SELECT c.NAME, c.TEL_NUM, TO_CHAR(r.Start_date, 'YYYY-MM-DD'), TO_CHAR(r.Start_date + 14, 'YYYY-MM-DD')
            FROM Rent_Management r
            JOIN User_reg c ON r.id_num = c.id_num
            WHERE r.Tracking_num = :1 AND r.Return_date IS NULL AND c.Del_date IS NULL
            ORDER BY r.Start_date
        """
        cur.execute(sql, (tracking_num,))
        rows = cur.fetchall()
        cur.close()
        return rows   

#----------------------------------------------------------------------------------------------------------- 

    def search_users_for_loan(self, keyword):
        """키워드로 회원 이름 또는 회원번호를 검색합니다."""
        conn = self.connect()
        cur = conn.cursor()
        search_term = f'%{keyword}%'
        # :1 대신 :keyword 라는 '이름'을 가진 바인드 변수를 사용합니다.
        sql = """
            SELECT id_num, name
            FROM User_reg
            WHERE (name LIKE :keyword OR TO_CHAR(id_num) LIKE :keyword) AND Del_date IS NULL
            ORDER BY name
        """
        # 이름이 같은 바인드 변수에는 값을 한 번만 전달할 수 있습니다.
        cur.execute(sql, keyword=search_term)
        rows = cur.fetchall()
        cur.close()
        return rows

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

        # Treeview에 마우스 클릭 및 움직임 이벤트를 연결합니다.
        self.book_tree.bind("<Button-1>", self.on_book_tree_click)
        self.book_tree.bind("<Motion>", self.on_book_tree_motion)

        # 프로그램 시작 시 도서 목록을 불러옵니다.
        self.load_book_data()

    def load_book_data(self, keyword=None):#키워드 입력되면 호출됨
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
                values_with_button = list(book) + ["정보"]
                self.book_tree.insert('', tk.END, values=values_with_button)
        except Exception as e:
            messagebox.showerror("DB 오류", f"도서 목록을 불러오는 데 실패했습니다: {e}")

    def search_books(self):
        """검색창의 키워드로 도서 목록을 필터링합니다."""
        keyword = self.search_entry.get().strip()#사용자가 검색창에 입력한 텍스트를 가져와 (깨끗하게 한 뒤에) 변수에 넣음
        self.load_book_data(keyword if keyword else None) #키워드가 입력됬는지 안됬는지

    def open_book_registration_window(self):
        """도서등록 창을 엽니다."""
        register_window = tk.Toplevel(self.root)
        # BookRegistrationWindow 클래스가 DB 객체를 인자로 받는다고 가정합니다.
        BookRegistrationWindow(register_window, self.db)
        self.root.wait_window(register_window)  # 등록 창이 닫힐 때까지 기다립니다.
        self.load_book_data()  # 창이 닫히면 데이터를 새로고침합니다.

    def on_book_tree_click(self, event):
        """Treeview 클릭 이벤트를 처리하여 '정보' 버튼 클릭을 감지합니다."""
        region = self.book_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.book_tree.identify_column(event.x)
            # 마지막 컬럼('#6')이 '정보' 컬럼입니다.
            if column == '#6':
                item_id = self.book_tree.identify_row(event.y)
                item_values = self.book_tree.item(item_id, 'values')
                tracking_num = item_values[0]  # 관리번호는 첫 번째 값 (인덱스 0)
                self.open_book_detail_window(tracking_num)

    def open_book_detail_window(self, tracking_num):
        """도서 상세 정보 창을 엽니다."""
        detail_window = tk.Toplevel(self.root)
        BookLoanWindow(detail_window, self.db, tracking_num)
        self.root.wait_window(detail_window)
        self.load_book_data() # 상세 정보 창이 닫히면 목록을 새로고침합니다.

    def on_book_tree_motion(self, event):
        """마우스 움직임에 따라 '정보' 컬럼 위에서 커서를 변경합니다."""
        column = self.book_tree.identify_column(event.x)
        if column == '#6':
            self.book_tree.config(cursor="hand2")
        else:
            self.book_tree.config(cursor="")

# -----------------------------
# 실행부
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerApp(root)
    root.mainloop()

