# user_reg
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

# user_registration.py에 정의된 클래스를 import
from user_registration import MemberRegistrationWindow
# 새로 만들 user_Edit_delete_Management.py 파일에서 클래스를 가져옵니다.
from user_Edit_Delete_Management import UserDetailWindow
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
        sql = "SELECT id_num, name, TO_CHAR(birthday, 'YYYY-MM-DD'), gender, tel_num, email, Del_date FROM user_reg ORDER BY name"
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
            SELECT id_num, name, TO_CHAR(birthday, 'YYYY-MM-DD'), gender, tel_num, email, Del_date
            FROM user_reg 
            WHERE (name LIKE :1 OR tel_num LIKE :2)
            ORDER BY name
        """
        # :1과 :2에 각각 동일한 값을 바인딩합니다.
        cur.execute(sql, (search_term, search_term))
        rows = cur.fetchall()
        cur.close()
        return rows

    def fetch_user_by_id(self, user_id):
        """ID로 특정 회원 정보를 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        # 이미지 경로를 포함한 모든 컬럼을 가져옵니다.
        sql = "SELECT name, TO_CHAR(birthday, 'YYYY-MM-DD'), gender, tel_num, email, image_path FROM user_reg WHERE id_num = :1"
        cur.execute(sql, (user_id,))
        row = cur.fetchone() # 단일 행을 가져옵니다.
        cur.close()
        return row          

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


    def update_user(self, data, user_id):
        """회원 정보를 업데이트합니다."""
        conn = self.connect()
        cur = conn.cursor()
        sql = """
            UPDATE user_reg
            SET name = :1,
                birthday = TO_DATE(:2, 'YYYY-MM-DD'),
                gender = :3,
                tel_num = :4,
                email = :5,
                image_path = :6
            WHERE id_num = :7
        """
        cur.execute(sql, data + (user_id,))
        conn.commit()
        cur.close()
    
    def has_active_loans(self, user_id):
        """회원의 미반납 도서 여부를 확인합니다. 미반납 도서가 있으면 True를 반환합니다."""
        conn = self.connect()
        cur = conn.cursor()
        sql = """
            SELECT COUNT(*) FROM Rent_Management
            WHERE id_num = :user_id AND Return_date IS NULL
        """
        cur.execute(sql, user_id=user_id)
        loan_count = cur.fetchone()[0]
        cur.close()
        return loan_count > 0

    def soft_delete_user(self, user_id):
        """회원 정보를 논리적으로 삭제합니다 (Del_date 업데이트)."""
        conn = self.connect()
        cur = conn.cursor()
        sql = "UPDATE User_reg SET Del_date = SYSDATE WHERE id_num = :user_id"
        cur.execute(sql, user_id=user_id)
        conn.commit()
        cur.close()

