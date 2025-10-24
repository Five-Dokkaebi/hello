# user_reg
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

# user_registration.py에 정의된 클래스를 import
from user_registration import MemberRegistrationWindow
import oracledb

# -----------------------------
# 오라클 DB 연결용 클래스 (같은 설정 재사용)
# -----------------------------
class OracleDB:
    def __init__(self):
        # DB 정보 (필요하면 여기서 바꿔)
        self.dbUser = "fusers"
        self.dbPW   = "skyfive"
        self.dbHost = "deu.duraka.shop"
        self.dbPort = 4265
        self.dbSID  = "xe"
        self.conn   = None

        
    def connect(self):
        if self.conn is None:
            dsn = oracledb.makedsn(self.dbHost, self.dbPort, sid=self.dbSID)
            self.conn = oracledb.connect(user=self.dbUser, password=self.dbPW, dsn=dsn)
        return self.conn

    def fetch_all_users(self):
        """데이터베이스에서 모든 회원 정보를 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        # 생년월일 컬럼을 'YYYY-MM-DD' 형식의 문자열로 변환하여 선택합니다.
        sql = "SELECT name, TO_CHAR(birthday, 'YYYY-MM-DD'), gender, tel_num, email FROM user_reg ORDER BY name"
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    def search_users_by_keyword(self, keyword):
        """키워드로 이름 또는 전화번호를 검색하여 회원 정보를 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        # '%'를 사용하여 부분 일치 검색을 수행합니다.
        search_term = f'%{keyword}%'
        sql = """
            SELECT name, TO_CHAR(birthday, 'YYYY-MM-DD'), gender, tel_num, email 
            FROM user_reg 
            WHERE name LIKE :1 OR tel_num LIKE :2
            ORDER BY name
        """
        # :1과 :2에 각각 동일한 값을 바인딩합니다.
        cur.execute(sql, (search_term, search_term))
        rows = cur.fetchall()
        cur.close()
        return rows        

    def insert_user_reg(self, data):
        conn = self.connect()
        cur = conn.cursor()
        sql = """
            INSERT INTO user_reg (name, birthday, gender, tel_num, email, image_path)
            VALUES (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3, :4, :5, :6)
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
        self.root.title("회원 관리 프로그램")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)

        style = ttk.Style()
        style.configure(
            "Gray.TButton",
            background= "#696969",   # 회색
            foreground="black",    # 글자색
            padding=5
        )

        # DB 클래스 인스턴스 생성
        self.db = OracleDB()

        self.create_main_ui()

    def create_main_ui(self):
        title_font = Font(family="Arial", size=18, weight="bold")
        ttk.Label(self.root, text="회원 관리 프로그램", font=title_font).pack(pady=10)

        # 검색 영역
        search_frame = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        search_frame.pack(fill=tk.X)
        ttk.Label(search_frame, text="이름 또는 ID를 입력하십시오:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, width=50)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        ttk.Button(search_frame, text="검색", command=self.search_users).pack(side=tk.LEFT)

        # 버튼 프레임
        tab_frame = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        tab_frame.pack(fill=tk.X)
        ttk.Button(tab_frame, text="회원관리", style="Gray.TButton").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tab_frame, text="도서관리").pack(side=tk.LEFT)
        ttk.Button(tab_frame, text="회원등록", command=self.open_registration_window).pack(side=tk.RIGHT)

        # 회원 목록 테이블 (컬럼 예시)
        columns = ("이름", "생년월일", "성별", "전화번호", "이메일")
        self.user_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.user_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        for col in columns:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=150, anchor=tk.CENTER)

        # 프로그램 시작 시 회원 목록을 불러옵니다.
        self.load_user_data()
        

    def load_user_data(self, keyword=None):
        """DB에서 회원 정보를 가져와 테이블에 표시합니다. 키워드가 있으면 필터링합니다."""
        # 기존 테이블의 모든 항목을 삭제합니다.
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)
        
        try:
            # 키워드가 있는지 여부에 따라 다른 DB 메서드를 호출합니다.
            if keyword:
                user_list = self.db.search_users_by_keyword(keyword)
            else:
                user_list = self.db.fetch_all_users()

            for user in user_list:
                self.user_tree.insert('', tk.END, values=user)
        except Exception as e:
            messagebox.showerror("DB 오류", f"회원 목록을 불러오는 데 실패했습니다: {e}")

    def search_users(self):
        """검색창의 키워드로 회원 목록을 필터링합니다."""
        keyword = self.search_entry.get().strip()
        self.load_user_data(keyword if keyword else None)           
           

    # 회원등록 창으로 연결
    def open_registration_window(self):
        register_window = tk.Toplevel(self.root)
        # db 객체(연결정보)를 재사용해서 팝업으로 넘김
        MemberRegistrationWindow(register_window, self.db)
        self.root.wait_window(register_window) # 등록 창이 닫힐 때까지 기다립니다.
        self.load_user_data() # 창이 닫히면 데이터를 새로고침합니다.


# -----------------------------
# 실행부
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerApp(root)
    root.mainloop()