import sys, exp3, exp3_fix
exp3.run_team('fix', exp3_fix.ALLV['pacote de correções'], int(sys.argv[1]) if len(sys.argv) > 1 else 12000, 101)
