import os

search_term = "notification_list.html"  # 検索する文字列
base_dir = "."  # 現在のディレクトリを基準に検索

for root, dirs, files in os.walk(base_dir):
    for file in files:
        file_path = os.path.join(root, file)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                if search_term in content:
                    print(f"Found in: {file_path}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
