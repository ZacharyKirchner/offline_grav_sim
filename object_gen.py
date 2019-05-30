from random import choices, random, gauss, triangular,choice
from math import sin,cos,tan,sqrt,atan2,atan,fsum,asin,acos

asteroidMassScale={25000000:(10**-12),4000000:2.7*(10**-12),2000000:1.25*(10**-10),750000:(10**-9),200000:2.7*(10**-8),90000:1.25*(10**-7),10000:0.000001,1100:0.000027,600:0.000125,200:0.001,27:0.008} # A dictionary of asteroid numbers and masses relative to Ceres, roughly.
asteroidSMARanges=[[2.1,2.5],[2.5,2.825],[2.825,2.95],[2.95,3.3]]
def generate_object(modeEccentricity,maxEccentricity,massScale,maxGM,maxInc,sma_ranges):
    GM=maxGM*triangular(0.2,5,1)*choices([x for x in iter(massScale.values())],weights=[x for x in iter(massScale.keys())])[0]
    ecc= triangular(0,1.1*maxEccentricity,modeEccentricity)#For the asteroid belt, the max is 0.4 and the mode is 0.07
    inc= gauss(0,maxInc/3)#For the asteroid belt, max inclination is 30 degrees, or about 0.523599 radians
    window=choice(sma_ranges)#pick one of the windows
    sma= gauss((window[1]+window[0])/2,(window[1]-window[0])/6 )#picks a sma in the window selected, using a gaussian distribution. This is probably not very accurate.
    anomaly=random()*6.28
    argPeriapsis=random()*6.28
    longAN=random()*6.28
    return (ecc,GM,inc,sma,anomaly,argPeriapsis,longAN)


#def generate_population(maxEccentricity,massScale,maxMass,maxInclination):
def get_ecliptic(t):
    return 0.408407 #23.4 degrees in radians
def orbit_convert(eccentricity,massParam,inclination,sma,anomaly,argPeriapsis,longAN,anomType="e",GMsun=0.000295912):
    #Takes kepler parameters of orbit and produces ecliptic coordinates
    if anomType=="e":
        eccAnomaly=anomaly
        meanAnomaly=eccAnomaly-eccentricity*sin(eccAnomaly)
        trueAnomaly=2*atan(sqrt((1+eccentricity)/(1-eccentricity))*tan(eccAnomaly/2))
        radius = sma * (1 - eccentricity * cos(eccAnomaly))
    #elif anomType=="t":
        #Eccentric Anomaly is currently preferred. Mean anomaly cannot yet be calculated from true anomaly but is necessary for calculations
    #    trueAnomaly=anomaly
    #    radius = sma * (1 - eccentricity * eccentricity) / (1 + eccentricity * cos(trueAnomaly))
    else:
        raise Exception("Sorry, Mean and True Anomaly are not accepted at this time")
    #radius=sma*(1-eccentricity*eccentricity)/(1+eccentricity*cos(trueAnomaly))
    semi_minor=sma*sqrt(1-eccentricity*eccentricity)
    coords=[[sma*cos(eccAnomaly)],[semi_minor*sin(eccAnomaly)],[0]]
    #v_mag_sq=massParam*((2/radius)-(1/sma))
    print(sma)
    print(massParam)
    period=6.28*sqrt((sma**3)/GMsun)
    ang_vel=(6.28/period)/(1+eccentricity*cos(eccAnomaly))
    #quad_a=1+((semi_minor**4 *coords[0][0]**2)/(sma**4 *coords[1][0]**2))
    #print(quad_a)
    #quad_b=2*(semi_minor**4 *coords[0][0])/(coords[1][0]*sma*sma)
    #print(quad_b)
    #quad_c=(semi_minor**4)/(coords[1][0]**2)
    #v1=quad_b*quad_b-4*quad_a*quad_c
    #print(v1)
    #vx= (-quad_b-sqrt(quad_b*quad_b-4*quad_a*quad_c))/(2*quad_a)
    #val=v_mag_sq-vx*vx
    #print(val)
    #vy= sqrt(v_mag_sq-vx*vx)
    vx= -sma*sin(eccAnomaly)*ang_vel
    vy= semi_minor*cos(eccAnomaly)*ang_vel
    vz=0
    vel_vect=[[vx],[vy],[vz]]
    rot=get_rotation(get_axis(cos(argPeriapsis),sin(argPeriapsis),0),inclination)
    ecliptic_coords=matrix_multiply_3d(rot,coords)
    ecliptic_v=matrix_multiply_3d(rot,vel_vect)
    eq_coords=to_equatorial(ecliptic_coords[0][0],ecliptic_coords[1][0],ecliptic_coords[2][0])
    eq_vel = to_equatorial(ecliptic_v[0][0], ecliptic_v[1][0], ecliptic_v[2][0])
    return [eq_coords,eq_vel,massParam]