#------------------------------------------------------------------------------------------------
    def fetch_loans_by_user(self, user_id):#user_edit delete management.py 대출정보
        """특정 회원의 대출 정보를 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        # RENTAL 테이블과 BOOK_INFO 테이블을 조인하여 대출 정보를 가져옵니다.
        # 테이블과 컬럼 이름은 실제 DB 스키마에 맞게 조정해야 합니다.
        sql = """
            SELECT b.Title, TO_CHAR(r.Start_date, 'YYYY-MM-DD'), b.Isbn
            FROM Rent_Management r
            JOIN Book_info b ON r.Tracking_num = b.Tracking_num
            JOIN User_reg c ON r.id_num = c.id_num
            WHERE r.id_num = :user_id
            AND r.Return_date IS NULL
            AND b.Del_date IS NULL
            AND c.Del_date IS NULL
            ORDER BY r.Start_date DESC
        """
        cur.execute(sql, user_id=user_id)
        rows = cur.fetchall()
        cur.close()
        return rows
#------------------------------------------------------------------------------------------------
    def fetch_past_loans_by_user(self, user_id):#회원의 과거 내역
        """특정 회원의 과거 대출 내역을 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        sql = """
            SELECT b.Title, TO_CHAR(r.Start_date, 'YYYY-MM-DD'), TO_CHAR(r.Return_date, 'YYYY-MM-DD')
            FROM Rent_Management r
            JOIN Book_info b ON r.Tracking_num = b.Tracking_num
            JOIN User_reg c ON r.id_num = c.id_num
            WHERE r.id_num = :user_id
            AND r.Return_date IS NOT NULL
            AND c.Del_date IS NULL
            ORDER BY r.Return_date DESC
        """
        cur.execute(sql, user_id=user_id)
        rows = cur.fetchall()
        cur.close()
        return rows

    def fetch_all_current_loans_for_user(self, user_id):
        """특정 회원의 모든 대출중인 도서 정보를 반납을 위해 가져옵니다."""
        conn = self.connect()
        cur = conn.cursor()
        sql = """
            SELECT b.Title, b.Isbn, TO_CHAR(r.Start_date, 'YYYY-MM-DD'), TO_CHAR(r.End_date, 'YYYY-MM-DD'),
                   CASE WHEN SYSDATE > r.End_date THEN TRUNC(SYSDATE - r.End_date) ELSE 0 END as Overdue_Days,
                   r.rent_num
            FROM Rent_Management r
            JOIN Book_info b ON r.Tracking_num = b.Tracking_num
            WHERE r.id_num = :user_id
            AND r.Return_date IS NULL
            AND b.Del_date IS NULL
            ORDER BY r.Start_date
        """
        cur.execute(sql, user_id=user_id)
        rows = cur.fetchall()
        cur.close()
        return rows

    def process_bulk_return(self, rent_nums):
        """여러 도서를 한 번에 반납 처리합니다."""
        conn = self.connect()
        cur = conn.cursor()
        # executemany를 사용하기 위해 데이터를 (rent_num,) 형태의 튜플 리스트로 변환합니다.
        data_to_update = [(num,) for num in rent_nums]
        
        sql = "UPDATE Rent_Management SET Return_date = SYSDATE WHERE rent_num = :1"
        
        # executemany는 여러 데이터 행에 대해 동일한 SQL 문을 실행합니다.
        cur.executemany(sql, data_to_update)
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
        ttk.Button(tab_frame, text="도서관리", command=self.switch_to_book_management).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tab_frame, text="회원관리", style="Gray.TButton").pack(side=tk.LEFT)
        ttk.Button(tab_frame, text="회원등록", command=self.open_registration_window).pack(side=tk.RIGHT)

        # 회원 목록 테이블 (컬럼 예시)
        columns = ("이름", "생년월일", "성별", "전화번호", "이메일","정보")
        self.user_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.user_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # 각 컬럼의 너비를 설정하여 가로 스크롤이 생기지 않도록 합니다.
        col_widths = {
            "이름": 80,
            "생년월일": 180,
            "성별": 100,
            "전화번호": 100,
            "이메일": 120,
            "정보": 100
        }

        for col, width in col_widths.items():
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, width=width, anchor=tk.CENTER)

        # 탈퇴한 회원을 위한 스타일 태그를 설정합니다.
        self.user_tree.tag_configure('deleted_user', foreground='gray')

        # Treeview에 마우스 클릭 이벤트를 연결합니다.
        self.user_tree.bind("<Button-1>", self.on_tree_click)

        # Treeview에 마우스 움직임 이벤트를 연결하여 커서 모양을 변경합니다.
        self.user_tree.bind("<Motion>", self.on_tree_motion)

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
                user_id = user[0] # id_num
                del_date = user[6] # Del_date
                display_values = list(user[1:6]) # name, birthday, gender, tel_num, email
                # '정보' 칸에 '정보 보기' 텍스트를 추가하고, 위에서 설정한 태그를 적용합니다.
                values_with_button = display_values + ["정보"]
                if del_date is not None: # 탈퇴한 회원이면
                    self.user_tree.insert('', tk.END, iid=user_id, values=values_with_button, tags=('deleted_user',))
                else: # 활성 회원이면
                    self.user_tree.insert('', tk.END, iid=user_id, values=values_with_button)
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
        

    def on_tree_click(self, event):
        """Treeview 클릭 이벤트를 처리하여 '정보 보기' 버튼 클릭을 감지합니다."""
        region = self.user_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.user_tree.identify_column(event.x)
            # 마지막 컬럼('#6')이 '정보' 컬럼입니다.
            if column == '#6':
                user_id = self.user_tree.identify_row(event.y)
                if user_id: # 클릭된 행이 있는지 확인
                    # 클릭된 행의 태그를 가져옵니다.
                    tags = self.user_tree.item(user_id, 'tags')
                    # 'deleted_user' 태그가 있으면 아무 동작도 하지 않습니다.
                    if 'deleted_user' in tags:
                        return
                    self.open_user_detail_window(user_id)

    def open_user_detail_window(self, user_id):
        """회원 상세 정보 창을 엽니다."""
        detail_window = tk.Toplevel(self.root)
        UserDetailWindow(detail_window, self.db, user_id)
        self.root.wait_window(detail_window)
        self.load_user_data() # 상세 정보 창이 닫히면 목록을 새로고침합니다.
        
    def on_tree_motion(self, event):
        """마우스 움직임에 따라 '정보' 컬럼 위에서 커서를 변경합니다."""
        column = self.user_tree.identify_column(event.x)
        # 마지막 컬럼('#6') 위일 때만 커서를 손가락 모양으로 변경
        if column == '#6':
            user_id = self.user_tree.identify_row(event.y)
            if user_id:
                tags = self.user_tree.item(user_id, 'tags')
                # 탈퇴한 회원이 아닐 때만 커서를 변경합니다.
                if 'deleted_user' not in tags:
                    self.user_tree.config(cursor="hand2")
                else:
                    self.user_tree.config(cursor="")
        else:
            self.user_tree.config(cursor="")

    def switch_to_book_management(self):
        """도서 관리 창으로 전환합니다."""
        self.root.destroy() # 현재 창을 닫습니다.

        # 순환 참조 오류를 피하기 위해 함수 내에서 import 합니다.
        import book_mainpage

        # 새로운 tkinter 루트 창과 앱을 생성하여 실행합니다.
        new_root = tk.Tk()
        book_mainpage.BookManagerApp(new_root)
        new_root.mainloop()


# -----------------------------
# 실행부
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerApp(root)
    root.mainloop()