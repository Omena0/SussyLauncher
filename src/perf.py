import os
import cProfile

try: os.rename('SussyLauncher V1.7.pyw','PerfAnalysis.pyw')
except: pass

profiler = cProfile.Profile()

p = profiler.run('import PerfAnalysis')

p.dump_stats('perf_analysis.dmp')

os.rename('PerfAnalysis.pyw','SussyLauncher V1.7.pyw')

os.system('snakeviz perf_analysis.dmp')