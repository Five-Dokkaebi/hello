import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.font import Font


class BookManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("도서 관리 프로그램")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)  # 최소 창 크기 설정

        self.create_main_ui()

    def create_main_ui(self):
        # 상단 검색 바 및 타이틀
        title_font = Font(family="Arial", size=18, weight="bold")
        ttk.Label(self.root, text="도서 관리 프로그램", font=title_font).pack(pady=10)

        search_frame = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        search_frame.pack(fill=tk.X)
        ttk.Label(search_frame, text="제목 또는 저자를 입력하십시오:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(search_frame, width=50).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        ttk.Button(search_frame, text="검색").pack(side=tk.LEFT)

        # 탭 및 버튼 프레임
        tab_frame = ttk.Frame(self.root, padding=(10, 0, 10, 5))
        tab_frame.pack(fill=tk.X)
        ttk.Button(tab_frame, text="도서관리").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(tab_frame, text="회원관리").pack(side=tk.LEFT)

        # '도서등록' 버튼 클릭 시 새 창 열기
        ttk.Button(tab_frame, text="도서등록", command=self.open_registration_window).pack(side=tk.RIGHT)

        # 도서 목록을 보여줄 Treeview
        columns = ("제목", "ISBN", "저자", "가격", "출판사")
        self.book_tree = ttk.Treeview(self.root, columns=columns, show="headings")
        self.book_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        for col in columns:
            self.book_tree.heading(col, text=col)
            self.book_tree.column(col, width=150, anchor=tk.CENTER)

    def open_registration_window(self):
        # 도서 등록 팝업 창을 Tkinter Toplevel 위젯으로 생성
        register_window = tk.Toplevel(self.root)
        register_window.title("도서 등록")
        register_window.geometry("600x500")
        register_window.resizable(False, False)
        register_window.grab_set()  # 팝업 창이 열리면 메인 창 제어 불가

        # --- 메인 프레임 (좌우 배치) ---
        main_frame = tk.Frame(register_window)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # --- 왼쪽: 사진 등록 영역 ---
        photo_frame = tk.Frame(main_frame, width=150, height=200, bg="gray")
        photo_frame.grid(row=0, column=0, padx=10, pady=5, rowspan=2, sticky="n")

        photo_frame.pack_propagate(False)
        photo_label = tk.Label(photo_frame, text="이미지\n미리보기", bg="gray", fg="white")
        photo_label.pack(expand=True)

        photo_button = tk.Button(main_frame, text="사진선택",
                                 command=lambda: filedialog.askopenfilename(
                                     title="사진 선택",
                                     filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
                                 ))
        photo_button.grid(row=2, column=0, pady=5)

        # --- 오른쪽: 도서 정보 입력 영역 ---
        form_frame = tk.Frame(main_frame)
        form_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

        fields = ["제목", "저자", "출판사", "가격", "장르", "ISBN"]
        self.entries = {}

        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field, width=8, anchor="w")
            label.grid(row=i, column=0, sticky="e", pady=2)

            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=2)
            self.entries[field] = entry

        # 책 설명
        desc_label = tk.Label(form_frame, text="책 설명", anchor="w")
        desc_label.grid(row=len(fields), column=0, sticky="ne", pady=2)
        desc_text = tk.Text(form_frame, width=30, height=5)
        desc_text.grid(row=len(fields), column=1, pady=2)

        # 하단: 현재번호 + 등록 버튼 프레임
        bottom_frame = tk.Frame(register_window)
        bottom_frame.pack(fill="x", padx=10, pady=10)

        number_label = tk.Label(bottom_frame, text="현재번호 : 2", fg="gray")
        number_label.pack(side="left")

        register_button = tk.Button(bottom_frame, text="등록", width=15, bg="#4CAF50", fg="white",
                                    command=lambda: messagebox.showinfo("안내", "등록 기능 구현 필요"))
        register_button.pack(side="right")


if __name__ == "__main__":
    root = tk.Tk()
    app = BookManagerApp(root)
    root.mainloop()
