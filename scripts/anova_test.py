import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Генерируем синтетические данные (три группы с разными конверсиями)
np.random.seed(42)

# Группа A: базовая конверсия 10%
group_a = np.random.binomial(1, 0.10, 1000)
# Группа B: конверсия 12%
group_b = np.random.binomial(1, 0.12, 1000)
# Группа C: конверсия 15%
group_c = np.random.binomial(1, 0.15, 1000)

# Собираем в DataFrame
df = pd.DataFrame({
    'group': ['A'] * 1000 + ['B'] * 1000 + ['C'] * 1000,
    'conversion': np.concatenate([group_a, group_b, group_c])
})

print("Средние конверсии по группам:")
print(df.groupby('group')['conversion'].mean())

# 2. Проводим ANOVA
f_stat, p_value = stats.f_oneway(group_a, group_b, group_c)
print(f"\nANOVA: F-статистика = {f_stat:.4f}, p-value = {p_value:.6f}")

if p_value < 0.05:
    print("✅ Разница статистически значима (отвергаем H0)")
else:
    print("❌ Разница статистически не значима (не отвергаем H0)")

# 3. Post-hoc тест (Тьюки)
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukey = pairwise_tukeyhsd(df['conversion'], df['group'], alpha=0.05)
print("\nPost-hoc тест Тьюки:")
print(tukey)

# 4. Визуализация
plt.figure(figsize=(10, 6))
sns.boxplot(x='group', y='conversion', data=df)
plt.title('Сравнение конверсии по группам (A, B, C)')
plt.xlabel('Группа')
plt.ylabel('Конверсия')
plt.savefig('assets/anova_boxplot.png')
plt.show()
