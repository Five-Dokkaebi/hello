import tkinter as tk
from tkinter import ttk, messagebox
from book_loan_management import BookLoanWindow

class BookLookupWindow:
    def __init__(self, master, db, isbn):
        self.master = master
        self.db = db
        self.isbn = isbn

        self.master.title("동일 도서 목록 조회")
        self.master.geometry("600x400")
        self.master.resizable(False, False)
        self.master.grab_set()

        self.create_widgets()
        self.populate_book_list()

    def create_widgets(self):
        main_frame = tk.Frame(self.master, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(main_frame, text=f"ISBN: {self.isbn} 도서 목록", font=("Arial", 14, "bold"))
        title_label.pack(anchor="w", pady=(0, 10))

        columns = ("도서 제목", "대출 여부", "관리번호", "조회")
        self.lookup_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        self.lookup_tree.pack(fill=tk.BOTH, expand=True)

        col_widths = {"도서 제목": 200, "대출 여부": 80, "관리번호": 80, "조회": 80}
        for col, width in col_widths.items():
            self.lookup_tree.heading(col, text=col)
            self.lookup_tree.column(col, width=width, anchor=tk.CENTER)

        self.lookup_tree.bind("<Button-1>", self.on_lookup_tree_click)
        self.lookup_tree.bind("<Motion>", self.on_lookup_tree_motion)

    def populate_book_list(self):
        for item in self.lookup_tree.get_children():
            self.lookup_tree.delete(item)

        try:
            book_list = self.db.fetch_books_by_isbn_with_status(self.isbn)
            if not book_list:
                messagebox.showinfo("정보", "해당 ISBN을 가진 도서가 없습니다.", parent=self.master)
                self.master.destroy()
                return

            for book in book_list:
                values_with_button = list(book) + ["조회"]
                self.lookup_tree.insert('', tk.END, values=values_with_button)
        except Exception as e:
            messagebox.showerror("DB 오류", f"도서 목록을 불러오는 데 실패했습니다: {e}", parent=self.master)
            self.master.destroy()

    def on_lookup_tree_click(self, event):
        region = self.lookup_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.lookup_tree.identify_column(event.x)
            if column == '#4': # '조회' 컬럼
                item_id = self.lookup_tree.identify_row(event.y)
                item_values = self.lookup_tree.item(item_id, 'values')
                tracking_num = item_values[2] # 관리번호는 3번째 값
                self.open_book_detail_window(tracking_num)

    def open_book_detail_window(self, tracking_num):
        detail_window = tk.Toplevel(self.master)
        BookLoanWindow(detail_window, self.db, tracking_num)
        self.master.wait_window(detail_window)
        # Refresh the list in case the loan status changed
        self.populate_book_list()

    def on_lookup_tree_motion(self, event):
        column = self.lookup_tree.identify_column(event.x)
        if column == '#4':
            self.lookup_tree.config(cursor="hand2")
        else:
            self.lookup_tree.config(cursor="")

if __name__ == '__main__':
    # Test code
    class MockDB:
        def fetch_books_by_isbn_with_status(self, isbn):
            print(f"Fetching books for ISBN: {isbn}")
            return [
                ("클린 코드", "대출가능", 101),
                ("클린 코드", "대출중", 102),
                ("클린 코드", "대출가능", 103),
            ]
        def fetch_book_by_tracking_num(self, tracking_num):
            return ("클린 코드", "로버트 C. 마틴", "인사이트", "설명...", None, "978-89-6626-095-9")
        def fetch_users_by_book_loan(self, tracking_num):
            if tracking_num == 102:
                return [("김철수", "010-1234-5678", "2023-10-20", "2023-11-03")]
            return []

    root = tk.Tk()
    root.withdraw()
    db_mock = MockDB()
    test_isbn = "978-89-6626-095-9"
    app_window = tk.Toplevel(root)
    BookLookupWindow(app_window, db_mock, test_isbn)
    root.mainloop()

