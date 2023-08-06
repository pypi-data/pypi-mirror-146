import math
import numpy as np
import scipy as sp
import sympy as sym
from sympy.physics.quantum import TensorProduct

def EAtoDCM(seqval, symornum=None, theta1=None, theta2=None, theta3=None):
    # First seperating EA sequence to individual rotations
    rseqval = seqval
    f_rot = int(round(rseqval / 100, 0)) # First rotation
    rseqval = rseqval - (100 * f_rot)
    s_rot = int(round(rseqval / 10, 0)) # Second rotation
    t_rot = int(rseqval - (10 * s_rot)) # Last rotation
    
    # Checking if Thetas are defined
    if (symornum is None) or (symornum == 'sym'):
        theta1 = sym.Symbol('t1', commutative = False)
        theta2 = sym.Symbol('t2', commutative = False)
        theta3 = sym.Symbol('t3', commutative = False)

    if (symornum == 'num'):
        finalDCM = NumericalDCM(f_rot, s_rot, t_rot, theta1, theta2, theta3)
    else:
        finalDCM = SymbolicDCM(f_rot, s_rot, t_rot, theta1, theta2, theta3)
    
    print('\n' + str(seqval) + ' EA to DCM:')
    print(finalDCM)

    return(finalDCM)

def NumericalDCM(rot1, rot2, rot3, angle1, angle2, angle3):
    if (rot1 == 1):
        R1s = np.matrix([[1 , 0, 0],[0, np.cos(angle1), np.sin(angle1)],[0, -np.sin(angle1), np.cos(angle1)]])
    elif (rot1 == 2):
        R1s = np.matrix([[np.cos(angle1), 0, -np.sin(angle1)], [0, 1, 0], [np.sin(angle1), 0, np.cos(angle1)]])
    elif (rot1 == 3):
        R1s = np.matrix([[np.cos(angle1), np.sin(angle1), 0], [-np.sin(angle1), np.cos(angle1), 0], [0,0,1]])
    
    if (rot2 == 1):
        R2s = np.matrix([[1 , 0, 0],[0, np.cos(angle2), np.sin(angle2)],[0, -np.sin(angle2), np.cos(angle2)]])
    elif (rot2 == 2):
        R2s = np.matrix([[np.cos(angle2), 0, -np.sin(angle2)], [0, 1, 0], [np.sin(angle2), 0, np.cos(angle2)]])
    elif (rot2 == 3):
        R2s = np.matrix([[np.cos(angle2), np.sin(angle2), 0], [-np.sin(angle2), np.cos(angle2), 0], [0,0,1]])
    
    if (rot3 == 1):
        R3s = np.matrix([[1 , 0, 0],[0, np.cos(angle3), np.sin(angle3)],[0, -np.sin(angle3), np.cos(angle3)]])
    elif (rot3 == 2):
        R3s = np.matrix([[np.cos(angle3), 0, -np.sin(angle3)], [0, 1, 0], [np.sin(angle3), 0, np.cos(angle3)]])
    elif (rot3 == 3):
        R3s = np.matrix([[np.cos(angle3), np.sin(angle3), 0], [-np.sin(angle3), np.cos(angle3), 0], [0,0,1]])
    
    Rotations = [0, R1s, R2s, R3s]
    DCM = Rotations[3] * Rotations[2] * Rotations[1]
    return(DCM)

