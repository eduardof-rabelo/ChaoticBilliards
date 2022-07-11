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
    def __init__(self, width=  4, height=3, n = n_balls, radius=0.001, raio=0.75):
        
        self.raio = raio
        self.borda = plt.Circle((2,1.5), raio, linewidth=1, fill=True, facecolor='black')
        
        self.width = width
        self.height = height
 
        self.border = plt.Rectangle((0, 0), width, height,
                                    linewidth=1, fill=False)
 
        self.n = n
        self.radius = radius
        
        self.posicao = []
 
        # DEFINE AS POSIÇÕES INICIAIS DA PARTÍCULA
        self.particles = []
        
        self.x1 = (width-2*self.radius)*0.1+self.radius
        self.y1 = (height-2*self.radius)*0.1+self.radius
        
        print("x = " +str(round(self.x1,4)) + " e y = " + str(round(self.y1,4)))
        
        self.eps = 0
        
        for i in range(n):
            while True:
                self.x1 += self.eps
                self.y1 += self.eps
                
                pos = (self.x1,self.y1)
                if not OverlapWithOthers(self.particles, pos, self.radius):
                    break 
            
            vel = (np.sqrt(2),np.sqrt(2))
            
            self.particles.append(Particle(pos, vel))
            #SOMA UMA PORÇÃO EPSILON A POSIÇÃO INICIAL DA PARTÍCULA
            self.eps += 1e-05
        self.time = 0
        
    def step(self, dt):
  
        # COLISÃO DA PARTÇIUILA COM A CIRCUNFERENCIA
        for particle in self.particles:
            if (np.sqrt((particle.pos[0]-2)**2+(particle.pos[1]-1.5)**2)) < self.raio +0.05:
                
                self.modulo_normal = np.sqrt((particle.pos[0]-2)**2+(particle.pos[1]-1.5)**2)
                self.normal = ((particle.pos[0]-2)/self.modulo_normal,(particle.pos[1]-1.5)/self.modulo_normal)

                self.k = (-2*np.dot(particle.vel,self.normal)*self.normal[0],
                          -2*np.dot(particle.vel,self.normal)*self.normal[1])
                particle.vel[0] = particle.vel[0]+self.k[0]
                particle.vel[1] = particle.vel[1]+self.k[1]

        # COLISÃO DA PARTÇIULA COM A PAREDE
            if particle.pos[0] <= self.radius or \
                    particle.pos[0] >= self.width - 0.08:
                particle.vel[0] *= -1
            if particle.pos[1] <= self.radius or \
                    particle.pos[1] >= self.height - 0.08:
                particle.vel[1] *= -1
        # ATUALIZAÇÃO DA POSIÇÃO DA PARTÍCULA
        for i in range(self.n):
            self.particles[i].pos += self.particles[i].vel * dt
            self.posicao.append(self.particles[i].pos)
        self.time += dt
        
    def getpos(self):
        return self.posicao
        
box = Box()
ax.set(xlim=[0, 4], ylim=[0, 3])

ax.set_aspect('equal', adjustable='box')
ax.add_patch(box.borda)
ax.add_patch(box.border)

cor = ['darkred','salmon','teal','indigo','fuchsia','darkmagenta','royalblue','lime',
       'gold','skyblue','plum','dodgerblue','crimson','darkorange','mediumpurple',
       'rebeccapurple']

circles = [plt.Circle((0, 0), 0.05, color = cor[i]) for i in range(n_balls)]


def animate(x):
    box.step(0.02)
 
    for i in range(n_balls):
        circles[i].center = tuple(box.particles[i].pos)
        
        ax.add_artist(circles[i])
        
    return circles

anim = animation.FuncAnimation(fig, animate,
                               frames=6006, interval=40,
                               repeat=True, blit=True)

circles2 = [plt.Circle((0, 0), 0.05, color = cor[i]) for i in range(n_balls)]

posicao1, posicao2 = [], []
distancia, tempo = [], []
tempo = np.zeros(10000)

##############################################################################
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

if Salvar == True:
    writervideo = animation.FFMpegWriter(fps=60)
    anim.save('CircularChaoticBilliards.mp4', writer=writervideo, dpi = 150)
    plt.close()
