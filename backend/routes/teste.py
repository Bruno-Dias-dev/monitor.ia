from datetime import date, timedelta

hoje = date.today()

inicio_semana = hoje - timedelta(days=hoje.weekday())
fim_semana = inicio_semana + timedelta(days=7)

print(inicio_semana, fim_semana)