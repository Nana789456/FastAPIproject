visits = ["user123", "user456", "user123", "user789", 
          "user456", "user123", "user999", "user456", "user123"]


visit_counts = {}
for visit in visits:
    visit_counts[visit] = visit_counts.get(visit, 0) + 1 # если такого ключа нет, то методget вернет 0
print(visit_counts)

active_visitors = max(visit_counts, key=visit_counts.get)
print(active_visitors)
