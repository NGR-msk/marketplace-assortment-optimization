import pandas as pd
import glob
import os
import re

INPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Материалы\Маркет\Доп информация'
OUTPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Output'

def clean_rub(x):
    if pd.isna(x):
        return 0.0
    try:
        return float(str(x).replace(' ₽', '').replace('\xa0', '').replace(' ', '').replace(',', '.'))
    except:
        return 0.0

def clean_column_names(df):
    """Убирает суффиксы .8, .7 и т.д., обрабатывает дубликаты"""
    new_columns = []
    col_counts = {}
    
    for col in df.columns:
        # Убираем суффиксы типа .8, .7, .1 и т.д.
        cleaned = re.sub(r'\.\d+$', '', str(col))
        
        # Если колонка уже встречалась, добавляем счетчик
        if cleaned in col_counts:
            col_counts[cleaned] += 1
            cleaned = f"{cleaned}_{col_counts[cleaned]}"
        else:
            col_counts[cleaned] = 0
        
        new_columns.append(cleaned)
    
    df.columns = new_columns
    return df

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    files = [f for f in glob.glob(os.path.join(INPUT_DIR, '*.xlsx'))
             if not os.path.basename(f).startswith('~$')]
    
    if not files:
        print(f"❌ Файлы не найдены в {INPUT_DIR}")
        return
    
    print(f"📁 Найдено файлов: {len(files)}")
    
    all_transactions = []
    all_margin = []
    
    for i, file in enumerate(files, 1):
        filename = os.path.basename(file)
        print(f"\n[{i}/{len(files)}] 📄 {filename}")
        
        try:
            xls = pd.ExcelFile(file)
            sheets = xls.sheet_names
        except Exception as e:
            print(f"   ❌ Ошибка открытия: {e}")
            continue
        
        # ЛИСТ 1: Транзакции
        if 'Транзакции по заказам и товарам' in sheets:
            print(f"   🔄 Читаю транзакции...")
            try:
                df_t = pd.read_excel(file, sheet_name='Транзакции по заказам и товарам', header=8)
                
                # Чистим заголовки от суффиксов и дубликатов
                df_t = clean_column_names(df_t)
                
                # Удаляем полностью пустые колонки
                # df_t = df_t.dropna(axis=1, how='all')
                
                if 'Ваш SKU' in df_t.columns:
                    df_t = df_t[df_t['Ваш SKU'].notna()]
                    df_t = df_t[df_t['Ваш SKU'].astype(str).str.strip() != '']
                
                # df_t['Источник_файл'] = filename
                all_transactions.append(df_t)
                print(f"   ✅ Транзакции: {len(df_t)} строк, {len(df_t.columns)} колонок")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
        
        # ЛИСТ 2: Маржа
        if 'Услуги и маржа по заказам' in sheets:
            print(f"   🔄 Читаю маржу...")
            try:
                df_m = pd.read_excel(file, sheet_name='Услуги и маржа по заказам', header=6)
                
                # Чистим заголовки
                df_m = clean_column_names(df_m)
                df_m = df_m.dropna(axis=1, how='all')
                
                if 'Ваш SKU' in df_m.columns:
                    df_m = df_m[df_m['Ваш SKU'].notna()]
                    df_m = df_m[df_m['Ваш SKU'].astype(str).str.strip() != '']
                
                # df_m['Источник_файл'] = filename
                all_margin.append(df_m)
                print(f"   ✅ Маржа: {len(df_m)} строк, {len(df_m.columns)} колонок")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")
    
    # Объединяем
    if all_transactions:
        print(f"\n🔄 Объединяю транзакции...")
        # Используем join='outer' для объединения всех колонок
        df_transactions = pd.concat(all_transactions, ignore_index=True, sort=False)
        
        for col in df_transactions.columns:
            col_str = str(col).lower()
            if '₽' in str(col) or 'сумма' in col_str or 'цена' in col_str or 'скидка' in col_str or 'оплата' in col_str or 'балл' in col_str:
                df_transactions[col] = df_transactions[col].apply(clean_rub)
        
        filepath1 = os.path.join(OUTPUT_DIR, 'market_transactions.csv')
        df_transactions.to_csv(filepath1, index=False, encoding='utf-8-sig')
        print(f"💾 {filepath1} ({len(df_transactions)} строк)")
    
    if all_margin:
        print(f"\n🔄 Объединяю маржу...")
        df_margin = pd.concat(all_margin, ignore_index=True, sort=False)
        
        for col in df_margin.columns:
            col_str = str(col).lower()
            if '₽' in str(col) or 'сумма' in col_str or 'цена' in col_str or 'доход' in col_str:
                df_margin[col] = df_margin[col].apply(clean_rub)
        
        filepath2 = os.path.join(OUTPUT_DIR, 'market_margin.csv')
        df_margin.to_csv(filepath2, index=False, encoding='utf-8-sig')
        print(f"💾 {filepath2} ({len(df_margin)} строк)")
    
    print("\n✅ ГОТОВО!")

if __name__ == "__main__":
    main()