def SymbolicDCM(rot1, rot2, rot3, angle1, angle2, angle3):
    if (rot1 == 1):
        R1s = sym.Matrix([[1 , 0, 0],[0, sym.cos(angle1), sym.sin(angle1)],[0, -sym.sin(angle1), sym.cos(angle1)]])
    elif (rot1 == 2):
        R1s = sym.Matrix([[sym.cos(angle1), 0, -sym.sin(angle1)], [0, 1, 0], [sym.sin(angle1), 0, sym.cos(angle1)]])
    elif (rot1 == 3):
        R1s = sym.Matrix([[sym.cos(angle1), sym.sin(angle1), 0], [-sym.sin(angle1), sym.cos(angle1), 0], [0,0,1]])
    
    if (rot2 == 1):
        R2s = sym.Matrix([[1 , 0, 0],[0, sym.cos(angle2), sym.sin(angle2)],[0, -sym.sin(angle2), sym.cos(angle2)]])
    elif (rot2 == 2):
        R2s = sym.Matrix([[sym.cos(angle2), 0, -sym.sin(angle2)], [0, 1, 0], [sym.sin(angle2), 0, sym.cos(angle2)]])
    elif (rot2 == 3):
        R2s = sym.Matrix([[sym.cos(angle2), sym.sin(angle2), 0], [-sym.sin(angle2), sym.cos(angle2), 0], [0,0,1]])
    
    if (rot3 == 1):
        R3s = sym.Matrix([[1 , 0, 0],[0, sym.cos(angle3), sym.sin(angle3)],[0, -sym.sin(angle3), sym.cos(angle3)]])
    elif (rot3 == 2):
        R3s = sym.Matrix([[sym.cos(angle3), 0, -sym.sin(angle3)], [0, 1, 0], [sym.sin(angle3), 0, sym.cos(angle3)]])
    elif (rot3 == 3):
        R3s = sym.Matrix([[sym.cos(angle3), sym.sin(angle3), 0], [-sym.sin(angle3), sym.cos(angle3), 0], [0,0,1]])
    
    Rotations = [0, R1s, R2s, R3s]
    DCM = Rotations[3] * Rotations[2] * Rotations[1]
    return(DCM)

def NumInvVerify(DCM):
    InvMatrix = np.linalg.inv(DCM)
    TpMatrix = np.transpose(DCM)

    if (np.allclose(InvMatrix,TpMatrix)):
        print("\n The DCM is orthogonal. Below is the inverse:")
        print(InvMatrix)
    else:
        print("\n The DCM is not orthogonal. Below are the inverse & transpose:")
        print(InvMatrix)
        print(TpMatrix)

def DCMtoEA(seqval,DCM):
    # Indexing Array ahead of time, easier to type up:
    C11 = DCM[0,0]
    C12 = DCM[0,1]
    C13 = DCM[0,2]
    C21 = DCM[1,0]
    C22 = DCM[1,1]
    C23 = DCM[1,2]
    C31 = DCM[2,0]
    C32 = DCM[2,1]
    C33 = DCM[2,2]
    
    # If-checks for all possible EA sequences
    if (seqval == 231):
        angle1 = math.atan2(-C13,C11)
        angle2 = math.asin(C12)
        angle3 = math.atan2(C32, -C22)
    if (seqval == 121):
        angle1 = math.atan2(C12, -C13)
        angle2 = math.acos(C11)
        angle3 = math.atan2(C21, C31)
    if (seqval == 232):
        angle1 = math.atan2(C23, -C21)
        angle2 = math.acos(C22)
        angle3 = math.atan2(C32, C12)
    if (seqval == 123):
        angle1 = math.atan2(-C32, C33)
        angle2 = math.asin(C31)
        angle3 = math.atan2(-C21, C11)
    if (seqval == 323):
        angle1 = math.atan2(C32, C31)
        angle2 = math.acos(C33)
        angle3 = math.atan2(C23, -C13)
    if (seqval == 212):
        angle1 = math.atan2(C21, C23)
        angle2 = math.acos(C22)
        angle3 = math.atan2(C12, -C32)
    if (seqval == 321):
        angle1 = math.atan2(C12, C11)
        angle2 = (-1) * math.asin(C13)
        angle3 = math.atan2(C23, C33)
    if (seqval == 131):
        angle1 = math.atan2(C13, C12)
        angle2 = math.acos(C11)
        angle3 = math.atan2(C31, -C21)
    if (seqval == 213):
        angle1 = math.atan2(C31, C33)
        angle2 = (-1) * math.asin(C32)
        angle3 = math.atan2(C12, C22)
    if (seqval == 132):
        angle1 = math.atan2(C23, C22)
        angle2 = (-1) * math.asin(C21)
        angle3 = math.atan2(C31, C11)
    if (seqval == 313):
        angle1 = math.atan2(C31, -C32)
        angle2 = math.acos(C33)
        angle3 = math.atan2(C13, C23)
    if (seqval == 312):
        angle1 = math.atan2(-C21, C22)
        angle2 = (-1) * math.asin(C23)
        angle3 = math.atan2(-C13, C33)
    
    print("\nThe angles, in degrees, are:")
    print(math.degrees(angle1), math.degrees(angle2), math.degrees(angle3))

    return(angle1, angle2, angle3)

