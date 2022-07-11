import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
 
fig, ax = plt.subplots()
fig1, ax1 = plt.subplots()
 
n_balls = 1 #Define a quantidade de partículas do sistema
Lyapunov = False #True para calcular Lyapunov APENAS com 2 particulas
Salvar = False #True para salvar a animação das partículas

class Particle(object):
    def __init__(self, init_pos, init_vel):
        self.pos = np.array(init_pos)
        self.vel = np.array(init_vel)

def OverlapWithOthers(particles, pos, radius):
    for particle in particles:
        if np.linalg.norm(particle.pos-pos) <= 2*radius:
            return True
    return False
 
class Box(object):
    def __init__(self, width=  4, height=4, n = n_balls, radius=0.001, raio=2, posicao = []):
        
        self.raio = raio
        self.borda = plt.Circle((2,2), raio, linewidth=1, fill=False, facecolor='black')
        
        self.width = width
        self.height = height
        self.posicao = posicao
 
        self.border = plt.Rectangle((0, 0), width, height,
                                    linewidth=2, fill=False)
 
        self.n = n
        self.radius = radius
 
        #POSIÇÃO INICIAL DAS PARTÍCULAS
        self.particles = []
        
        self.x1 = (width-2*self.radius)*0.71+self.radius 
        self.y1 = (height-2*self.radius)*0.25+self.radius
               
        print("x = " +str(round(self.x1,4)) + " e y = " + str(round(self.y1,4)))
        
        self.eps = 0
        
        for i in range(n):
            while True:
                self.x1 += self.eps
                self.y1 += self.eps
                
                pos = (self.x1,self.y1)
                if not OverlapWithOthers(self.particles, pos, self.radius):
                    break 
            
            vel = (2,3*1.1254)
            
            self.particles.append(Particle(pos, vel))
            self.eps += 10e-05
        self.time = 0
        
    def step(self, dt):

        #COLISÃO DE PARTÍCULAS COM A CIRCUNFERENCIA
        for particle in self.particles:
            if (np.sqrt((particle.pos[0]-2)**2+(particle.pos[1]-2)**2)) > self.raio -0.05:
                
                self.modulo_normal = np.sqrt((particle.pos[0]-2)**2+(particle.pos[1]-2)**2)
                self.normal = ((particle.pos[0]-2)/self.modulo_normal,(particle.pos[1]-2)/self.modulo_normal)

                self.k = (-2*np.dot(particle.vel,self.normal)*self.normal[0],
                          -2*np.dot(particle.vel,self.normal)*self.normal[1])
                particle.vel[0] = particle.vel[0]+self.k[0]
                particle.vel[1] = particle.vel[1]+self.k[1]

        #ATUALIZAÇÃO DA POSIÇÃO DA PARTÍCULA
        for i in range(self.n):
            self.particles[i].pos += self.particles[i].vel * dt
        self.time += dt
        
box = Box()
ax.set(xlim=[0, 4], ylim=[0,4])
ax.set_aspect('equal', adjustable='box')
ax.add_patch(box.borda)

cor = ['darkred','salmon','teal','indigo','fuchsia','darkmagenta','royalblue','lime',
       'gold','skyblue','plum','dodgerblue','crimson','darkorange','mediumpurple',
       'rebeccapurple']

circles = [plt.Circle((0, 0), 0.05, color = cor[i]) for i in range(n_balls)]

trace, = ax.plot([], [], '-', lw=1, ms=2, color='r')
historyx, historyy = [], []
###############################################################################
# CÁLCULO DO EXPOENTE DE LYAPUNOV 
# CONDICIONADO QUANDO O PARÂMETRO LYAPUNOV É VERDADEIRO
if Lyapunov == True:
    
    posicao1, posicao2 = [], []
    distancia, tempo = [], []
    tempo = np.zeros(10000)
    t = 0
    for j in range(0,10000):
        box.step(0.03)
        for i in range(n_balls):
            circles[i].center = tuple(box.particles[i].pos)
            if i%2 == 0:
                posicao = list(box.particles[i].pos)
                posicao1.append(posicao)
            else:
                posicao = list(box.particles[i].pos)
                posicao2.append(posicao)
        
        distancia.append(np.log(np.sqrt((posicao1[j][0]-posicao2[j][0])**2+
                         (posicao1[j][1]-posicao2[j][1])**2)))
        t += 0.03
        tempo[j] = t
    
    coef = (distancia[766] - distancia[0])/23
    
    print("O coeficiente de Lyapunov é:" + str(coef))
    ax1.plot(tempo,distancia)
###############################################################################
# CONSIDERAR TRACE QUANDO O NÚMERO DE PARTÍCULAS FOR 1

def animate(x):
    box.step(0.02)
 
    for i in range(n_balls):
        circles[i].center = tuple(box.particles[i].pos)
        historyx.append(box.particles[i].pos[0])
        historyy.append(box.particles[i].pos[1])

        ax.add_artist(circles[i])
    trace.set_data(historyx,historyy)
    
    if n_balls == 1:
        return *circles, trace
    else:
        return circles


# INICIA A ANIMAÇÃO DO PROBLEMA COM BASE NAS ATAULIZAÇÃOES DA POSIÇÃO DA PARTÍCULA
anim = animation.FuncAnimation(fig, animate,
                               frames=6006, interval=40,
                               repeat=True, blit=True)
if Salvar == True:
    writervideo = animation.FFMpegWriter(fps=60)
    anim.save('CircularChaoticBilliards.mp4', writer=writervideo, dpi = 150)
    plt.close()