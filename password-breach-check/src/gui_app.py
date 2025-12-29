import customtkinter as ctk
from tkinter import messagebox

from .checker import check_password_pwned, evaluate_password_strength
from .hibp_client import HibpClientError


class PasswordCheckGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Pencere ayarları
        self.title("Password Breach Checker")
        self.geometry("900x650")
        self.minsize(800, 600)
        self.resizable(True, True)

        ctk.set_appearance_mode("dark")      # "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

        # Ana container (ortalanmış kart)
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(expand=True, padx=20, pady=20, fill="both")

        # Üst başlık satırı
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.header_frame.pack(fill="x", pady=(10, 0), padx=20)

        self.label_title = ctk.CTkLabel(
            self.header_frame,
            text="Password Breach Check",
            font=("Segoe UI", 22, "bold"),
        )
        self.label_title.pack(side="left")

        # Tema seçimi (light/dark)
        self.theme_option = ctk.CTkOptionMenu(
            self.header_frame,
            values=["Dark", "Light", "System"],
            command=self.change_theme,
            width=110,
        )
        self.theme_option.set("Dark")
        self.theme_option.pack(side="right")

        # Parola girişi alanı
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=20, pady=(15, 5))

        self.entry_password = ctk.CTkEntry(
            self.input_frame,
            width=350,
            placeholder_text="Parolanızı girin",
            show="*",
        )
        self.entry_password.grid(row=0, column=0, padx=(0, 10), pady=(0, 5), sticky="w")

        self.show_password_var = ctk.BooleanVar(value=False)
        self.check_show_password = ctk.CTkCheckBox(
            self.input_frame,
            text="Göster",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
        )
        self.check_show_password.grid(row=0, column=1, sticky="w")

        # Butonlar
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.btn_check = ctk.CTkButton(
            self.button_frame,
            text="Kontrol Et",
            command=self.check_password,
            width=140,
        )
        self.btn_check.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.btn_clear = ctk.CTkButton(
            self.button_frame,
            text="Temizle",
            command=self.clear_fields,
            width=90,
            fg_color="gray30",
            hover_color="gray40",
        )
        self.btn_clear.grid(row=0, column=1, pady=5, sticky="w")

        # Güç analizi bölümü
        self.strength_frame = ctk.CTkFrame(self.main_frame)
        self.strength_frame.pack(fill="x", padx=20, pady=(5, 10))

        self.label_strength_title = ctk.CTkLabel(
            self.strength_frame,
            text="Parola Gücü",
            font=("Segoe UI", 14, "bold"),
        )
        self.label_strength_title.pack(anchor="w", pady=(8, 2), padx=10)

        self.strength_bar = ctk.CTkProgressBar(
            self.strength_frame,
            height=12,
        )
        self.strength_bar.set(0)
        self.strength_bar.pack(fill="x", padx=10, pady=(0, 5))

        self.label_strength = ctk.CTkLabel(
            self.strength_frame,
            text="Henüz analiz edilmedi.",
            font=("Segoe UI", 12),
        )
        self.label_strength.pack(anchor="w", padx=10, pady=(0, 8))

        # Sonuç metin kutusu
        self.result_frame = ctk.CTkFrame(self.main_frame)
        self.result_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.label_result_title = ctk.CTkLabel(
            self.result_frame,
            text="Sonuç",
            font=("Segoe UI", 14, "bold"),
        )
        self.label_result_title.pack(anchor="w", padx=10, pady=(8, 2))

        self.result_box = ctk.CTkTextbox(
            self.result_frame,
            width=500,
            height=180,
        )
        self.result_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # ------------------------------------------------------------------
    # Yardımcı fonksiyonlar
    # ------------------------------------------------------------------

    def change_theme(self, mode: str):
        """Tema değiştir (Dark / Light / System)."""
        mode = mode.lower()
        if mode == "dark":
            ctk.set_appearance_mode("dark")
        elif mode == "light":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("system")

    def toggle_password_visibility(self):
        """Parola giriş alanını göster/gizle."""
        if self.show_password_var.get():
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")

    def clear_fields(self):
        """Parola girişini ve sonuç alanını temizle."""
        self.entry_password.delete(0, "end")
        self.result_box.delete("1.0", "end")
        self.strength_bar.set(0)
        self.label_strength.configure(text="Henüz analiz edilmedi.")

    def update_strength_ui(self, strength: dict):
        """Parola güç analizine göre progress bar ve label güncelle."""
        score = strength.get("score", 0)  # 0–4 arası
        label = strength.get("label", "bilinmiyor")

        # Progress bar değeri (0–1 arası)
        value = max(0, min(score / 4, 1))
        self.strength_bar.set(value)

        # Renk tonları score'a göre değişebilir (soft şekilde)
        if score <= 1:
            strength_text = f"Güç: {label} (skor: {score}/4)"
        elif score == 2:
            strength_text = f"Güç: {label} (skor: {score}/4)"
        elif score == 3:
            strength_text = f"Güç: {label} (skor: {score}/4)"
        else:
            strength_text = f"Güç: {label} (skor: {score}/4)"

        self.label_strength.configure(text=strength_text)

    # ------------------------------------------------------------------
    # Ana iş mantığı
    # ------------------------------------------------------------------

    def check_password(self):
        password = self.entry_password.get()
        if not password:
            messagebox.showwarning("Uyarı", "Lütfen bir parola girin.")
            return

        try:
            strength = evaluate_password_strength(password)
            is_pwned, count = check_password_pwned(password)
            
        except HibpClientError as exc:
            messagebox.showerror("API Hatası", f"HIBP hatası: {exc}")
            return
        except Exception as exc:
            messagebox.showerror("Hata", f"Beklenmeyen hata: {exc}")
            return

        # Güç barını güncelle
        self.update_strength_ui(strength)

        # Sonuç metnini yaz
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", f"Parola uzunluğu: {strength['length']}\n")
        self.result_box.insert("end", f"Parola gücü: {strength['label']} (skor: {strength['score']}/4)\n\n")

        if strength["reasons"]:
            self.result_box.insert("end", "Güç Analizi Notları:\n")
            for reason in strength["reasons"]:
                self.result_box.insert("end", f" - {reason}\n")
            self.result_box.insert("end", "\n")

        if is_pwned:
            self.result_box.insert("end", "⚠ Bu parola ihlal edilmiş!\n")
            self.result_box.insert("end", f"{count} kez veri ihlallerinde görülmüş.\n")
            self.result_box.insert(
                "end",
                "\nÖneri: Bu parolayı derhal değiştirin ve farklı hesaplarda tekrar kullanmayın.\n",
            )
        else:
            self.result_box.insert("end", "Bu parola HIBP veritabanında bulunmamış.\n")
            self.result_box.insert(
                "end",
                "Yine de benzersiz, uzun ve karmaşık parolalar kullanmanız önerilir.\n",
            )


def run_gui():
    app = PasswordCheckGUI()
    app.mainloop()


if __name__ == "__main__":
    run_gui()
