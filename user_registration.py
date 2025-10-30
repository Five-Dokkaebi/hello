import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import oracledb

class OracleDB:
    def __init__(self):
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


class MemberRegistrationWindow:
    def __init__(self, master, db):
        self.master = master
        self.db = db
        self.photo_path = None
        # 미리보기 이미지 크기 (픽셀 단위)
        self.preview_width = 150
        self.preview_height = 180
        self.master.grab_set()  # 팝업 창이 포커스를 잃지 않도록 설정
        self.create_ui()

    def create_ui(self):
        self.master.title("회원 등록")
        self.master.geometry("600x450")
        self.master.resizable(False, False)

        # --- 제목 ---
        title_label = tk.Label(self.master, text="회원등록", font=("Arial", 16, "bold"))
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        separator = tk.Frame(self.master, height=2, bg="black")
        separator.pack(fill="x", padx=15, pady=(0, 10))

        # --- 메인 영역 ---
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # 왼쪽: 사진 등록
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="n", padx=(0, 15))

        # 고정 크기의 Frame으로 미리보기 영역을 만듦
        self.preview_frame = tk.Frame(left_frame, width=self.preview_width, height=self.preview_height, bg="white", relief="solid", bd=1)
        self.preview_frame.pack()
        self.preview_frame.pack_propagate(False)  # 내부 위젯 크기로 프레임이 늘어나지 않게 함

        self.photo_label = tk.Label(self.preview_frame, bg="white")
        self.photo_label.pack(expand=True)

        photo_btn = tk.Button(left_frame, text="사진선택", command=self.select_photo)
        photo_btn.pack(pady=5)

        # 오른쪽: 입력 영역
        right_frame = tk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky="n")

        labels = ["이름", "생년월일(YYYY-MM-DD)", "성별", "전화번호", "이메일"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(right_frame, text=label_text, width=15, anchor="e", font=("맑은 고딕", 10, "bold"))
            label.grid(row=i, column=0, sticky="e", pady=7)
            entry = tk.Entry(right_frame, width=30)
            entry.grid(row=i, column=1, pady=7)
            self.entries[label_text] = entry

        # 하단 버튼
        bottom_frame = tk.Frame(self.master)
        bottom_frame.pack(fill="x", padx=20, pady=10)

        register_btn = tk.Button(bottom_frame, text="등록", bg="lightgray", width=10, command=self.register_member)
        register_btn.pack(side="right", padx=5, pady=5)

    # -----------------------------
    # 사진 선택 기능 (미리보기)
    # -----------------------------
    def select_photo(self):
        path = filedialog.askopenfilename(
            title="사진 선택",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if path:
            self.photo_path = path
            img = Image.open(path)

            # 이미지 크기를 미리보기 영역에 맞게 리사이즈
            img = img.resize((self.preview_width, self.preview_height), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)

            self.photo_label.config(image=img_tk)
            self.photo_label.image = img_tk

    # -----------------------------
    # 등록 버튼 클릭 시 동작
    # -----------------------------
    def register_member(self):
        name = self.entries["이름"].get().strip()
        birth = self.entries["생년월일(YYYY-MM-DD)"].get().strip()
        gender = self.entries["성별"].get().strip()
        phone = self.entries["전화번호"].get().strip()
        email = self.entries["이메일"].get().strip()
        image_path = self.photo_path if self.photo_path else None

        if not all([name, birth, gender, phone, email]):
            messagebox.showwarning("입력 오류", "모든 항목을 입력하세요.")
            return

        confirm = (
            f"이름: {name}\n생년월일: {birth}\n성별: {gender}\n"
            f"전화번호: {phone}\n이메일: {email}\n이미지: {image_path or '없음'}\n\n"
            "등록하시겠습니까?"
        )

        if not messagebox.askyesno("확인", confirm):
            return

        try:
            self.db.insert_user_reg((name, birth, gender, phone, email, image_path))
            messagebox.showinfo("성공", "회원이 성공적으로 등록되었습니다.")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("DB 오류", str(e))


# -----------------------------
# 실행 테스트용
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    db = OracleDB()
    MemberRegistrationWindow(tk.Toplevel(root), db)
    root.mainloop()
