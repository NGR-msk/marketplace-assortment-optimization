# ============================================
# ФАЙЛ 3: parse_ozon_economics.py
# ============================================
import pandas as pd
import glob
import os
import re

INPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Материалы\OZON\Юнит-экономика'
OUTPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Output'

def clean_number(x):
    if pd.isna(x):
        return 0.0
    try:
        return float(str(x).replace(' ₽', '').replace('\xa0', '').replace(' ', '').replace(',', '.'))
    except:
        return 0.0

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    files = glob.glob(os.path.join(INPUT_DIR, '*.xlsx'))
    if not files:
        print(f"❌ Файлы не найдены в {INPUT_DIR}")
        return
    
    print(f"📁 Найдено файлов: {len(files)}")
    
    all_dfs = []
    for file in files:
        match = re.search(r'(\d{2}\.\d{2}\.\d{4})', os.path.basename(file))
        period = match.group(1) if match else 'Неизвестно'
        
        df = pd.read_excel(file, header=3)
        df['Период'] = period
        all_dfs.append(df)
        print(f"✅ {os.path.basename(file)} → {period}")
    
    df_all = pd.concat(all_dfs, ignore_index=True)
    
    # Чистим числовые колонки
    numeric_cols = [c for c in df_all.columns if c not in ['SKU', 'Артикул', 'Название товара', 
                                                           'Схема работы', 'Период', 'Индекс цен', 
                                                           'Доступность товаров', 'Рекомендации']]
    for col in numeric_cols:
        df_all[col] = df_all[col].apply(clean_number)
    
    filepath = os.path.join(OUTPUT_DIR, 'ozon_economics.csv')
    df_all.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"\n💾 {filepath} ({len(df_all)} строк)")

if __name__ == "__main__":
    main()