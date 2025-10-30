import tkinter as tk
from tkinter import ttk, messagebox

class CheckInWindow:
    def __init__(self, master, db, user_id):
        self.master = master
        self.db = db
        self.user_id = user_id
        self.selected_rent_nums = set()

        self.master.title("도서 반납")
        self.master.geometry("800x450")
        self.master.resizable(False, False)
        self.master.grab_set()

        self.create_widgets()
        self.load_initial_data()

    def create_widgets(self):
        main_frame = tk.Frame(self.master, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)


        # --- 대출 도서 리스트 ---
        columns = ('select', '도서 제목', 'ISBN', '대여일', '반납예정일', '연체일수')
        self.loan_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.loan_tree.pack(fill=tk.BOTH, expand=True)

        self.loan_tree.heading('select', text='선택')
        self.loan_tree.column('select', width=50, anchor=tk.CENTER)
        self.loan_tree.heading('도서 제목', text='도서 제목')
        self.loan_tree.column('도서 제목', width=200)
        self.loan_tree.heading('ISBN', text='ISBN')
        self.loan_tree.column('ISBN', width=150, anchor=tk.CENTER)
        self.loan_tree.heading('대여일', text='대여일')
        self.loan_tree.column('대여일', width=100, anchor=tk.CENTER)
        self.loan_tree.heading('반납예정일', text='반납예정일')
        self.loan_tree.column('반납예정일', width=100, anchor=tk.CENTER)
        self.loan_tree.heading('연체일수', text='연체일수')
        self.loan_tree.column('연체일수', width=80, anchor=tk.CENTER)

        # 체크박스 클릭 이벤트
        self.loan_tree.bind("<Button-1>", self.on_tree_click)

        # --- 하단 반납 버튼 ---
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(10, 0))
        
        return_button = tk.Button(bottom_frame, text="반납하기", bg="lightblue", width=12, command=self.process_return)
        return_button.pack(side=tk.RIGHT)

    def load_initial_data(self):
        try:
            # DB에서 해당 회원의 모든 대출중인 도서 정보를 가져옴
            loan_list = self.db.fetch_all_current_loans_for_user(self.user_id)
            self.populate_treeview(loan_list)
        except Exception as e:
            messagebox.showerror("DB 오류", f"대출 목록을 불러오는 중 오류가 발생했습니다: {e}", parent=self.master)
            self.master.destroy()

    def populate_treeview(self, loan_list):
        for item in self.loan_tree.get_children():
            self.loan_tree.delete(item)
        
        for loan in loan_list:
            # (Title, Isbn, Start_date, End_date, Overdue_Days, rent_num)
            title, isbn, start_date, end_date, overdue, rent_num = loan
            # 연체일수가 0보다 작거나 같으면 0으로 표시
            overdue_display = overdue if overdue > 0 else 0
            display_values = ('☐', title, isbn, start_date, end_date, overdue_display)
            # rent_num을 item id로 사용하면 나중에 찾기 쉬움
            self.loan_tree.insert('', tk.END, iid=rent_num, values=display_values)

    def on_tree_click(self, event):
        region = self.loan_tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        column = self.loan_tree.identify_column(event.x)
        if column == '#1': # '선택' 컬럼
            item_id = self.loan_tree.identify_row(event.y)
            if not item_id:
                return
            
            rent_num = int(item_id)
            current_values = self.loan_tree.item(item_id, 'values')
            
            if rent_num in self.selected_rent_nums:
                self.selected_rent_nums.remove(rent_num)
                self.loan_tree.item(item_id, values=('☐',) + current_values[1:])
            else:
                self.selected_rent_nums.add(rent_num)
                self.loan_tree.item(item_id, values=('☑',) + current_values[1:])

    def process_return(self):
        if not self.selected_rent_nums:
            messagebox.showwarning("선택 오류", "반납할 도서를 선택해주세요.", parent=self.master)
            return

        confirm = messagebox.askyesno(
            "반납 확인",
            f"{len(self.selected_rent_nums)}개의 도서를 반납하시겠습니까?",
            parent=self.master
        )

        if confirm:
            try:
                self.db.process_bulk_return(list(self.selected_rent_nums))
                messagebox.showinfo("반납 완료", "선택한 도서가 반납 처리되었습니다.", parent=self.master)
                # 성공 후 창을 닫음
                self.master.destroy()
            except Exception as e:
                messagebox.showerror("DB 오류", f"반납 처리 중 오류가 발생했습니다: {e}", parent=self.master)

