#Accepts a barycenter relative to the solar barycenter and the coordinates of moons relative to the parent body
#The barycenter must be assigned the mass parameter of the parent body.
def find_center_body(bary,delta,MPcenter,MPorbital):
    return bary-(delta*MPorbital/(MPcenter+MPorbital))
infile=input("Enter filename:")
with open(infile) as f:
    bary=None
    #moons=[]
    moon=None
    for line in f:
        numline = [float(n) for n in line.split(",")]
        if bary is None:
            bary=numline
        else:
            #moons.append(numline)
            moon=numline
'''body=[]
for n in range(6):
    for moon in moons:
        body.append()'''
body=[]
moon_out=[]
for n in range(6):
    body.append(find_center_body(bary[n],moon[n],bary[6],moon[6]))
    moon_out.append(body[n]+moon[n])

print(body)
print(moon_out)


