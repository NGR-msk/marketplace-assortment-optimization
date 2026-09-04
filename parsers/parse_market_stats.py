# ============================================
# ФАЙЛ 1: parse_market_stats.py
# ============================================
import pandas as pd
import glob
import os

# ПУТИ (ЗАХАРдкожены)
INPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Материалы\Маркет\Объединенная статистика'
OUTPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Output'

# Листы для обработки
SHEETS = [
    'Товары, переданные в доставку',
    'Доставленные товары',
    'Невыкупленные товары',
    'Возвращенные товары'
]

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    files = glob.glob(os.path.join(INPUT_DIR, '*.xlsx'))
    if not files:
        print(f"❌ Файлы не найдены в {INPUT_DIR}")
        return
    
    print(f"📁 Найдено файлов: {len(files)}")
    
    all_data = {sheet: [] for sheet in SHEETS}
    
    for file in files:
        print(f"\n📄 {os.path.basename(file)}")
        xls = pd.ExcelFile(file)
        
        for sheet in SHEETS:
            if sheet in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet, header=16)
                # Удаляем строки с "Итого:"
                if 'Номер заказа' in df.columns:
                    df = df[~df['Номер заказа'].astype(str).str.contains('Итого:', na=False)]
                all_data[sheet].append(df)
                print(f"  ✅ {sheet}: {len(df)} строк")
    
    print("\n🔄 Сохраняю CSV...")
    for sheet, dfs in all_data.items():
        if dfs:
            df_combined = pd.concat(dfs, ignore_index=True)
            safe_name = sheet.replace(',', '').replace(' ', '_').lower()
            filepath = os.path.join(OUTPUT_DIR, f'market_{safe_name}.csv')
            df_combined.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"💾 {filepath} ({len(df_combined)} строк)")

if __name__ == "__main__":
    main()