## DCM to PRP
# Finds Principal Rotation Parameters from DCM
def DCMtoPRP(DCM):
    # Finding the angle first
    cosTheta = (0.5) * (DCM[0,0] + DCM[1,1] + DCM[2,2] - 1)
    theta = math.acos(cosTheta)

    # Finding rotation vector
    lambda1 = (1/(2*math.sin(theta))) * (DCM[1,2] - DCM[2,1])
    lambda2 = (1/(2*math.sin(theta))) * (DCM[2,0] - DCM[0,2])
    lambda3 = (1/(2*math.sin(theta))) * (DCM[0,1] - DCM[1,0])
    vector = [lambda1, lambda2, lambda3]

    # Printing PRP
    print("\n The DCM can be represented by the following PRP:")
    print("Theta (rad): ", theta)
    print(vector)

    return(vector, theta)

## DCM to EPs
# Finds Euler Parameters from DCM
def DCMtoERM(DCM):
    # Indexing Array ahead of time, easier to type up:
    C11 = DCM[0,0]
    C12 = DCM[0,1]
    C13 = DCM[0,2]
    C21 = DCM[1,0]
    C22 = DCM[1,1]
    C23 = DCM[1,2]
    C31 = DCM[2,0]
    C32 = DCM[2,1]
    C33 = DCM[2,2]

    # Finding Euler Parameters
    ep4 = (0.5) * math.sqrt(1 + C11 + C22 + C33) # 4th needs to be found first
    ep1 = (C23 - C32) / (4*ep4)
    ep2 = (C31 - C13) / (4*ep4)
    ep3 = (C12 - C21) / (4*ep4)
    EPs = [ep1, ep2, ep3, ep4]
    EPunitCheck(EPs)

    # Printing PRP
    print("\n The DCM can be represented by the following EPs:")
    print(EPs)

    return(EPs)

## Euler Parameter to Principal Rotation Parameter (or reverse)
# Checks to see if theta is provided. If not, finds PRPs. If yes, finds EPs.
def EPtPRPb(vector, theta=None):
    if (theta is None):
        theta = 2 * math.acos(vector[3])
        lambda1 = vector[0] / (math.sin(theta/2))
        lambda2 = vector[1] / (math.sin(theta/2))
        lambda3 = vector[2] / (math.sin(theta/3))
        result = [lambda1, lambda2, lambda3]
    else:
        e4 = math.cos(theta/2)
        e1 = vector[0] * math.sin(theta/2)
        e2 = vector[1] * math.sin(theta/2)
        e3 = vector[2] * math.sin(theta/2)
        result = [e1, e2, e3, e4]
        EPunitCheck(result)
    
    return(result, theta)

## Euler Parameter Unit Norm Condition checker
# Checks to make sure vector magnitude is 1
def EPunitCheck(vector):
    mag = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2 + vector[3]**2)

    if mag == 1:
        print("confirmed")
        result = vector
    else:
        e1 = vector[0] / mag
        e2 = vector[1] / mag
        e3 = vector[2] / mag
        e4 = vector[3] / mag
        result = [e1, e2, e3, e4]
        print("normalized")
    
    return(result)

