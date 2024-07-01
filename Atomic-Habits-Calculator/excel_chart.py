import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Funcție pentru citirea și pregătirea datelor
def read_and_prepare_data(file_path, sheet_name='Foaie1'):
    try:
        # Citirea datelor din fișierul Excel
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

        # Conversia coloanei 'Data' la tipul datetime
        df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y', errors='coerce')

        # Verificare dacă există valori neconforme în coloana 'Data'
        if df['Data'].isnull().any():
            raise ValueError("Există valori neconforme în coloana 'Data'. Verifică formatul datelor în fișierul Excel.")

        # Înlocuirea 'X' cu 1 și valorile lipsă cu 0 pentru coloanele numerice
        columns_to_replace = df.columns.drop('Data')  # Excludem coloana 'Data' din înlocuire
        df[columns_to_replace] = df[columns_to_replace].replace({'X': 1, np.nan: 0})

        return df

    except FileNotFoundError:
        print(f"Fișierul '{file_path}' nu a fost găsit.")
    except ValueError as ve:
        print(f"Eroare la citirea fișierului Excel: {ve}")
    except Exception as e:
        print(f"Eroare neașteptată: {str(e)}")
    return None

# Funcție pentru vizualizarea progresului zilnic
def plot_daily_progress(df_filtered):
    # Calcularea sumelor pe zile
    df_daily = df_filtered.set_index('Data').resample('D').sum()

    # Calcularea progresului zilnic cu 1% conform principiilor din Atomic Habits
    plt.figure(figsize=(14, 8))
    for col in df_daily.columns:
        cumulative_sum = df_daily[col].cumsum()  # Suma cumulată pe zi
        target = cumulative_sum.max() * 1.01  # 1% mai mult decât maximul acumulat
        plt.plot(cumulative_sum.index, cumulative_sum, marker='o', label=col)
        plt.plot([df_daily.index.min(), df_daily.index.max()], [target, target], 'r--', label=f'1% growth line - {col}')

        # Identificarea perioadelor fără activitate
        inactive_periods = cumulative_sum[cumulative_sum == 0].index
        if not inactive_periods.empty:
            plt.plot(inactive_periods, [0]*len(inactive_periods), 'gx', label=f'No activity - {col}')

    plt.title(f"Progresul zilnic cu 1% creștere zilnică")
    plt.xlabel('Dată')
    plt.ylabel('Sumă cumulată')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Funcție pentru vizualizarea progresului săptămânal
def plot_weekly_progress(df_filtered):
    # Calcularea sumelor pe săptămâni
    df_weekly = df_filtered.resample('W-Mon', on='Data').sum()

    # Afișarea progresului pe săptămâni
    plt.figure(figsize=(12, 8))
    for activity in df_weekly.columns:
        plt.plot(df_weekly.index, df_weekly[activity], marker='o', label=activity)

        # Identificarea săptămânilor fără activitate
        inactive_weeks = df_weekly[df_weekly[activity] == 0].index
        if not inactive_weeks.empty:
            plt.plot(inactive_weeks, [0]*len(inactive_weeks), 'gx', label=f'No activity - {activity}')

    plt.title('Progres săptămânal')
    plt.xlabel('Dată')
    plt.ylabel('Număr activități')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Funcție pentru heatmap-ul de corelații
def plot_correlation_heatmap(df):
    # Heatmap pentru corelații între activități
    plt.figure(figsize=(10, 8))
    corr = df.drop(columns=['Data']).corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))  # Masca pentru a ascunde jumătatea de jos a matricei
    sns.heatmap(corr, annot=True, cmap='YlGnBu', linewidths=0.5, mask=mask, cbar=True,
                annot_kws={"size": 8})  # Am redus dimensiunea textului pentru a face descrierile mai clare
    plt.title('Corelații între activități\n'
              'Valorile de corelație: '
              '0.4 și mai mare: Corelație moderată până la puternică, '
              '0.2 - 0.4: Corelație slabă până moderată, '
              'sub 0.2: Corelație foarte slabă sau inexistentă', fontsize=12)
    plt.show()

if __name__ == "__main__":
    file_path = 'data.xlsx'
    df = read_and_prepare_data(file_path)
    if df is not None:
        plot_daily_progress(df)
        plot_weekly_progress(df)
        plot_correlation_heatmap(df)
