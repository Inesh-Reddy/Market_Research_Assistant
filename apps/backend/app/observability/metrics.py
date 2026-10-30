# Lightweight counters; extend with Prometheus when needed.
counters: dict[str,int]={}
def inc(name: str): counters[name]=counters.get(name,0)+1
