import tkinter
from matplotlib import animation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from mpl_toolkits.mplot3d import proj3d
import numpy as np
import socket
import time
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Sock_wifi():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '192.168.1.9'  # host LAN ip
        self.port = 12350

    def hostserver(self):
        self.s.bind((self.host, self.port))
        self.s.listen(10)
        print("Asteptare client conexiune")
        self.c, addr = self.s.accept()
        print("Conexiune reusita")


def avion():
    glBegin(GL_LINE_LOOP)
    glColor4f(1.0, 1.0, 0.0, 1)
    glVertex3f(3, 0, -1)
    glVertex3f(4, 0, 0)
    glVertex3f(3, 0, 1)
    glVertex3f(0.5, 0, 1)
    glVertex3f(0.5, 0, 6)
    glVertex3f(-0.5, 0, 6)
    glVertex3f(-0.5, 0, 1)
    glVertex3f(-4, 0, 1)
    glVertex3f(-4, 0, 1.75)
    glVertex3f(-4.75, 0, 1.75)
    glVertex3f(-4.75, 0, -1.75)
    glVertex3f(-4, 0, -1.75)
    glVertex3f(-4, 0, -1)
    glVertex3f(-0.5, 0, -1)
    glVertex3f(-0.5, 0, -6)
    glVertex3f(0.5, 0, -6)
    glVertex3f(0.5, 0, -1)
    glEnd()