## Euler Parameter to Classical Rodrigues Parameter (or reverse)
# If input vector is of EP length, it finds CRPs. Otherwise, it finds EPs.
def EPtCRPb(vector):
    if (len(vector) == 4):
        p1 = vector[0] / vector[3]
        p2 = vector[1] / vector[3]
        p3 = vector[2] / vector[3]
        result = [p1, p2, p3]
    else:
        denom = math.sqrt(1 + (vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2]))
        e1 = vector[0] / denom
        e2 = vector[1] / denom
        e3 = vector[2] / denom
        e4 = 1 / denom
        result = [e1, e2, e3, e4]
        EPunitCheck(result)
    
    return(result)

## DCM to Classical Rodrigues Parameters
# Takes in DCM, converts to EPs, uses EPs to convert to CRPs, outputs CRPs.
def DCMtoCRP(DCM):
    EPs = DCMtoERM(DCM)
    CRP = EPtCRPb(EPs)

    print("\n The DCM can be represented by the following CRP:")
    print(CRP)

    return(CRP)

## Euler Parameters to DCM
# Takes in EP vector, finds DCM, outputs DCM
def EPtoDCM(vector):
    # First seperating so it is easier to type up
    e1 = vector[0]
    e2 = vector[1]
    e3 = vector[2]
    e4 = vector[3]
    # Creating the DCM
    DCM = np.matrix([[1 - 2*(e2**2) - 2*(e3**2), 2*(e1*e2 + e3*e4), 2*(e1*e3 - e2*e4)],[2*(e1*e2 - e3*e4), 1 - 2*(e1**2) - 2*(e3**2), 2*(e2*e3 + e1*e4)],[2*(e1*e3 + e2*e4), 2*(e2*e3 - e1*e4), 1 - 2*(e1**2) - 2*(e2**2)]])

    return(DCM)

## Classical Rodrigues Parameters to DCM
# Takes in CRP vector, finds EPs, finds DCM, outputs DCM
def CRPtoDCM(CRP):
    EPs = EPtCRPb(CRP)
    DCM = EPtoDCM(EPs)

    return(DCM)

## Modified Rodrigues Parameters to Euler Parameters (or reverse)
# If input vector is of EP length, it finds MRPs. Otherwise, it finds EPs.
def EPtMRPb(vector):
    if (len(vector) == 4):
        s1 = vector[0] / (1 + vector[3])
        s2 = vector[1] / (1 + vector[3])
        s3 = vector[2] / (1 + vector[3])
        result = [s1, s2, s3]
    else:
        denom = 1 + (vector[0]*vector[0] + vector[1]*vector[1] + vector[2]*vector[2])
        e1 = (2 * vector[0]) / denom
        e2 = (2 * vector[1]) / denom
        e3 = (2 * vector[2]) / denom
        e4 =(2 - denom) / denom
        result = [e1, e2, e3, e4]
        EPunitCheck(result)
    
    return(result)

## DCM to Modified Rodrigues Parameters
# Takes in DCM, converts to EPs, uses EPs to convert to CRPs, outputs CRPs.
def DCMtoMRP(DCM):
    EPs = DCMtoERM(DCM)
    MRP = EPtMRPb(EPs)

    print("\n The DCM can be represented by the following MRP:")
    print(MRP)

    return(MRP)

## Modified Rodrigues Parameters to DCM
# Takes in MRP vector, finds EPs, finds DCM, outputs DCM
def MRPtoDCM(MRP):
    EPs = EPtMRPb(MRP)
    DCM = EPtoDCM(EPs)

    return(DCM)

## Principal Rotation Parameters to DCM
# Takes in PRP vector, finds EPs, finds DCM, outputs DCM
def PRPtoDCM(PRP, theta):
    EPs, theta = EPtPRPb(PRP, theta)
    DCM = EPtoDCM(EPs)

    return(DCM)

