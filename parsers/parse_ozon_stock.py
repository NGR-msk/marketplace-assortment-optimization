import pandas as pd
import os
import re

INPUT_FILE = r'D:\Projects\Мастерская\Материалы\DonorSearch\OZON\Управление остатками\Управление остатками 08.07.2026 16-10.xlsx'
OUTPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Output'

def clean_column_name(col):
    """Чистит название колонки от всех спецсимволов"""
    # Заменяем неразрывный пробел \xa0 на обычный
    col = col.replace('\xa0', ' ')
    # Убираем переносы строк
    col = col.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    # Убираем множественные пробелы
    col = re.sub(r'\s+', ' ', col).strip()
    return col

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("🔄 Читаю файл управления остатками...")
    
    df = pd.read_excel(INPUT_FILE, sheet_name='Товары', header=[0, 1])
    
    # Схлопываем multiindex
    clean_cols = []
    for col in df.columns:
        parts = [str(c) for c in col if 'Unnamed' not in str(c) and str(c) != 'nan']
        clean_name = ' '.join(parts).strip()
        clean_cols.append(clean_name)
    df.columns = clean_cols
    
    # КРИТИЧЕСКИ ВАЖНО: чистим ВСЕ спецсимволы (включая \xa0!)
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # Удаляем служебные строки
    df = df[~df.iloc[:, 0].astype(str).str.contains('Нередактируемое|Номер артикула', na=False)]
    df.rename(columns={df.columns[0]: 'Артикул'}, inplace=True)
    df = df[df['Артикул'].notna() & (df['Артикул'].astype(str).str.strip() != '')]
    df['Артикул'] = df['Артикул'].astype(str).str.strip()
    
    # Приводим числовые колонки к числам
    text_cols = ['Артикул', 'Название товара', 'SKU', 'Признак товара', 'Зона размещения', 'Ликвидность Статус']
    for col in df.columns:
        if col not in text_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Сохраняем
    filepath = os.path.join(OUTPUT_DIR, 'ozon_stock_liquidity.csv')
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    print(f"✅ Сохранено: {filepath}")
    print(f"Строк: {len(df)}, Колонок: {len(df.columns)}")
    
if __name__ == "__main__":
    main()