def deconvert(x,y,z,vx,vy,vz,GM,GMParent):
    ecliptic_coords=from_equatorial(x,y,z)
    ecliptic_vel=from_equatorial(vx,vy,vz)
    r=sqrt(x*x+y*y+z*z)
    v=sqrt(vx*vx+vy*vy+vz*vz)
    b=asin(z/r)
    l=asin(y/r*cos(b))
    eccAnomaly=asin(x)

def to_equatorial(x,y,z,time=0):
    obliquity=get_ecliptic(time)
    x_equatorial=x
    y_equatorial=(cos(obliquity)*y)-(sin(obliquity)*z)
    z_equatorial=(sin(obliquity)*y)+(cos(obliquity)*z)
    return [x_equatorial,y_equatorial,z_equatorial]
def from_equatorial(x,y,z,time=0):
    obliquity = get_ecliptic(time)
    x_ecliptic = x
    y_ecliptic = (cos(obliquity) * y) + (sin(obliquity) * z)
    z_ecliptic = -(sin(obliquity) * y) + (cos(obliquity) * z)
    return [x_equatorial, y_equatorial, z_equatorial]
def get_axis(x,y,z):
    if int((x**2)+(y**2)+(z**2))==1:
        return [x,y,z]
    mag=sqrt((x ** 2) + (y ** 2) + (z ** 2))
    return [x/mag,y/mag,z/mag]

def get_rotation(axis,angle):
    #creates a rotation matrix for a given axis vector and angle
    #rotates points counterclockwise by angle, or rotates axes clockwise by angle
    a=cos(angle)+(axis[0]**2)*(1-cos(angle))
    b=axis[0]*axis[1]*(1-cos(angle))-axis[2]*sin(angle)
    c=axis[0]*axis[2]*(1-cos(angle))+axis[1]*sin(angle)

    d=axis[0]*axis[1]*(1-cos(angle))+axis[2]*sin(angle)
    e=cos(angle)+axis[1]*axis[1]*(1-cos(angle))
    f=axis[1]*axis[2]*(1-cos(angle))-axis[0]*sin(angle)

    g=axis[0]*axis[2]*(1-cos(angle))-axis[1]*sin(angle)
    h=axis[1]*axis[2]*(1-cos(angle))+axis[0]*sin(angle)
    i=cos(angle)+axis[2]*axis[2]*(1-cos(angle))
    return [[a,b,c],[d,e,f],[g,h,i]]
def matrix_multiply_3d(first_mat,second_mat):
    out_rows=len(first_mat)
    out_cols=len(second_mat[0])
    out_mat=[[fsum([first_mat[r][n]*second_mat[n][c] for n in range(len(second_mat))]) for c in range(out_cols)] for r in range(out_rows)]
    return out_mat
def file_write_coords(filename,objs):
    with open(filename,w) as f:
        for obj in objs:
            o=str(obj[0][0]+","+obj[0][1]+","+obj[0][2]+","+obj[1][0]+","+obj[1][1]+","+obj[1][2]+","+obj[2][0])
            f.write(o)

#asteroid=generate_object(0.07,0.4,asteroidMassScale,0.00000000000014,0.523599,asteroidSMARanges)
#orbit_coords=orbit_convert(asteroid[0],asteroid[1],asteroid[2],asteroid[3],asteroid[4],asteroid[5],asteroid[6])
#print(orbit_coords)
asteroids=[orbit_convert(*generate_object(0.07,0.4,asteroidMassScale,0.00000000000014,0.523599,asteroidSMARanges)) for n in range(100)]

earth=orbit_convert(0.016,0.000000000888769,0,1,0,1.98,-0.191986)
print(earth)