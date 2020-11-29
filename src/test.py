from ukkonen import SuffixTree
from modules import CheckSubString

"""s = "abcabxabcd$"
tree = SuffixTree(s)
tree.build_suffix_tree()
a = CheckSubString(tree, 'abc', findall=True)
print(a.check())"""


def cal_freq(S,L):
	f = []
	tree = SuffixTree(S)
	tree.build_suffix_tree()	
	n=len(S)
	for i in range(0,n-L+1):
		string = S[i:i+L]
		# print('string is', string)
		#print(string)
		a = CheckSubString(tree, string, findall=True)
		# t=a.check()
		# print(t)
		# print()
		f.append(len(a.check()))
	
	#print(f)
	return f

# S="ABCDEEBCADgxABCDEEBCADfeEBCADABCDEwwCDEEBCere"
# cal_freq(S,4)