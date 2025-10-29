import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class BookUpdateWindow:
    def __init__(self, master, db, book_data, tracking_num):
        self.master = master
        self.db = db
        # book_data is a tuple: (Title, Author, Publisher, Price, Link, Info, Image_path, Isbn)
        self.book_data = book_data
        self.tracking_num = tracking_num
        self.photo_path = book_data[6] if book_data and len(book_data) > 6 else None

        self.master.title("도서 정보 수정")
        self.master.geometry("600x500")
        self.master.resizable(False, False)
        self.master.grab_set()

        self.create_widgets()
        self.populate_fields()

    def create_widgets(self):
        title_label = tk.Label(self.master, text="도서 정보 수정", font=("Arial", 16, "bold"))
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        separator = tk.Frame(self.master, height=2, bg="black")
        separator.pack(fill="x", padx=15, pady=(0, 10))

        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="n", padx=(0, 15))

        self.preview_frame = tk.Frame(left_frame, width=150, height=200, bg="white", relief="solid", bd=1)
        self.preview_frame.pack()
        self.preview_frame.pack_propagate(False)

        self.photo_label = tk.Label(self.preview_frame, bg="white", text="이미지 미리보기")
        self.photo_label.pack(expand=True)

        photo_button = tk.Button(left_frame, text="사진 변경", command=self.select_photo)
        photo_button.pack(pady=5)

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

        desc_label = tk.Label(form_frame, text="책 설명", anchor="w")
        desc_label.grid(row=len(fields), column=0, sticky="ne", pady=2)
        self.desc_text = tk.Text(form_frame, width=30, height=5)
        self.desc_text.grid(row=len(fields), column=1, pady=2)

        bottom_frame = tk.Frame(self.master)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        update_button = tk.Button(bottom_frame, text="수정 완료", width=15, command=self.confirm_update)
        update_button.pack(side="right")

    def populate_fields(self):
        title, author, publisher, price, link, info, image_path, isbn = self.book_data
        
        self.entries["제목"].insert(0, title)
        self.entries["저자"].insert(0, author)
        self.entries["출판사"].insert(0, publisher)
        self.entries["가격"].insert(0, price if price is not None else "")
        self.entries["링크"].insert(0, link if link is not None else "")
        self.entries["ISBN"].insert(0, isbn)
        
        self.desc_text.insert("1.0", info if info else "")
        
        if self.photo_path:
            self.show_image(self.photo_path)

    def show_image(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((150, 200))
            img_tk = ImageTk.PhotoImage(img)
            self.photo_label.config(image=img_tk, text="")
            self.photo_label.image = img_tk
        except Exception:
            self.photo_label.config(image=None, text="이미지 로드 실패")

    def select_photo(self):
        path = filedialog.askopenfilename(parent=self.master, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.photo_path = path
            self.show_image(path)

    def confirm_update(self):
        title = self.entries["제목"].get().strip()
        author = self.entries["저자"].get().strip()
        publisher = self.entries["출판사"].get().strip()
        price_str = self.entries["가격"].get().strip()
        link = self.entries["링크"].get().strip()
        isbn = self.entries["ISBN"].get().strip()
        info = self.desc_text.get("1.0", tk.END).strip()
        image_path = self.photo_path

        if not all([title, author, publisher, isbn]):
            messagebox.showwarning("입력 오류", "제목, 저자, 출판사, ISBN은 필수 항목입니다.", parent=self.master)
            return
        
        try:
            price = int(price_str) if price_str.isdigit() else 0
        except ValueError:
            messagebox.showwarning("입력 오류", "가격은 숫자로 입력해야 합니다.", parent=self.master)
            return

        data_to_update = (title, author, publisher, price, link, info, image_path, isbn)

        try:
            self.db.update_book(data_to_update, self.tracking_num)
            messagebox.showinfo("성공", "도서 정보가 성공적으로 수정되었습니다.", parent=self.master)
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("DB 오류", f"도서 정보 수정에 실패했습니다: {e}", parent=self.master)

