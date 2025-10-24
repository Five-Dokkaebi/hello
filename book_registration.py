import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class BookRegistrationWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.photo_path = None

        self.master.title("도서 등록")
        self.master.geometry("600x500")
        self.master.resizable(False, False)
        self.master.grab_set()

        self.create_widgets()

    def create_widgets(self):
        # --- 제목 ---
        title_label = tk.Label(self.master, text="도서등록", font=("Arial", 16, "bold"))
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        separator = tk.Frame(self.master, height=2, bg="black")
        separator.pack(fill="x", padx=15, pady=(0, 10))

        # --- 메인 프레임 (좌우 배치) ---
        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # --- 왼쪽: 사진 등록 영역 ---
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="n", padx=(0, 15))

        self.preview_frame = tk.Frame(left_frame, width=150, height=200, bg="white", relief="solid", bd=1)
        self.preview_frame.pack()
        self.preview_frame.pack_propagate(False)

        self.photo_label = tk.Label(self.preview_frame, bg="white", text="이미지 미리보기")
        self.photo_label.pack(expand=True)

        photo_button = tk.Button(left_frame, text="사진선택", command=self.select_photo)
        photo_button.pack(pady=5)

        # --- 오른쪽: 도서 정보 입력 영역 ---
        form_frame = tk.Frame(main_frame)
        form_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

        fields = ["제목", "저자", "출판사", "가격", "링크", "ISBN"]
        self.entries = {}

        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field, width=8, anchor="e")
            label.grid(row=i, column=0, sticky="e", pady=2)

            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=2)
            self.entries[field] = entry

        # 책 설명
        desc_label = tk.Label(form_frame, text="책 설명", anchor="w")
        desc_label.grid(row=len(fields), column=0, sticky="ne", pady=2)
        self.desc_text = tk.Text(form_frame, width=30, height=5)
        self.desc_text.grid(row=len(fields), column=1, pady=2)

        # 하단: 등록 버튼 프레임
        bottom_frame = tk.Frame(self.master)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        register_button = tk.Button(bottom_frame, text="등록", width=15, command=self.register_book)
        register_button.pack(side="right")

    def select_photo(self):
        path = filedialog.askopenfilename(
            parent=self.master,
            title="사진 선택",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if path:
            self.photo_path = path
            img = Image.open(path)
            img.thumbnail((150, 200))
            img_tk = ImageTk.PhotoImage(img)

            self.photo_label.config(image=img_tk, text="")
            self.photo_label.image = img_tk

    def register_book(self):
        # Get data from entries
        title = self.entries["제목"].get().strip()
        author = self.entries["저자"].get().strip()
        publisher = self.entries["출판사"].get().strip()
        price_str = self.entries["가격"].get().strip()
        link = self.entries["링크"].get().strip()
        isbn = self.entries["ISBN"].get().strip()
        info = self.desc_text.get("1.0", tk.END).strip()
        image_path = self.photo_path

        if not all([title, author, publisher, isbn]):
             messagebox.showwarning("입력 오류", "제목, 저자, 출판사, ISBN은 필수 항목입니다.")
             return

        try:
            price = int(price_str) if price_str.isdigit() else 0
        except ValueError:
            messagebox.showwarning("입력 오류", "가격은 숫자로 입력해야 합니다.")
            return

        confirm_msg = (
            f"제목: {title}\n저자: {author}\n출판사: {publisher}\n"
            f"ISBN: {isbn}\n\n등록하시겠습니까?"
        )

        if not messagebox.askyesno("확인", confirm_msg):
            return

        # (ISBN, Title, Author, Publisher, Price, Link, Image_path, Info)
        data_to_insert = (isbn, title, author, publisher, price, link, image_path, info)

        try:
            self.db.insert_book(data_to_insert)
            messagebox.showinfo("성공", "도서가 성공적으로 등록되었습니다.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("DB 오류", f"도서 등록에 실패했습니다: {e}")
