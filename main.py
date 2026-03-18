import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread, Event
import time
from pynput.keyboard import Controller, Key

class PressEnterLaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Press Enter Later")
        self.root.geometry("250x380")
        self.root.resizable(False, False)
        
        self.keyboard = Controller()
        self.stop_event = Event()
        self.is_running = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # キー選択
        ttk.Label(main_frame, text="押すキー:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.key_var = tk.StringVar(value="Enter")
        key_combo = ttk.Combobox(main_frame, textvariable=self.key_var, width=15, state="readonly")
        key_combo['values'] = ('Enter', 'Space', 'Tab', 'Esc', 'a', 'b', 'c', 'd', 'e', 'f')
        key_combo.grid(row=0, column=1, sticky=tk.W, pady=5)
        key_combo.bind('<<ComboboxSelected>>', lambda e: self.update_preview())
        
        # 開始までの遅延時間（秒）
        ttk.Label(main_frame, text="開始までの時間 (秒):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.delay_var = tk.StringVar(value="3")
        delay_entry = ttk.Entry(main_frame, textvariable=self.delay_var, width=17)
        delay_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        delay_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 時間追加ボタン
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(button_frame, text="+1時間", command=self.add_one_hour, width=8).grid(row=0, column=0, padx=3)
        ttk.Button(button_frame, text="+10分", command=self.add_ten_minutes, width=8).grid(row=0, column=1, padx=3)
        ttk.Button(button_frame, text="+1分", command=self.add_one_minute, width=8).grid(row=0, column=2, padx=3)
        
        # セパレーター
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 繰り返し回数
        ttk.Label(main_frame, text="繰り返し回数:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.repeat_var = tk.StringVar(value="1")
        repeat_entry = ttk.Entry(main_frame, textvariable=self.repeat_var, width=17)
        repeat_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        repeat_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # 繰り返し間隔
        ttk.Label(main_frame, text="繰り返し間隔 (秒):").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.repeat_interval_var = tk.StringVar(value="1")
        interval_entry = ttk.Entry(main_frame, textvariable=self.repeat_interval_var, width=17)
        interval_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
        interval_entry.bind('<KeyRelease>', lambda e: self.update_preview())
        
        # ボタン
        button_control_frame = ttk.Frame(main_frame)
        button_control_frame.grid(row=6, column=0, columnspan=2, pady=15)
        
        self.start_button = ttk.Button(button_control_frame, text="開始", command=self.start_automation)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(button_control_frame, text="停止", command=self.stop_automation, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)
        
        # プレビュー
        self.preview_var = tk.StringVar(value="")
        preview_label = ttk.Label(main_frame, textvariable=self.preview_var, font=("", 9), foreground="blue", wraplength=225, justify=tk.LEFT)
        preview_label.grid(row=7, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        # ステータス
        self.status_var = tk.StringVar(value="待機中")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("", 10, "bold"))
        status_label.grid(row=8, column=0, columnspan=2, pady=5)
        
        # 初期プレビュー更新
        self.update_preview()
    
    def add_one_hour(self):
        """1時間追加"""
        try:
            current = int(self.delay_var.get())
            self.delay_var.set(str(current + 3600))
            self.update_preview()
        except ValueError:
            self.delay_var.set("3600")
            self.update_preview()
    
    def add_ten_minutes(self):
        """10分追加"""
        try:
            current = int(self.delay_var.get())
            self.delay_var.set(str(current + 600))
            self.update_preview()
        except ValueError:
            self.delay_var.set("600")
            self.update_preview()
    
    def add_one_minute(self):
        """1分追加"""
        try:
            current = int(self.delay_var.get())
            self.delay_var.set(str(current + 60))
            self.update_preview()
        except ValueError:
            self.delay_var.set("60")
            self.update_preview()
    
    def format_time(self, seconds):
        """秒数を「何時間何分何秒」形式に変換"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        parts = []
        if hours > 0:
            parts.append(f"{hours}時間")
        if minutes > 0:
            parts.append(f"{minutes}分")
        if secs > 0 or len(parts) == 0:
            parts.append(f"{secs}秒")
        
        return "".join(parts)
    
    def update_preview(self):
        """プレビューテキストを更新"""
        try:
            delay = int(self.delay_var.get())
            repeat = int(self.repeat_var.get())
            interval = float(self.repeat_interval_var.get())
            key = self.key_var.get()
            
            time_str = self.format_time(delay)
            
            if repeat == 1:
                preview = f"{time_str}後に、{key}キーを1回押します"
            else:
                preview = f"{time_str}後に、{interval}秒ごとに{repeat}回{key}キーを押します"
            
            self.preview_var.set(preview)
        except ValueError:
            self.preview_var.set("入力値を確認してください")
    
    
    def get_key(self, key_name):
        """文字列からpynputのKeyオブジェクトを取得"""
        key_map = {
            'Enter': Key.enter,
            'Space': Key.space,
            'Tab': Key.tab,
            'Esc': Key.esc,
        }
        return key_map.get(key_name, key_name)
    
    def validate_inputs(self):
        """入力値の検証"""
        try:
            delay = int(self.delay_var.get())
            repeat = int(self.repeat_var.get())
            repeat_interval = float(self.repeat_interval_var.get())
            
            if delay < 0 or repeat < 1 or repeat_interval < 0:
                raise ValueError("値が不正です")
            
            return delay, repeat, repeat_interval
        except ValueError as e:
            messagebox.showerror("入力エラー", f"正しい数値を入力してください\n{str(e)}")
            return None
    
    def automation_thread(self, delay, repeat, repeat_interval):
        """自動化処理のスレッド"""
        try:
            # 開始までの遅延（時分秒表示）
            remaining = int(delay)
            while remaining > 0:
                if self.stop_event.is_set():
                    return
                
                hours = remaining // 3600
                minutes = (remaining % 3600) // 60
                seconds = remaining % 60
                
                if hours > 0:
                    self.status_var.set(f"開始まで {hours}時間{minutes}分{seconds}秒")
                elif minutes > 0:
                    self.status_var.set(f"開始まで {minutes}分{seconds}秒")
                else:
                    self.status_var.set(f"開始まで {seconds}秒")
                
                time.sleep(1)
                remaining -= 1
            
            key = self.get_key(self.key_var.get())
            
            # 繰り返し実行
            for rep in range(repeat):
                if self.stop_event.is_set():
                    break
                
                self.status_var.set(f"実行中... ({rep + 1}/{repeat})")
                
                # キーを1回押す
                self.keyboard.press(key)
                self.keyboard.release(key)
                
                # 次の繰り返しまで待機
                if rep < repeat - 1:
                    time.sleep(repeat_interval)
            
            if not self.stop_event.is_set():
                self.status_var.set("完了")
                messagebox.showinfo("完了", "キー押下が完了しました")
            else:
                self.status_var.set("停止されました")
        
        except Exception as e:
            self.status_var.set("エラー")
            messagebox.showerror("エラー", f"実行中にエラーが発生しました:\n{str(e)}")
        
        finally:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def start_automation(self):
        """自動化を開始"""
        if self.is_running:
            return
        
        values = self.validate_inputs()
        if values is None:
            return
        
        self.is_running = True
        self.stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        thread = Thread(target=self.automation_thread, args=values, daemon=True)
        thread.start()
    
    def stop_automation(self):
        """自動化を停止"""
        self.stop_event.set()
        self.status_var.set("停止中...")

def main():
    root = tk.Tk()
    app = PressEnterLaterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
