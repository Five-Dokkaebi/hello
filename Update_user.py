import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class UserUpdateWindow:
    def __init__(self, master, db, user_data, user_id):
        self.master = master
        self.db = db
        # user_data is a tuple: (name, birthday, gender, tel_num, email, image_path)
        self.user_data = user_data
        self.user_id = user_id
        self.photo_path = user_data[5] if user_data and len(user_data) > 5 else None

        self.master.title("회원 수정")
        self.master.geometry("600x450")
        self.master.resizable(False, False)
        self.master.grab_set()

        self.create_widgets()
        self.populate_fields()

    def create_widgets(self):
        title_label = tk.Label(self.master, text="회원 수정", font=("Arial", 16, "bold"))
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        separator = tk.Frame(self.master, height=2, bg="black")
        separator.pack(fill="x", padx=15, pady=(0, 10))

        main_frame = tk.Frame(self.master)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="n", padx=(0, 15))

        self.preview_frame = tk.Frame(left_frame, width=150, height=180, bg="white", relief="solid", bd=1)
        self.preview_frame.pack()
        self.preview_frame.pack_propagate(False)

        self.photo_label = tk.Label(self.preview_frame, bg="white", text="이미지 미리보기")
        self.photo_label.pack(expand=True)

        photo_button = tk.Button(left_frame, text="사진 변경", command=self.select_photo)
        photo_button.pack(pady=5)

        form_frame = tk.Frame(main_frame)
        form_frame.grid(row=0, column=1, padx=10, pady=5, sticky="n")

        fields = ["이름", "생년월일 (YYYY-MM-DD)", "성별", "전화번호", "이메일"]
        self.entries = {}

        for i, field in enumerate(fields):
            label = tk.Label(form_frame, text=field, width=20, anchor="e")
            label.grid(row=i, column=0, sticky="e", pady=5)

            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            self.entries[field] = entry

        bottom_frame = tk.Frame(self.master)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        update_button = tk.Button(bottom_frame, text="수정 완료", width=15, command=self.confirm_update)
        update_button.pack(side="right")

    def populate_fields(self):
        name, birthday, gender, tel_num, email, _ = self.user_data
        
        self.entries["이름"].insert(0, name)
        self.entries["생년월일 (YYYY-MM-DD)"].insert(0, birthday)
        self.entries["성별"].insert(0, gender)
        self.entries["전화번호"].insert(0, tel_num)
        self.entries["이메일"].insert(0, email)
        
        if self.photo_path:
            self.show_image(self.photo_path)

    def show_image(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((150, 180))
            img_tk = ImageTk.PhotoImage(img)
            self.photo_label.config(image=img_tk, text="")
            self.photo_label.image = img_tk
        except Exception:
            self.photo_label.config(image=None, text="이미지 로드 실패")
            self.photo_label.image = None

    def select_photo(self):
        path = filedialog.askopenfilename(
            parent=self.master,
            title="사진 선택",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if path:
            self.photo_path = path
            self.show_image(path)

    def confirm_update(self):
        name = self.entries["이름"].get().strip()
        birthday = self.entries["생년월일 (YYYY-MM-DD)"].get().strip()
        gender = self.entries["성별"].get().strip()
        tel_num = self.entries["전화번호"].get().strip()
        email = self.entries["이메일"].get().strip()
        image_path = self.photo_path

        if not all([name, birthday, gender, tel_num]):
            messagebox.showwarning("입력 오류", "이름, 생년월일, 성별, 전화번호는 필수 항목입니다.", parent=self.master)
            return

        data_to_update = (name, birthday, gender, tel_num, email, image_path)

        try:
            self.db.update_user(data_to_update, self.user_id)
            messagebox.showinfo("성공", "회원 정보가 성공적으로 수정되었습니다.", parent=self.master)
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("DB 오류", f"회원 정보 수정에 실패했습니다: {e}", parent=self.master)