## Add Euler Parameters
# Takes in e-prime (B-N), and e-double-prime(C-B), returns e.
def addEP(eprime, edprime):
    #seperating into temp vars bc it's easier to type
    ep1 = eprime[0]
    ep2 = eprime[1]
    ep3 = eprime[2]
    ep4 = eprime[3]
    epp = np.array([[edprime[0]],[edprime[1]],[edprime[2]],[edprime[3]]])

    # Euler Parameter addition
    EPaddMatrix = np.matrix([[ep4, -ep3, ep2, ep1],[ep3, ep4, -ep1, ep2],[-ep2, ep1, ep4, ep3],[-ep1, -ep2, -ep3, ep4]])
    EPs = EPaddMatrix * epp

    # Printing result
    print("\n Below is the Euler Parameter for Axis 3 relative to Axis 1")
    print(EPs)
    
    # Returning result
    result = np.transpose(EPs)
    return(result)

# Finds the derivative of Euler Parameter (e') using Euler Parameter and Omega
def EPDiff(euler,omega,list=None):
    # Seperating omega for ease of writing
    w1 = omega[0]
    w2 = omega[1]
    w3 = omega[2]
    # Checking if list math or Matrix math
    if (list == 'list') or (list == None):
        EPr1 = (0.5) * ((w3 * euler[1]) + (-w2 * euler[2]) + (w1 * euler[3]))
        EPr2 = (0.5) * ((-w3 * euler[0]) + (w1 * euler[2]) + (w2 * euler[3]))
        EPr3 = (0.5) * ((w2 * euler[0]) + (-w1 * euler[1]) + (w3 * euler[3]))
        EPr4 = (0.5) * ((-w1 * euler[0]) + (-w2 * euler[1]) + (-w3 * euler[2]))

        result = [EPr1, EPr2, EPr3, EPr4]
    else:
        # Creating omega matrix
        omegaM = np.matrix([[0,w3,-w2,w1],[-w3,0,w1,w2],[w2,-w1,0,w3],[-w1,-w2,-w3,0]])
        Eprime = omegaM * euler
        
        result = np.transpose(Eprime)
    
    return(result)


# Finds the derivative of CRP using CRP and Omega
def CRPDiff(crp,omega,list=None):
    # Seperating crp for ease of writing
    c1 = crp[0]
    c2 = crp[1]
    c3 = crp[2]
    # Checking if list math or Matrix math
    if (list == 'list') or (list == None):
        # Equations shown matrix form seperately
        crpdot1 = (0.5) * ((omega[0] * (1 + c1*c1)) + (omega[1] * (c1*c2 - c3)) + (omega[2] * (c1*c3 + c2)))
        crpdot2 = (0.5) * ((omega[0] * (c2*c1 + c3)) + (omega[1] * (1 + c2*c2)) + (omega[2] * (c2*c3 - c1)))
        crpdot3 = (0.5) * ((omega[0] * (c3*c1 - c2)) + (omega[1] * (c3*c2 + c1)) + (omega[2] * (1 + c3*c3)))

        result = [crpdot1, crpdot2, crpdot3]
    else:
        # Creating 3x3 Matrix with CRP
        cMatrix = np.matrix([[1+ c1*c1, c1*c2 - c3, c1*c3 + c2],[c2*c1 + c3, 1 + c2*c2, c2*c3 - c1], [c3*c1 - c2, c3*c2 + c1, 1 + c3*c3]])
        # Converting Omega into Column vector
        omegaM = np.transpose(omega)
        # Multiplying and transposing to return as row vector
        cprime = cMatrix * omegaM
        result = np.transpose(cprime)
    
    return(result)

