import numpy as np
import tkinter as tk
import random

class GoL:
    def __init__(self, width=50, height=50, zoom=1, fps=60.0, canvas=None, window=None):
        self.width=width
        self.height=height
        self.grid=np.zeros((self.width, self.height), dtype=int)
        self.grid
        self.zoom=zoom
        self.fps=fps
        self.rendergrid=np.zeros((self.width, self.height), dtype=int)
        self.state='active'
        self.canvas=canvas
        self.canvas.config(width=self.width*self.zoom, height=self.height*self.zoom)
        self.window=window
    
    def init_oneglider(self):
        self.grid[self.height-1][0]=1
        self.grid[self.height-1][1]=1
        self.grid[self.height-1][2]=1
        self.grid[self.height-2][2]=1
        self.grid[self.height-3][1]=1
        
    def init_random(self, p=0.1):
        for i in range(self.height):
            for j in range(self.width):
                if(random.random()<p):
                    self.grid[i][j]=1
        
    
    def count_neighbours(self, i, j, grid):
        return grid[(i)%self.height][(j+1)%self.width]+grid[(i)%self.height][(j-1)%self.width]+grid[(i+1)%self.height][(j)%self.width]+grid[(i-1)%self.height][(j)%self.width]+grid[(i+1)%self.height][(j+1)%self.width]+grid[(i-1)%self.height][(j+1)%self.width]+grid[(i+1)%self.height][(j-1)%self.width]+grid[(i-1)%self.height][(j-1)%self.width]
    
    def update(self):
        oldgrid=np.copy(self.grid)
        for i in range(self.height):
            for j in range(self.width):
                neigh=self.count_neighbours(i,j,oldgrid)
                if oldgrid[i][j]==1:
                    if neigh<2:
                        self.grid[i][j]=0
                    elif neigh==2 or neigh==3:
                        self.grid[i][j]=1
                    elif neigh>3:
                        self.grid[i][j]=0
                if oldgrid[i][j]==0:
                    if neigh==3:
                        self.grid[i][j]=1
                
                #value=self.grid[i][j]
                #colorval = "#%02x%02x%02x" % (255*value,155*value,255*value) #convert (255,255,255) to '#ffffff'
        return oldgrid, self.grid
                
    def render(self, oldgrid, newgrid):    
        colorval = "#%02x%02x%02x" % (255,155,255)
        for i in range(self.height):
            for j in range(self.width):        
                if(oldgrid[i][j]!=self.grid[i][j]):
                    if self.grid[i][j]==1:
                        self.rendergrid[i][j] = self.canvas.create_rectangle(j*self.zoom,i*self.zoom,(j+1)*self.zoom,(i+1)*self.zoom,width=0,fill=colorval, tag=str(i*self.width+j))
                    if self.grid[i][j]==0:
                        #canvas.delete(str(i*self.width+j))
                        self.canvas.delete(self.rendergrid[i][j])
    
    def slowrender(self, newgrid):
        colorval = "#%02x%02x%02x" % (255,155,255)
        self.canvas.delete('all')
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j]==1:
                    self.rendergrid[i][j] = self.canvas.create_rectangle(j*self.zoom,i*self.zoom,(j+1)*self.zoom,(i+1)*self.zoom,width=0,fill=colorval, tag=str(i*self.width+j))
                    
    def activate(self, event):
        if(self.state!='active'):
            self.state='active'
            self.titleupdate()
            self.animate()
    def animate(self):
        if(self.state=='active'):
            oldgrid, newgrid=self.update()
            self.render(oldgrid, newgrid)
            self.canvas.after(int(1000./myGoL.fps), self.animate)
    
    def stepping(self, event):
        self.state='stepping'
        self.titleupdate()
        if(self.state=='stepping'):
            oldgrid, newgrid=self.update()
            self.render(oldgrid, newgrid)
    
    def pause(self, event):
        if(self.state!='paused'):
            self.state='paused'
            self.titleupdate()
        elif(self.state=='paused'):
            self.state='active'
            self.titleupdate()
            self.animate()
    
    def modify(self, event):
        if(self.state!='modifying'):
            self.state='modifying'
            self.titleupdate()
        elif(self.state=='modifying'):
            self.state='active'
            self.titleupdate()
            self.animate()
    def add(self, event):
        if(self.state=='modifying'):
            oldgrid=np.copy(self.grid)
            i=event.y//self.zoom
            j=event.x//self.zoom
            self.grid[i][j]=1
            self.render(oldgrid, self.grid)
    def subtract(self, event):
        if(self.state=='modifying'):
            oldgrid=np.copy(self.grid)
            i=event.y//self.zoom
            j=event.x//self.zoom
            self.grid[i][j]=0
            self.render(oldgrid, self.grid)
    
    def titleupdate(self):
        self.window.title('Conway\'s GoL - '+self.state)
    
    def zoomupdate(self, event):
        try:
            self.zoom=int(event.char)
            self.canvas.config(width=self.width*self.zoom, height=self.height*self.zoom)
            self.slowrender(self.grid)
        except ValueError:
            pass
    

myWindow=tk.Tk()
myWindow.title('Conway\'s GoL - active')
myWindow.configure(background='gray')
#mainframe=tk.Frame(master=myWindow)
#mainframe.grid(row=0, column=0)
mycanvas=tk.Canvas(master=myWindow, bg='#000000')
mycanvas.grid(row=0,column=0)
    
myGoL=GoL(zoom=7, canvas=mycanvas, window=myWindow)

mycanvas.focus_set()
mycanvas.bind('a', myGoL.activate)
mycanvas.bind('s', myGoL.stepping)
mycanvas.bind('p', myGoL.pause)
mycanvas.bind('m', myGoL.modify)
mycanvas.bind('<Button-1>', myGoL.add)
mycanvas.bind('<B1-Motion>', myGoL.add)
mycanvas.bind('<Button-3>', myGoL.subtract)
mycanvas.bind('<B3-Motion>', myGoL.subtract)

for i in range(10):
    mycanvas.bind(str(i), myGoL.zoomupdate)

#myGoL.init_random()
myGoL.init_oneglider()

myGoL.animate()

myWindow.mainloop()