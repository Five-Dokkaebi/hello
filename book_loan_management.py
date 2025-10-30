import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font
from PIL import Image, ImageTk

from Update_book import BookUpdateWindow


class BookLoanWindow:
    def __init__(self, master, db, tracking_num):
        self.master = master
        self.db = db
        self.tracking_num = tracking_num
        self.book_data = None
        self.borrower_tel = None # 대출 중인 회원의 전화번호 저장
        self.photo_path = None
        self.preview_width = 150
        self.preview_height = 200
        self.master.title("도서 정보와 대출 정보")
        self.master.geometry("1000x500")
        self.master.resizable(False, False)

        # 다른 창에서 팝업으로 띄울 경우, 이 창에 포커스를 고정합니다.
        self.master.grab_set()

        self.fetch_book_details()

        self.create_widgets()
        if self.book_data:
            self.populate_book_data()
            self.populate_loan_data()
        else:
            messagebox.showerror("오류", "도서 정보를 불러오는 데 실패했습니다.")
            self.master.destroy()

    def fetch_book_details(self):
        """DB에서 특정 도서의 상세 정보를 가져옵니다."""
        try:
            # book_mainpage.py의 OracleDB 클래스에 추가된 fetch_book_by_isbn 메서드를 사용합니다.
            self.book_data = self.db.fetch_book_by_tracking_num(self.tracking_num)
        except Exception as e:
            messagebox.showerror("DB 오류", f"도서 정보를 가져오는 중 오류가 발생했습니다: {e}")
            self.book_data = None

   
    def create_widgets(self):
        # --- 메인 컨테이너 프레임 ---
        main_frame = tk.Frame(self.master, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.grid_columnconfigure(0, weight=1) # 왼쪽 영역
        main_frame.grid_columnconfigure(1, weight=1) # 오른쪽 영역
        main_frame.grid_rowconfigure(0, weight=1)
        

        # --- 1. 왼쪽 영역: 도서 정보 ---
        left_container = tk.Frame(main_frame)
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # 도서정보 제목
        book_info_title = tk.Label(left_container, text="도서 정보", font=("Arial", 14, "bold"))
        book_info_title.pack(anchor="w", pady=(0, 5))
        separator_left = tk.Frame(left_container, height=2, bg="black")
        separator_left.pack(fill="x", pady=(0, 10))

        # 도서 정보 내용 프레임
        book_content_frame = tk.Frame(left_container)
        book_content_frame.pack(fill="both", expand=True)
    
        # 도서 정보 상단 (이미지 + 기본 정보)
        top_book_frame = tk.Frame(book_content_frame)
        top_book_frame.pack(fill=tk.X, pady=(0, 10))     

        # 이미지 프레임
        image_frame = tk.Frame(top_book_frame, width=150, height=200, bg="white", relief="solid", bd=1)
        image_frame.pack(side=tk.LEFT, padx=(0, 20), anchor="n")
        image_frame.pack_propagate(False)
        self.img_label = tk.Label(image_frame, text="이미지 없음", bg="white")
        self.img_label.pack(fill=tk.BOTH, expand=True)


        # 기본 정보 프레임 (제목, 저자, 출판사)
        details_frame = tk.Frame(top_book_frame)
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        detail_font = Font(family="Arial", size=11)
        detail_bold_font = Font(family="Arial", size=11, weight="bold")

        tk.Label(details_frame, text="제목:", font=detail_font).grid(row=0, column=0, sticky="w", pady=5)
        self.title_val_label = tk.Label(details_frame, text="", font=detail_bold_font, anchor="w")
        self.title_val_label.grid(row=0, column=1, sticky="w", padx=5)
        
        tk.Label(details_frame, text="저자:", font=detail_font).grid(row=1, column=0, sticky="w", pady=5)
        self.author_val_label = tk.Label(details_frame, text="", font=detail_bold_font, anchor="w")
        self.author_val_label.grid(row=1, column=1, sticky="w", padx=5)
        
        tk.Label(details_frame, text="출판사:", font=detail_font).grid(row=2, column=0, sticky="w", pady=5)
        self.publisher_val_label = tk.Label(details_frame, text="", font=detail_bold_font, anchor="w")
        self.publisher_val_label.grid(row=2, column=1, sticky="w", padx=5)

        # 도서 정보 하단 (책 설명)
        bottom_book_frame = tk.Frame(book_content_frame)
        bottom_book_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(bottom_book_frame, text="책 설명", font=detail_bold_font).pack(anchor="w", pady=(10, 5))
        self.desc_text = tk.Text(bottom_book_frame, height=5, font=("Arial", 10), relief="solid", borderwidth=1)
        self.desc_text.pack(fill=tk.BOTH, expand=True)
        self.desc_text.config(state=tk.DISABLED) # 읽기 전용으로 설정

        # ISBN 라벨 추가
        self.isbn_label = tk.Label(bottom_book_frame, text="ISBN: ", font=detail_font)
        self.isbn_label.pack(anchor="w", pady=(5, 0))

        # 하단 버튼 (수정, 삭제)
        bottom_button_frame = tk.Frame(left_container)
        bottom_button_frame.pack(fill="x", side="bottom", pady=(10, 0))
        delete_btn = tk.Button(bottom_button_frame, text="삭제", bg="lightcoral", width=10, command=self.confirm_delete_book)
        delete_btn.pack(side="right", padx=5, pady=5)
        edit_btn = tk.Button(bottom_button_frame, text="수정", bg="lightblue", width=10, command=self.open_book_update_window)
        edit_btn.pack(side="right", padx=5, pady=5)


        # --- 2. 오른쪽 영역: 대출 정보 ---
        right_container = tk.Frame(main_frame)
        right_container.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # 대출정보 제목
        loan_info_title = tk.Label(right_container, text="대출 정보", font=("Arial", 14, "bold"))
        loan_info_title.pack(anchor="w", pady=(0, 5))
        separator_right = tk.Frame(right_container, height=2, bg="black")
        separator_right.pack(fill="x", pady=(0, 10))

        # 대출 상태
        self.loan_status_label = tk.Label(right_container, text="", font=("Arial", 14, "bold"))
        self.loan_status_label.pack(anchor="w", pady=(0, 10))

        # 회원 검색
        search_frame = tk.Frame(right_container)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        self.member_search_entry = tk.Entry(search_frame, font=("Arial", 10), relief="solid", bd=1)
        self.member_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.member_search_button = tk.Button(search_frame, text="검색", command=self.search_members)
        self.member_search_button.pack(side=tk.LEFT)

        # 검색 결과 목록 (Treeview 사용)
        columns = ("회원번호", "회원명", "상태", "선택")
        self.member_tree = ttk.Treeview(right_container, columns=columns, show="headings")
        self.member_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # 각 컬럼의 너비를 직접 지정하여 스크롤바가 생기지 않도록 합니다.
        col_widths = {"회원번호": 100, "회원명": 150, "상태": 80, "선택": 80}
        for col, width in col_widths.items():
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, width=width, anchor=tk.CENTER)

        # '선택' 버튼 기능 연결
        self.member_tree.bind("<Button-1>", self.on_member_tree_click)
        self.member_tree.bind("<Motion>", self.on_member_tree_motion)

    def populate_book_data(self):
        """가져온 도서 데이터로 위젯을 채웁니다."""
        # book_data 인덱스: 0:Title, 1:Author, 2:Publisher, 3:Price, 4:Link, 5:Info, 6:Image_path, 7:Isbn
        title, author, publisher, price, link, info, image_path, isbn = self.book_data

        self.title_val_label.config(text=title)
        self.author_val_label.config(text=author)
        self.publisher_val_label.config(text=publisher)

        self.desc_text.config(state=tk.NORMAL)
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert(tk.END, info if info else "")
        self.desc_text.config(state=tk.DISABLED)

        self.isbn_label.config(text=f"ISBN: {isbn}")

        self.photo_path = image_path
        if self.photo_path:
            try:
                img = Image.open(self.photo_path)
                img = img.resize((self.preview_width, self.preview_height), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.img_label.config(image=img_tk, text="")
                self.img_label.image = img_tk
            except Exception:
                self.img_label.config(image=None, text="이미지 로드 실패")
                self.img_label.image = None
        else:
            self.img_label.config(image=None, text="이미지 없음")
            self.img_label.image = None

    def populate_loan_data(self):
        """DB에서 도서의 대출 정보를 가져와 테이블에 표시합니다."""
        try:
            # fetch_users_by_book_loan은 현재 대출 중인 회원 목록을 반환
            loan_list = self.db.fetch_users_by_book_loan(self.tracking_num)

            # 기존 테이블 내용 지우기
            for item in self.member_tree.get_children():
                self.member_tree.delete(item)

            if loan_list:
                # 대출 중인 경우
                self.loan_status_label.config(text="대출중", fg="red")

                self.borrower_tel = loan_list[0][1] if loan_list else None
                # 검색 기능 비활성화
                self.member_search_entry.delete(0, tk.END)
                self.member_search_entry.insert(0, "현재 대출 중인 도서입니다.")
                self.member_search_entry.config(state=tk.DISABLED)
                self.member_search_button.config(state=tk.DISABLED)
            else:
                # 대출 가능한 경우
                self.loan_status_label.config(text="대출가능", fg="green")
                self.borrower_tel = None
                # 검색 기능 활성화
                self.member_search_entry.config(state=tk.NORMAL)
                self.member_search_entry.delete(0, tk.END)
                self.member_search_entry.insert(0, "회원 이름 또는 회원번호로 검색")
                self.member_search_button.config(state=tk.NORMAL)
        except AttributeError:
             messagebox.showwarning("알림", "대출 정보를 가져오는 DB 기능이 아직 구현되지 않았습니다.")
        except Exception as e:
            messagebox.showerror("DB 오류", f"대출 정보를 가져오는 중 오류가 발생했습니다: {e}")

    def search_members(self):
        """회원 검색을 수행하고 결과를 테이블에 표시합니다."""
        keyword = self.member_search_entry.get().strip()
        if not keyword or keyword == "회원 이름 또는 회원번호로 검색":
            messagebox.showinfo("알림", "검색할 회원 이름 또는 번호를 입력하세요.", parent=self.master)
            return

        try:
            user_list = self.db.search_users_for_loan(keyword)
            
            for item in self.member_tree.get_children():
                self.member_tree.delete(item)

            if not user_list:
                messagebox.showinfo("검색 결과", "일치하는 회원이 없습니다.", parent=self.master)
            else:
                for user in user_list:
                    values = (user[0], user[1], "대출가능", "선택")
                    self.member_tree.insert('', tk.END, values=values)
        except Exception as e:
            messagebox.showerror("DB 오류", f"회원 검색 중 오류가 발생했습니다: {e}", parent=self.master)

    def on_member_tree_click(self, event):
        """회원 검색 결과 테이블 클릭 이벤트를 처리하여 대출을 진행합니다."""
        # '대출가능' 상태가 아니면 아무 동작도 하지 않음
        if self.loan_status_label.cget("text") != "대출가능":
            return
        region = self.member_tree.identify("region", event.x, event.y)
        if region == "cell" and self.member_tree.identify_column(event.x) == '#4': # '선택' 컬럼
            item_id = self.member_tree.identify_row(event.y)
            values = self.member_tree.item(item_id, 'values')
            user_id = values[0]
            user_name = values[1]

            # 1. 대출 확인 알림창 표시
            confirm = messagebox.askyesno(
                "대출 확인",
                f"'{user_name}' 회원님으로 대여하시겠습니까?",
                parent=self.master
            )

            if confirm:
                try:
                    # 2. 회원의 연체 여부 확인
                    is_overdue = self.db.check_overdue_status(user_id)
                    if is_overdue:
                        messagebox.showerror("대출 불가", "이 회원은 연체된 책이 있으므로 대여할 수 없습니다.", parent=self.master)
                        return

                    # 3. 대출 처리
                    end_date = self.db.process_loan(self.tracking_num, user_id)
                    
                    # 4. 성공 메시지 표시
                    end_date_str = end_date.strftime('%Y.%m.%d %H:%M:%S')
                    messagebox.showinfo("대출 완료", f"대여되었습니다.\n반납기간: {end_date_str}", parent=self.master)

                    # 5. 대출 완료 후 창 닫기
                    self.master.destroy()

                except Exception as e:
                    messagebox.showerror("DB 오류", f"대출 처리 중 오류가 발생했습니다: {e}", parent=self.master)

    def on_member_tree_motion(self, event):
        """마우스 움직임에 따라 '선택' 컬럼 위에서 커서를 변경합니다."""
        column = self.member_tree.identify_column(event.x)
        if column == '#4':
            self.member_tree.config(cursor="hand2")
        else:
            self.member_tree.config(cursor="")

    def open_book_update_window(self):
        """도서 정보 수정 창을 엽니다."""
        if not self.book_data:
            messagebox.showerror("오류", "수정할 도서 정보가 없습니다.", parent=self.master)
            return

        try:
            update_window = tk.Toplevel(self.master)
            # 수정 창에 DB 객체, 현재 도서 데이터, 관리번호를 전달합니다.
            BookUpdateWindow(update_window, self.db, self.book_data, self.tracking_num)
            self.master.wait_window(update_window)

            # 수정 창이 닫힌 후, 변경된 정보를 다시 불러와 화면을 갱신합니다.
            self.fetch_book_details()
            if self.book_data:
                self.populate_book_data()
                self.populate_loan_data() # 대출 정보도 새로고침
        except Exception as e:
            messagebox.showerror("DB 오류", f"도서 정보 수정 창을 여는 중 오류가 발생했습니다: {e}", parent=self.master)

    def confirm_delete_book(self):
        """도서 삭제를 확인하고 처리합니다."""
        try:
            # 1. 대출 중인지 확인
            is_on_loan = self.db.is_book_on_loan(self.tracking_num)
            if is_on_loan:
                messagebox.showwarning("삭제 불가", "대여중이므로 삭제할 수 없습니다.", parent=self.master)
                return

            # 2. 사용자에게 재확인
            book_title = self.title_val_label.cget("text")
            confirm = messagebox.askyesno(
                "도서 삭제 확인",
                f"'{book_title}' 도서를 정말로 삭제 처리하시겠습니까?\n이 작업은 되돌릴 수 없습니다.",
                parent=self.master
            )

            if confirm:
                # 3. 논리적 삭제 실행
                self.db.soft_delete_book(self.tracking_num)
                messagebox.showinfo("성공", "도서 삭제 처리가 완료되었습니다.", parent=self.master)
                self.master.destroy()
        except Exception as e:
            messagebox.showerror("DB 오류", f"도서 삭제 처리 중 오류가 발생했습니다: {e}", parent=self.master)



# --- 실행 테스트용 ---

if __name__ == '__main__':
    root = tk.Tk()
     # 불필요한 빈 tk 창(root)을 화면에 표시하지 않고 숨깁니다.
    root.withdraw()
    # 테스트를 위한 Mock DB 클래스
    class MockDB:
        def fetch_book_by_tracking_num(self, tracking_num):
            return ("테스트 도서", "테스트 저자", "테스트 출판사", "이것은 테스트용 도서 설명입니다.", None, "1234567890")
        def fetch_user_by_tel(self, tel_num):
            return ("홍길동", "1990-01-01", "남", "010-1111-2222", "hong@example.com", None)

    db_mock = MockDB()
    test_tracking_num = 1
    app = BookLoanWindow(tk.Toplevel(root), db_mock, test_tracking_num)
    root.mainloop()