def PRPtCRPb(vector, theta=None):
    # Checking to see if CRP or PRP is provided
    if (theta == None):
        # CRP -> PRP
        EPs = EPtCRPb(vector)
        PRP, theta = EPtPRPb(EPs)
        result = PRP
    else: # PRP -> CRP
        EPs = EPtPRPb(vector, theta)
        CRP = EPtCRPb(EPs)
        result = CRP
    
    return(result, theta)

def MRPDiff(mrp, omega, list=None):
    # Seperating MRPs for ease of writing
    s1 = mrp[0]
    s2 = mrp[1]
    s3 = mrp[2]
    o2 = s1*s1 + s2*s2 + s3*s3
    # Checking if list math or not
    if (list == 'list') or (list == None):
        sdot1 = (0.25) * ((omega[0] * (1 - o2 + (2*s1*s1))) + (omega[1] * 2 * ((s1*s2) - s3)) + (omega[2] * 2 * ((s1*s3) + s2)))
        sdot2 = (0.25) * ((omega[0] * 2 * ((s2*s1) + s3)) + (omega[1] * (1 - o2 + (2*s2*s2))) + (omega[2] * 2 * ((s2*s3) - s1)))
        sdot3 = (0.25) * ((omega[0] * 2 * ((s3*s1) - s2)) + (omega[1] * 2 * ((s3*s2) + s1)) + (omega[2] * (1 - o2 + (2*s3*s3))))

        result = [sdot1, sdot2, sdot3]

    else:
        # Creating 3x3 Matrix with MRP
        sMatrix = np.matrix([[1 - o2 + 2*s1*s1, 2*(s1*s2 - s3), 2*(s1*s3 + s2)], [2*(s2*s1 + s3), 1 - o2 + 2*s2*s2, 2*(s2*s3 - s1)], [2*(s3*s1 - s2), 2*(s3*s2 + s1), 1 - o2 + 2*s3*s3]])
        # Making Omega into Column Vector, Doing Matrix Multiplication, and Returning as Row Vector
        omegaM = np.transpose(omega)
        sprime = sMatrix * omegaM
        result = np.transpose(sprime) 
    
    return(result)

def PRPtMRPb(vector, theta=None):
    # Checking to see if CRP or PRP is provided
    if (theta == None):
        # MRP -> PRP
        EPs = EPtMRPb(vector)
        PRP, theta = EPtPRPb(EPs)
        result = PRP
    else:
        EPs = EPtPRPb(vector, theta)
        MRP = EPtMRPb(EPs)
        result = MRP
    
    return(result, theta)

def angMomCalc(inertia, omega):
    Hc1 = inertia[0] * omega[0]
    Hc2 = inertia[1] * omega[1]
    Hc3 = inertia[2] * omega[2]

    result = [Hc1, Hc2, Hc3]

    return(result)

def rotKineticCalc(omega, vector, intorhc=None):
    # First checking if vector is inertia or Hc. Assume inertia
    if (intorhc == 'inertia') or (intorhc == None):
        Hc = angMomCalc(vector, omega)
    else:
        Hc = vector
    # Now calculating Trot
    Trot1 = (0.5) * omega[0] * Hc[0]
    Trot2 = (0.5) * omega[1] * Hc[1]
    Trot3 = (0.5) * omega[2] * Hc[2]
    Trot = Trot1 + Trot2 + Trot3

    return(Trot)

def dwdt_torqueFree(omega, inertias):
    # Seperating into variables for ease of typing up / readibility
    I1 = inertias[0]
    I2 = inertias[1]
    I3 = inertias[2]
    w1 = omega[0]
    w2 = omega[1]
    w3 = omega[2]
    # See given Euler's rotational equations of motions:
    wdot1 = -((I3 - I2) * w2 * w3) / I1
    wdot2 = -((I1 - I3) * w3 * w1) / I2
    wdot3 = -((I2 - I1) * w1 * w2) / I3
    # Combining and returning
    omegadot = [wdot1, wdot2, wdot3]
    
    return(omegadot)
