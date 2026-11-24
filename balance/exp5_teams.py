import sys, exp3, exp4_classes as C, exp4_teams_specs as SP
label, which, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
exp3.run_team(label, SP.SPECS[which], n, 101)
