# ============================================
# ФАЙЛ 2: parse_market_funnel.py
# ============================================
import pandas as pd
import glob
import os
import re

INPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Материалы\Маркет\Аналитика продаж'
OUTPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Output'

def extract_month(filename):
    month_map = {
        'январь': '01', 'февраль': '02', 'март': '03', 'апрель': '04',
        'май': '05', 'июнь': '06', 'июль': '07', 'август': '08',
        'сентябрь': '09', 'октябрь': '10', 'ноябрь': '11', 'декабрь': '12'
    }
    match = re.search(r'(\w+)\s+(\d{4})', filename)
    if match:
        month = month_map.get(match.group(1).lower(), '00')
        return f"01.{month}.{match.group(2)}"
    return None

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    files = glob.glob(os.path.join(INPUT_DIR, '*.xlsx'))
    if not files:
        print(f"❌ Файлы не найдены в {INPUT_DIR}")
        return
    
    print(f"📁 Найдено файлов: {len(files)}")
    
    all_dfs = []
    for file in files:
        period = extract_month(os.path.basename(file))
        df = pd.read_excel(file)
        df['Период'] = period
        all_dfs.append(df)
        print(f"✅ {os.path.basename(file)} → {period}")
    
    df_all = pd.concat(all_dfs, ignore_index=True)
    filepath = os.path.join(OUTPUT_DIR, 'market_funnel.csv')
    df_all.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"\n💾 {filepath} ({len(df_all)} строк)")

if __name__ == "__main__":
    main()