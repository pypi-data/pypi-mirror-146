from roboticstoolbox import *
from spatialmath import SE3
import numpy as np

robot = models.DH.Puma560();
# robot.base = SE3.Tz(-0.6714)
print(robot)
q = robot.qr

S, TE0 = robot.twists()
print(S)
print(TE0)


T_poe = S.exp(q).prod() * TE0
print(T_poe)



T = robot.fkine(q)
print(T)