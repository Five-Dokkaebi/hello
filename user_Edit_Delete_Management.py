import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Check_In_Book import CheckInWindow
from Update_user import UserUpdateWindow

class UserDetailWindow:
    def __init__(self, master, db, user_id):
        self.master = master
        self.db = db
        self.user_id = user_id
        self.user_data = None
        self.photo_path = None
        self.preview_width = 150
        self.preview_height = 180

        self.master.title("회원 상세 정보")
        self.master.geometry("1000x500")
        self.master.resizable(False, False)
        self.master.grab_set()

        self.fetch_user_details()
        self.create_widgets()
        if self.user_data:
            self.populate_data()
            self.populate_loan_data()
        else:
            messagebox.showerror("오류", "회원 정보를 불러오는 데 실패했습니다.")
            self.master.destroy()

    def fetch_user_details(self):
        """DB에서 특정 회원의 상세 정보를 가져옵니다."""
        try:
            # user_mainpage.py의 OracleDB 클래스에 추가된 fetch_user_by_tel 메서드를 사용합니다.
            self.user_data = self.db.fetch_user_by_id(self.user_id)
        except Exception as e:
            messagebox.showerror("DB 오류", f"회원 정보를 가져오는 중 오류가 발생했습니다: {e}")
            self.user_data = None

    def create_widgets(self):
        # --- 메인 영역 (좌우 분할) ---
        main_frame = tk.Frame(self.master, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_columnconfigure(0, weight=3) # 왼쪽 영역 (회원 정보)에 더 많은 공간 할당 (60%)
        main_frame.grid_columnconfigure(1, weight=2) # 오른쪽 영역 (대출 정보) 공간 축소 (40%)
        main_frame.grid_rowconfigure(0, weight=1)

        # --- 1. 왼쪽 영역: 회원 정보 ---
        left_container = tk.Frame(main_frame)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # 회원정보 제목
        user_info_title = tk.Label(left_container, text="회원 정보", font=("Arial", 14, "bold"))
        user_info_title.pack(anchor="w", pady=(0, 5))
        separator_left = tk.Frame(left_container, height=2, bg="black")
        separator_left.pack(fill="x", pady=(0, 10))

        # 회원 정보 내용 프레임 (사진 + 상세정보)
        user_content_frame = tk.Frame(left_container)
        # 내용 프레임의 두 번째 열(정보 표시 영역)이 남은 공간을 모두 차지하도록 설정
        user_content_frame.grid_columnconfigure(1, weight=1)
        user_content_frame.pack(fill="both", expand=True)

        # 사진
        photo_frame = tk.Frame(user_content_frame)
        photo_frame.grid(row=0, column=0, sticky="n", padx=(0, 15))
        self.preview_frame = tk.Frame(photo_frame, width=self.preview_width, height=self.preview_height, bg="white", relief="solid", bd=1)
        self.preview_frame.pack()
        self.preview_frame.pack_propagate(False)
        self.photo_label = tk.Label(self.preview_frame, bg="white", text="이미지 없음")
        self.photo_label.pack(expand=True)

        # 정보 표시
        info_frame = tk.Frame(user_content_frame)
        # 정보 프레임이 할당된 셀을 가로로 꽉 채우도록 설정
        info_frame.grid(row=0, column=1, sticky="new")
        info_frame.grid_columnconfigure(1, weight=1)

        labels_info = ["이름", "생년월일", "성별", "전화번호", "이메일"]
        self.info_labels = {}

        for i, label_text in enumerate(labels_info):
            label = tk.Label(info_frame, text=label_text + ":", width=10, anchor="w", font=("맑은 고딕", 10))
            label.grid(row=i, column=0, sticky="nw", pady=7)
            
            info_label = tk.Label(info_frame, text="", wraplength=300, justify='left', anchor="w", font=("맑은 고딕", 10, "bold"))
            info_label.grid(row=i, column=1, sticky="ew", pady=7)
            self.info_labels[label_text] = info_label

        # 하단 버튼 (수정, 삭제)
        bottom_frame = tk.Frame(left_container)
        bottom_frame.pack(fill="x", side="bottom", pady=(10, 0))
        delete_btn = tk.Button(bottom_frame, text="삭제", bg="lightcoral", width=10)        
        delete_btn.pack(side="right", padx=5, pady=5)
        
        edit_btn = tk.Button(bottom_frame, text="수정", bg="lightblue", width=10, command=self.open_user_update_window)
        edit_btn.pack(side="right", padx=5, pady=5)

        # --- 2. 오른쪽 영역: 대출 정보 ---
        right_container = tk.Frame(main_frame)
        right_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # --- 2-1. 대출중인 도서 프레임 ---
        current_loan_frame = tk.Frame(right_container)
        current_loan_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        current_loan_title = tk.Label(current_loan_frame, text="대출중인 도서", font=("Arial", 14, "bold"))
        current_loan_title.pack(anchor="w", pady=(0, 5))
        separator_current = tk.Frame(current_loan_frame, height=2, bg="black")
        separator_current.pack(fill="x", pady=(0, 10))

        current_loan_columns = ("도서명", "대여일", "ISBN", "선택")
        self.current_loan_tree = ttk.Treeview(current_loan_frame, columns=current_loan_columns, show="headings", height=5)
        self.current_loan_tree.pack(fill="both", expand=True)

        # 각 컬럼의 너비를 직접 지정합니다.
        current_col_widths = {"도서명": 140, "대여일": 110, "ISBN": 150, "선택": 60}
        for col, width in current_col_widths.items():
            self.current_loan_tree.heading(col, text=col)
            self.current_loan_tree.column(col, width=width, anchor=tk.CENTER)

        # --- 2-2. 과거 대출 내역 프레임 ---
        past_loan_frame = tk.Frame(right_container)
        past_loan_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        past_loan_title = tk.Label(past_loan_frame, text="과거 대출 내역", font=("Arial", 14, "bold"))
        past_loan_title.pack(anchor="w", pady=(0, 5))
        separator_past = tk.Frame(past_loan_frame, height=2, bg="black")
        separator_past.pack(fill="x", pady=(0, 10))

        past_loan_columns = ("도서명", "대여일", "반납일")
        self.past_loan_tree = ttk.Treeview(past_loan_frame, columns=past_loan_columns, show="headings", height=5)
        self.past_loan_tree.pack(fill="both", expand=True)

        # 각 컬럼의 너비를 직접 지정합니다.
        past_col_widths = {"도서명": 160, "대여일": 130, "반납일": 130}
        for col, width in past_col_widths.items():
            self.past_loan_tree.heading(col, text=col)
            self.past_loan_tree.column(col, width=width, anchor=tk.CENTER)

        # Treeview에 마우스 클릭 및 움직임 이벤트를 연결합니다.
        self.current_loan_tree.bind("<Button-1>", self.on_loan_tree_click)
        self.current_loan_tree.bind("<Motion>", self.on_loan_tree_motion)


    def populate_data(self):
        """가져온 데이터로 위젯을 채웁니다."""
        # user_data 인덱스: 0:이름, 1:생일, 2:성별, 3:전화번호, 4:이메일, 5:이미지경로
        name, birthday, gender, tel_num, email, image_path = self.user_data

        self.info_labels["이름"].config(text=name)
        self.info_labels["생년월일"].config(text=birthday)
        self.info_labels["성별"].config(text=gender)
        self.info_labels["전화번호"].config(text=tel_num)
        self.info_labels["이메일"].config(text=email)
        
        self.photo_path = image_path
        if self.photo_path:
            try:
                img = Image.open(self.photo_path)
                img = img.resize((self.preview_width, self.preview_height), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.photo_label.config(image=img_tk, text="")
                self.photo_label.image = img_tk
            except FileNotFoundError:
                self.photo_label.config(text="이미지 없음")
                self.photo_label.image = None
            except Exception:
                self.photo_label.config(text="이미지 로드 실패")
                self.photo_label.image = None

    def populate_loan_data(self):
        """DB에서 회원의 현재 및 과거 대출 정보를 가져와 테이블에 표시합니다."""
        # --- 현재 대출 목록 채우기 ---
        try:
            current_loan_list = self.db.fetch_loans_by_user(self.user_id)
            
            for item in self.current_loan_tree.get_children():
                self.current_loan_tree.delete(item)

            for loan in current_loan_list:
                values_with_button = list(loan) + ["선택"]
                self.current_loan_tree.insert('', tk.END, values=values_with_button)
        except AttributeError:
            messagebox.showwarning("알림", "현재 대출 정보를 가져오는 DB 기능이 아직 구현되지 않았습니다.", parent=self.master)
        except Exception as e:
            messagebox.showerror("DB 오류", f"현재 대출 정보를 가져오는 중 오류가 발생했습니다: {e}", parent=self.master)

        # --- 과거 대출 목록 채우기 ---
        try:
            past_loan_list = self.db.fetch_past_loans_by_user(self.user_id)

            for item in self.past_loan_tree.get_children():
                self.past_loan_tree.delete(item)

            for loan in past_loan_list:
                self.past_loan_tree.insert('', tk.END, values=loan)
        except AttributeError:
            messagebox.showwarning("알림", "과거 대출 정보를 가져오는 DB 기능이 아직 구현되지 않았습니다.", parent=self.master)
        except Exception as e:
            messagebox.showerror("DB 오류", f"과거 대출 정보를 가져오는 중 오류가 발생했습니다: {e}", parent=self.master)



#-----------------------------------------------------------------------------------

    def on_loan_tree_click(self, event):
        """대출 목록 Treeview 클릭 이벤트를 처리합니다."""
        region = self.current_loan_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.current_loan_tree.identify_column(event.x)
            # 마지막 컬럼('#4')이 '선택' 컬럼입니다.
            if column == '#4':
                item_id = self.current_loan_tree.identify_row(event.y)
                if item_id: # 행이 클릭되었는지 확인
                    self.open_check_in_window()

    def open_check_in_window(self):
        """도서 반납 창을 엽니다."""
        check_in_window = tk.Toplevel(self.master)
        CheckInWindow(check_in_window, self.db, self.user_id)
        # wait_window를 사용하면 상세창을 닫아야 원래 창을 조작할 수 있습니다.
        self.master.wait_window(check_in_window)
        # 상세창이 닫힌 후 대출 목록을 새로고침합니다.
        self.populate_loan_data()

    def on_loan_tree_motion(self, event):
        """마우스 움직임에 따라 '선택' 컬럼 위에서 커서를 변경합니다."""
        column = self.current_loan_tree.identify_column(event.x)
        # 마지막 컬럼('#4') 위일 때만 커서를 손가락 모양으로 변경
        if column == '#4':
            self.current_loan_tree.config(cursor="hand2")
        else:
            self.current_loan_tree.config(cursor="")

    def open_user_update_window(self):
        """회원 정보 수정 창을 엽니다."""
        if not self.user_data:
            messagebox.showerror("오류", "수정할 회원 정보가 없습니다.", parent=self.master)
            return

        try:
            update_window = tk.Toplevel(self.master)
            # 수정 창에 DB 객체, 현재 회원 데이터, 원본 전화번호를 전달합니다.
            UserUpdateWindow(update_window, self.db, self.user_data, self.user_id)
            self.master.wait_window(update_window)

            # 수정 창이 닫힌 후, 변경된 정보를 다시 불러와 화면을 갱신합니다.
            self.fetch_user_details()
            if self.user_data:
                self.populate_data()
                self.populate_loan_data() # 대출 정보도 새로고침
        except Exception as e:
            messagebox.showerror("DB 오류", f"회원 정보 수정 창을 여는 중 오류가 발생했습니다: {e}", parent=self.master)           

#-----------------------------------------------------------------------------------

# 이 파일을 직접 실행할 때 테스트하기 위한 코드
if __name__ == '__main__':
    class MockDB:
        def fetch_user_by_id(self, user_id):
            print(f"테스트: ID로 사용자 조회 - {user_id}")
            # (name, birthday, gender, tel_num, email, image_path) 형식의 튜플 반환
            return ("홍길동", "1990-01-01", "남", "010-1234-5678", "hong@example.com", None)

        def fetch_loans_by_user(self, user_tel):
            print(f"테스트: 전화번호로 대출 목록 조회 - {user_tel}")
            # (Title, Start_date, Isbn) 형식의 튜플 리스트 반환
            return [("클린코드", "2023-10-01", "978-89-6626-095-9"), ("오브젝트", "2023-10-10", "978-89-98139-76-6")]

        def fetch_past_loans_by_user(self, user_tel):
            print(f"테스트: 전화번호로 과거 대출 목록 조회 - {user_tel}")
            # (Title, Start_date, Return_date) 형식의 튜플 리스트 반환
            return [("이펙티브 자바", "2023-09-01", "2023-09-15")]

    root = tk.Tk()
    root.withdraw()
    
    db_mock = MockDB()
    test_user_id = 1
    
    app_window = tk.Toplevel(root)
    UserDetailWindow(app_window, db_mock, test_user_id)
    
    root.mainloop()

