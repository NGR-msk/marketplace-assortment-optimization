import pandas as pd
import glob
import os

INPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Материалы\OZON\Отчет по товарам'
OUTPUT_DIR = r'D:\Projects\Мастерская\DonorSearch\Output'

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Находим все xlsx файлы, игнорируя временные ~$
    files = [f for f in glob.glob(os.path.join(INPUT_DIR, '*.xlsx'))
             if not os.path.basename(f).startswith('~$')]
    
    if not files:
        print(f"❌ Файлы не найдены в {INPUT_DIR}")
        return
    
    print(f"📁 Найдено файлов: {len(files)}")
    for f in files:
        print(f"   - {os.path.basename(f)}")
    
    all_dfs = []
    
    for i, file in enumerate(files, 1):
        filename = os.path.basename(file)
        print(f"\n[{i}/{len(files)}] 📄 {filename}")
        
        try:
            df = pd.read_excel(file)
            # df['Источник_файл'] = filename
            all_dfs.append(df)
            print(f"   ✅ Прочитано: {len(df)} строк, {len(df.columns)} колонок")
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
    
    if not all_dfs:
        print("\n❌ Не удалось прочитать ни одного файла")
        return
    
    print(f"\n🔄 Объединяю {len(all_dfs)} файлов...")
    df_combined = pd.concat(all_dfs, ignore_index=True)
    
    print(f"✅ Итого: {len(df_combined)} строк, {len(df_combined.columns)} колонок")
    
    # Сохраняем ВСЁ без фильтрации
    filepath = os.path.join(OUTPUT_DIR, 'ozon_reports_by_goods.csv')
    df_combined.to_csv(filepath, index=False, encoding='utf-8-sig')
    
    print(f"\n💾 Сохранено: {filepath}")


if __name__ == "__main__":
    main()