''' Andrew Henshaw
    based on
       Boris Borcic 2006
       Quick and concise Python 2.5 sudoku solver
    but faster
'''
import sys

w2q = [[n/9, n/81*9+n%9+81, n%81+162, n%9*9+n/243*3+n/27%3+243] for n in xrange(729)]
q2w = []
for y, (s0, s1, s2, s3) in enumerate(w2q):
	q2w += [(s0, y), (s1, y), (s2, y),(s3, y)]
q2w = (z[1] for z in sorted(q2w))
q2w = map(set,zip(*9*[q2w]))
w2q2w = [(q2w[q0] | q2w[q1] | q2w[q2] | q2w[q3]) for q0, q1, q2, q3 in w2q]

def search(w0s,q2nw,takens,ws) :
    w0s_app = w0s.append
    w0s_pop = w0s.pop
    t_add   = takens.add
    ws_add  = ws.add
    q2nw_index = q2nw.index
    while True:
        while w0s:
            w0 = w0s_pop()
            t_add(w0)
            ws_add(w0)
            q0, q1, q2, q3 = w2q[w0]
            q2nw[q0] +=100
            q2nw[q1] +=100
            q2nw[q2] +=100
            q2nw[q3] +=100
            
            for w in w2q2w[w0] - takens :
                t_add(w)
                q0, q1, q2, q3 = w2q[w]
                
                n = q2nw[q0] = q2nw[q0]-1
                if n<2 :
                    w0s_app((q2w[q0]-takens).pop())
                    
                n = q2nw[q1] = q2nw[q1]-1
                if n<2 :
                    w0s_app((q2w[q1]-takens).pop())
                    
                n = q2nw[q2] = q2nw[q2]-1
                if n<2 :
                    w0s_app((q2w[q2]-takens).pop())
                    
                n = q2nw[q3] = q2nw[q3]-1
                if n<2 :
                    w0s_app((q2w[q3]-takens).pop())
        if len(ws)==81 :
            raise Exception(ws)
        w1,w0 = q2w[q2nw_index(2)]-takens 
        try : search([w1],q2nw[:],takens.copy(),ws.copy())
        except KeyError : 
            w0s_app(w0)
givens = [9*j+int(k)-1 for j,k in enumerate(sys.argv[1]) if '0'<k]
try :
    search(givens,[9]*len(q2w),set(),set())
except Exception, e :
    print ''.join(str(w%9+1) for w in sorted(e.message))
