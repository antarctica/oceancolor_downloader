l = []
lower = 1
higher = 8
for x in range(0, 46):
	l2 = []
	
	for y in range(lower,higher +1):
		l2.append(y)
	l.append(l2)
	lower = lower + 8
	higher = higher + 8
print l



