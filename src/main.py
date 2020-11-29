from ukkonen import SuffixTree
from modules import CheckSubString
from test import cal_freq
from time import time
import numpy as np
from matplotlib import pyplot as plt
from threading import Thread as th

D=[]
l=[]
r=[]
tree = None
s = 0
def RepSeeker(S,L,Fm):
	global l, r, D, s
	f = cal_freq(S,L)
	# print(f)
	if (f[0]>=Fm):
		l.append(0)
	n=len(S)
	for i in range(1,n-L):
		if(f[i]>=Fm):
			if(f[i]!=f[i-1]):
				l.append(i)
			if(f[i]!=f[i+1]):
				r.append(i+L) #exclusive

	# print('len l',len(l))
	# print('len r', len(r))
	if len(l) != len(r):
		r.append(len(S))
	# print(len(l), len(r))
	for i in range(0,len(l)):
		D.append((l[i], r[i]))
	s = len(D)
	# print(D)
	# print("Starting Check")
	Check(f,L,S)
	# print("Starting Extend")
	Extend(f,L,S,Fm)
	#print("Starting Classify")
	return Classify(f,L,S,Fm)

def get_substring(S, D):
	return S[D[0]:D[1]]

# Definition 3 A is an elementary repeat of S, if A is a
# nontrivial substring of S with the maximal length, A occurs
# in S at least F m times, and every nontrivial substring of A is a
# subrepeat of A. F m is a specified lowest frequency of
# occurrences of repeats.

def Check(f,L,S):
	global l, r, D, s
	# print("started check, number of strings",s)

	# s = no. of those substrings in the sequence whose frequency >= Fm

	for i in range(s): # running on all substrings

		# starting position of all unique substrings of s[i]
		a = CheckSubString(tree, get_substring(S, D[i]), findall=True).check()
		# print('a', get_substring(S, D[i]), a)

		fD=len(a) # taken out from suffix tree frequency of all unique of substrings of s[i] taken from suffix tree
	
		# print(">>>check",i,fD, a, get_substring(S, D[i]))
		# print('li', l[i], len(f))
		if (f[l[i]])!=fD: # k < m
			P = []
			for j in range(D[i][0], D[i][1] - L + 1):
				string = get_substring(S,(j, j+L))
				b = CheckSubString(tree, string, findall=True).check()
				b.sort()
				# print('b', string, b)
				P.append(b)
				# n=len(S)
				# for z in range(0,n-):
				# 	string = get_substring(S, (D[i][0] + z, D[i][0] + z + L))
				# 	print('string',string)
				# 	b = CheckSubString(tree, string, findall=True).check()
				# 	print('tree', b)
				# 	b.sort()
				# 	P.append(b)
					
			for k in range(0, D[i][1] - D[i][0] - L):
				for m in range(min(len(P[k]), len(P[k+1]))):
					P[k+1]
					P[k]
					if(P[k+1][m]!=P[k][m]+1):
						l.append(l[i]+k)
						r.append(l[i]+k+L)
						if (l[-1], r[-1]) not in D:
							D.append((l[-1], r[-1]))
							s += 1
						else:
							l.pop()
							r.pop()
			# print('--------------',len(l), len(r))

def merop(S,i):
	global D
	l1=D[i-1][0]
	r1=D[i-1][1]
	l2=D[i][0]
	r2=D[i][1]
	# print('merop', l1, r1, l2, r2)
	if l1 > l2:
		l1, r1, l2, r2 = l2, r2, l1, r1
	if l1 == l2 and r1 > r2:
		r1, r2 = r2, r1
	if l2 > r1:
		return 0
	else:
		return 100 

def fre(S,i,Fm):
	global D
	l1=D[i-1][0]
	r1=D[i-1][1]
	l2=D[i][0]
	r2=D[i][1]
	if l1 > l2:
		l1, r1, l2, r2 = l2, r2, l1, r1
	strAuB=S[l1:r2]
	# tree = SuffixTree(S)
	# tree.build_suffix_tree()
	a = CheckSubString(tree, strAuB, findall=True).check()
	fD=len(a)
	if(fD>=Fm):
		return 1
	else:
		return 0



def Extend(f,L,S,Fm):
	global l, r, D, s
	D.sort()

	#print("VALUE OF SUM IN EXTEND:",sum)
	i = 1
	p = []
	# for x in range(len(D)):
		# print(x, D[x])

	for i in range(1,len(D)):
		if merop(S,i)>=25 and fre(S,i,Fm):
			# print('#######', D[i-1], D[i])
			# print('before merge ', i , get_substring(S,D[i-1]), get_substring(S, D[i]), D[i-1], D[i])
			D[i] = (D[i-1][0], D[i][1])
			# print('merged length', i , get_substring(S, D[i]))


def Classify(f,L,S,Fm):
	global l, r, D, s
	classes=[]
	longest_str_length=0
	longest_str = None
	longest_str_occ = None
	for i in range(len(D)):
		string = get_substring(S, D[i])
		b = len(CheckSubString(tree, string, findall=True).check())
		if b < Fm:
			continue
		classes.append(string)
		str_length = D[i][1] - D[i][0]
		if(str_length>=longest_str_length):
			longest_str_length=str_length
			longest_str = string
		longest_str_occ = CheckSubString(tree, string, findall=True).check()
	return (longest_str, longest_str_length, longest_str_occ)


# with open('data1.txt','r') as f:
# 	mainstring=f.read()

# tree = SuffixTree(mainstring)
# tree.build_suffix_tree()
# print("length of longest sequence",RepSeeker(mainstring,20,3))

def rep_timer(file_name, win_l=20):
	global l, r, D, s, tree
	l, r, D, s, tree = [], [], [], 0, None
	with open(file_name, 'r') as f:
		mainstring = f.read()
	tree = SuffixTree(mainstring)
	tree.build_suffix_tree()
	t = time()
	print('For window length :',end = " ")
	print(win_l)
	print("Length of longest sequence",RepSeeker(mainstring, win_l, 3))
	t = time() - t
	print('Done processing in', t, 'seconds')
	return t

data_file = 'data3.txt'

def plotter():
    x = [i for i in range(6, 15)]
    # print('--x done')
    y = [rep_timer(data_file, i) for i in x]
    # print('-- y done')

    plt.title('')
    plt.xlabel('window length')
    plt.ylabel('')
    plt.plot(x, y, label='Time -v/s- Window size')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad = 0.0)
    plt.show()


if __name__ == '__main__':
	rep_timer('data3.txt')
	plotter()