def compass():
    glBegin(GL_LINE_LOOP)
    glColor4f(1.0, 0.0, 1.0, 1)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(2.5, 0.0, 0.0)
    glColor4f(1, 0, 1, 0)

    glColor4f(1.0, 0.0, 1.0, 1)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 2.5)

    glColor4f(1, 0, 1, 0)
    glVertex3f(0, 0.5, 2.5)
    glColor4f(1, 0, 1, 1)
    glVertex3f(0, 0.5, 2.83)
    glVertex3f(0, 0.5, 2.5)
    glVertex3f(0, 0.83, 2.5)
    glVertex3f(0, 0.83, 2.83)
    glVertex3f(0, 0.83, 2.5)
    glVertex3f(0, 1.13, 2.5)
    glVertex3f(0, 1.13, 2.83)
    glColor4f(1, 0, 1, 0)
    glVertex3f(0, 1.13, 2.5)
    glVertex3f(0, 0.83, 2.5)
    glVertex3f(0, 0.83, 2.83)
    glVertex3f(0, 0.83, 2.5)
    glVertex3f(0, 0.5, 2.83)
    glVertex3f(0, 0.5, 2.5)
    glVertex3f(0, 0.0, 0)
    glColor4f(1, 0, 1, 0)
    glVertex3f(2.5, 0.5, 0.0)
    glColor4f(1, 0, 1, 1)
    glVertex3f(2.5, 0.5, 0.0)
    glVertex3f(2.5, 1.11, 0.0)
    glVertex3f(2.83, 0.5, 0.0)
    glVertex3f(2.83, 1.11, 0.0)
    glColor4f(1, 0, 1, 0)
    glVertex3f(2.83, 0.5, 0.0)
    glVertex3f(2.5, 1.11, 0.0)
    glVertex3f(2.5, 0.5, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glColor4f(1, 0, 1, 1)
    glVertex3f(0.0, -2.5, 0.0)
    glEnd()


def animate(i):
    length = int(s.c.recv(2))
    msg = s.c.recv(length).decode('utf-8').split('|')
    # if msg == "STOP":
    # s.c.close()
    # ok = 1
    print(length)
    print(msg)
    global t
    dt = time.time() - t
    print(dt)
    t = time.time()
    global vN, vE, vS
    vN_str.set("Viteza Nord: " + msg[0] + " [m/s]")
    vE_str.set("Viteza Est: " + msg[1] + " [m/s]")
    vS_str.set("Viteza Sus: " + msg[2] + " [m/s]")
    dN_str.set("Deplasament Nord: " + msg[3] + " [m]")
    dE_str.set("Deplasament Est: " + msg[4] + " [m]")
    dS_str.set("Deplasament Sus: " + msg[5] + " [m]")
    if msg[10] == "1":
        avertisment.set("Vireaza la stanga!!!")
    elif msg[10] == "2":
        avertisment.set("Vireaza la dreapta!")
    elif msg[10] == "3":
        avertisment.set("Vireaza in sus!")
    elif msg[10] == "4":
        avertisment.set("Vireaza in jos!")
    elif msg[10] == "5":
        avertisment.set("Vireaza la dreapta si in sus!")
    elif msg[10] == "6":
        avertisment.set("Vireaza la stanga si in sus")
    elif msg[10] == "7":
        avertisment.set("Vireaza la stanga si in jos")
    elif msg[10] == "8":
        avertisment.set("Vireaza la dreapta si in jos!")
    else:
        avertisment.set("")
    distN.append(float(msg[3]))
    distE.append(float(msg[4]))
    distS.append(float(msg[5]))

    limita = abs(max(np.array([distN]).max(initial=0), np.array([distN]).min(initial=0), np.array([distE]).max(initial=0),
                     np.array([distE]).min(initial=0), np.array([distS]).max(initial=0), np.array([distS]).min(initial=0), key=abs))

    a4.clear()
    a4.plot(limita, limita, limita)
    a4.plot(distN, distE, distS, marker='D', markevery=[0, len(distN) - 1], markerfacecolor='r')

    x, y, z = distN[0], distE[0], distS[0]
    x2, y2, _ = proj3d.proj_transform(x, y, z, a4.get_proj())
    a4.annotate("Start", (x2, y2))
    a4.set_xlabel('deplasament Nord [m]', fontfamily='Times New Roman', fontsize=12)
    a4.set_ylabel('deplasament Est [m]', fontfamily='Times New Roman', fontsize=12)
    a4.set_zlabel('deplasament Sus [m]', fontfamily='Times New Roman', fontsize=12)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(float(msg[6]), 1, 0, 0)
    glRotatef(float(msg[7]), 0, 0, 1)
    glRotatef(float(msg[8]), 0, 1, 0)
    glColor3f(1, 1, 1)
    avion()
    glPopMatrix()
    glPushMatrix()
    glRotatef(float(msg[9]), 0, 1, 0)
    compass()
    glPopMatrix()
    pygame.display.flip()


def fereastra(tip, ok2):
    if ok2 == 0:
        s.c.send(bytes([len("START")]))
        s.c.send("START".encode("utf-8"))
        print("START")
        ok2 = 1
    topin = tkinter.Toplevel()

    def inchidere():
        pygame.quit()
        topin.destroy()

    topin.title("Monitorizare " + tip)
    frame1 = tkinter.LabelFrame(topin)
    frame2 = tkinter.LabelFrame(topin)

    l1 = tkinter.Label(frame1, textvariable=vN_str, font=("Times New Roman", 14)).pack()
    l2 = tkinter.Label(frame1, textvariable=vE_str, font=("Times New Roman", 14)).pack()
    l3 = tkinter.Label(frame1, textvariable=vS_str, font=("Times New Roman", 14)).pack()
    l4 = tkinter.Label(frame1, textvariable=dN_str, font=("Times New Roman", 14)).pack()
    l5 = tkinter.Label(frame1, textvariable=dE_str, font=("Times New Roman", 14)).pack()
    l6 = tkinter.Label(frame1, textvariable=dS_str, font=("Times New Roman", 14)).pack()
    l_avertisment = tkinter.Label(frame2, textvariable=avertisment, font=("Times New Roman", 14)).pack()
    canvas4 = FigureCanvasTkAgg(fig4, master=topin)
    canvas4.draw()

    btn = tkinter.Button(topin, text="Quit", command=inchidere, font=("Times New Roman", 12))
    frame1.pack(padx=10, pady=10)
    canvas4.get_tk_widget().pack(padx=10, pady=10, ipadx=10, ipady=10)
    frame2.pack(padx=10, pady=10)
    btn.pack(padx=10, pady=10, ipadx=10, ipady=10)
    ani4 = animation.FuncAnimation(fig4, animate, interval=1, repeat=True, frames=60)
    topin.mainloop()


if __name__ == "__main__":
    vN, vE, vS = 0, 0, 0
    distN = []
    distE = []
    distS = []
    root = tkinter.Tk()
    fig4 = plt.figure(dpi=115)
    a4 = fig4.add_subplot(111, projection="3d")
    vN_str = tkinter.StringVar()
    vE_str = tkinter.StringVar()
    vS_str = tkinter.StringVar()
    dN_str = tkinter.StringVar()
    dE_str = tkinter.StringVar()
    dS_str = tkinter.StringVar()
    avertisment = tkinter.StringVar()
    root.title("Aplicatie monitorizare")
    root.geometry("400x300")


    def indoor():
        s.c.send(bytes([len("indoor")]))
        s.c.send("indoor".encode("utf-8"))
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -15)
        glRotatef(30, 1, 0, 0)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        fereastra("indoor", 0)


    def outdoor():
        s.c.send(bytes([len("outdoor")]))
        s.c.send("outdoor".encode("utf-8"))
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        gluPerspective(60, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -15)
        glRotatef(30, 1, 0, 0)
        fereastra("outdoor", 0)


    def inchidere2():
        root.destroy()
        quit()


    label = tkinter.Label(root, text="Aleceti tipul de monitorizare:", font=("Times New Roman", 16)).pack()
    frame = tkinter.LabelFrame(root, text="text", padx=5, pady=5, font=("Times New Roman", 12)).pack(padx=5, pady=5)
    btn1 = tkinter.Button(frame, text="Indoor", command=indoor, font=("Times New Roman", 12)).pack(padx=10, pady=10,
                                                                                                   ipadx=10, ipady=10)
    btn2 = tkinter.Button(frame, text="Outdoor", command=outdoor, font=("Times New Roman", 12)).pack(padx=10, pady=10,
                                                                                                     ipadx=10, ipady=10)
    btn3 = tkinter.Button(frame, text="Quit", command=inchidere2, font=("Times New Roman", 12)).pack(padx=10, pady=10,
                                                                                                     ipadx=10,
                                                                                                     ipady=10)

    s = Sock_wifi()
    s.hostserver()
    t = time.time()
    tkinter.mainloop()
