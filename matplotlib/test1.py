from pylab import *

figure(figsize=(8,6),dpi=80,facecolor=None,edgecolor='black',frameon=False)

subplot(1,1,1)

X = np.linspace(-np.pi,np.pi,256,endpoint=True)
C,S=np.cos(X),np.sin(X)


plot(X,C,color="red",linewidth=2.0,linestyle='-',label="consine")
plot(X,S,color="green",linewidth=2.0,linestyle='-',label="sine")
legend(loc='upper left')

#xlim(-4.0,4.0)
#xticks(np.linspace(-4,4,9,endpoint=True))
xmin,xmax=X.min(),X.max()
dx=(xmax-xmin)*0.01
xlim(xmin-dx,xmax+dx)
xticks([-np.pi,-np.pi/2,0,np.pi/2,np.pi],[r'$-\pi$',r'$-\pi/2$',r'$0$',r'$+\pi/2$',r'$+\pi$'])


#ylim(-1.0,1.0)
#yticks(np.linspace(-1,1,5,endpoint=True))

ymin,ymax=S.min(),S.max()
dy=(ymax-ymin)*0.05
ylim(ymin-dy,ymax+dy)
yticks([-1,0,+1],[r'$-1$',r'$0$',r'$+1$'])

#savefig('test1.png',dpi=72)

ax = gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position('left')
ax.spines['left'].set_position(('data',0))

show()