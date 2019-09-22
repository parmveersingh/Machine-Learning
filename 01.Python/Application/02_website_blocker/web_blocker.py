q=open("/etc/hosts","r").readlines()
wrt= open("/etc/hosts","a")
if q[-1] != "127.0.1.1       www.facebook.com":
     wrt.write("127.0.1.1       www.facebook.com")
print(q[-1])
