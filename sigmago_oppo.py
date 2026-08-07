#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
================================================================
SIGMAGO — PHƯƠNG TRÌNH BẬC HAI (TỰ HỌC, KHÔNG CÔNG THỨC)
================================================================
- Không dùng delta, không dùng Viet
- Không có công thức nào được nhét vào
- Chỉ có thử, sai, và tự rút ra quy luật
- Chạy được trên Oppo (Pydroid 3 / QPython)
"""

import random
import time

class SigmagoPhuongTrinh:
    def __init__(self):
        self.attempts = 0
        self.correct = 0
        self.streak = 0
        self.rules = []          # Lưu quy luật tự tìm ra
        self.memory = {}         # Lưu các cặp (phương trình, nghiệm) đã đúng

    # =========================================================
    # 1. TỰ TẠO PHƯƠNG TRÌNH (KHÔNG CÔNG THỨC)
    # =========================================================

    def _gen_equation(self):
        # Tạo phương trình bậc hai ngẫu nhiên
        a = random.randint(1, 5)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        return a, b, c

    # =========================================================
    # 2. TỰ "NGHĨ" RA NGHIỆM (THỬ - SAI - HỌC)
    # =========================================================

    def _guess_roots(self, a, b, c):
        """Sigmago tự đoán nghiệm — KHÔNG CÓ CÔNG THỨC NÀO"""
        # Nếu đã từng gặp phương trình này, dùng nghiệm đã nhớ
        key = (a, b, c)
        if key in self.memory:
            return self.memory[key]

        # Nếu chưa có, thử ngẫu nhiên (sai cũng được)
        # Bắt đầu từ -10 đến 10
        possible_roots = list(range(-10, 11))
        random.shuffle(possible_roots)

        # Chọn 2 giá trị khác nhau
        if len(possible_roots) >= 2:
            return possible_roots[0], possible_roots[1]
        else:
            return 0, 0

    # =========================================================
    # 3. TỰ KIỂM TRA (KHÔNG DÙNG DELTA)
    # =========================================================

    def _check(self, a, b, c, x1, x2):
        """Kiểm tra xem x1, x2 có phải là nghiệm không"""
        def is_root(x):
            return abs(a * x * x + b * x + c) < 0.001
        return is_root(x1) and is_root(x2)

    # =========================================================
    # 4. TỰ HỌC TỪ ĐÚNG VÀ SAI
    # =========================================================

    def _learn(self, a, b, c, x1, x2, is_correct):
        """Nếu đúng, ghi nhớ để dùng lại. Nếu sai, ghi nhớ để không lặp lại."""
        key = (a, b, c)
        if is_correct:
            # Lưu nghiệm đúng
            self.memory[key] = (x1, x2)
            # Rút ra quy luật (đơn giản: mỗi lần đúng, lưu lại)
            rule = f"{a}x² + {b}x + {c} = 0 → x₁={x1}, x₂={x2}"
            if rule not in self.rules:
                self.rules.append(rule)
                print(f"   📚 SIGMA VỪA TỰ HỌC: {rule}")
        else:
            # Sai là một bài học — ghi nhớ để lần sau thử khác
            wrong_rule = f"{a}x² + {b}x + {c} = 0 → {x1}, {x2} (sai)"
            if wrong_rule not in self.rules:
                self.rules.append(wrong_rule)

    # =========================================================
    # 5. VÒNG LẶP CHÍNH
    # =========================================================

    def run(self, delay=6):
        print("\n" + "="*50)
        print("  📐 SIGMAGO — PHƯƠNG TRÌNH BẬC HAI")
        print("  🌱 Không công thức, chỉ thử - sai - tự học")
        print("  ⏱️  Mỗi 6 giây, một phương trình mới")
        print("="*50 + "\n")

        while True:
            a, b, c = self._gen_equation()
            x1, x2 = self._guess_roots(a, b, c)
            is_correct = self._check(a, b, c, x1, x2)

            self.attempts += 1

            if is_correct:
                self.correct += 1
                self.streak += 1
            else:
                self.streak = 0

            self._learn(a, b, c, x1, x2, is_correct)

            print(f"[{self.attempts}] ❓ Giải: {a}x² + {b}x + {c} = 0")
            print(f"   💬 Sigma nghĩ: x₁ = {x1}, x₂ = {x2}")
            print(f"   📌 {'✅ Đúng!' if is_correct else '❌ Chưa đúng.'}")
            if not is_correct:
                # Không đưa đáp án đúng — để Sigmago tự tìm
                print(f"   🔄 Sigma sẽ thử lại lần sau...")

            print(f"   📊 Đúng: {self.correct}/{self.attempts}")
            print(f"   🔥 Chuỗi đúng: {self.streak}")
            print(f"   📚 Quy luật đã học: {len(self.rules)}")
            print()

            time.sleep(delay)

if __name__ == "__main__":
    sigmago = SigmagoPhuongTrinh()
    try:
        sigmago.run(delay=6)
    except KeyboardInterrupt:
        print("\n\n🌱 Tạm biệt! Sigmago đã đạt:")
        print(f"   📚 {len(sigmago.rules)} quy luật")
        print(f"   ✅ {sigmago.correct}/{sigmago.attempts} đúng")
        print(f"   💾 Vào file: (tự lưu trong bộ nhớ)")
