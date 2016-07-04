def fib (n):    
    u=[1,1]
    for i in range (n-1):
        u.append (u[i+1]+u[i])
    print (u)
    