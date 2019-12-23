import numpy as np
import tkinter as tk
import time
import tkinter.messagebox

class node():
    def __init__(self,father,r,c):
        self.father_node = father
        self.row = r
        self.col = c
        self.h_set()
        self.g_set()
        self.f_set()

    def h_set(self):
        if start==None or end ==None:
            self.h=0
        #find h, here it is the Euclidean distance between node and the end
        else:
            self.h = 10*np.sqrt(np.abs(self.row-end[0])**2 + np.abs(self.col-end[1])**2)

    def g_set(self):
        if start==None or end==None:
            self.g=0
        else:
            #find g, here xaxis & yaxis is 10, diaginal is 14
            if self.father_node == None:
                self. g= 0
            else:
                if np.abs(self.father_node.row - self.row) + np.abs(self.father_node.col - self.col) == 1:
                    self.g = self.father_node.g + 10
                else:
                    self.g = self.father_node.g + 14

    def f_set(self):
        #find f = g + h
        self.f = self.g + self.h

    def update(self,new_node):
        #if the node has been in open list, update the g
        if self.g > new_node.g:
            self.g=new_node.g
            self.father_node=new_node.father_node
            self.f_set()

#check whether the input"n" is legal
def check_n():
    try:
        #未输入n便执行
        if len(text.get()) == 0:
            tk.messagebox.showinfo(title='tips', message='Input map size please！')
        return 1
    except:
        tk.messagebox.showinfo(title='tips', message='Map size is illegal！')
        return 0

#draw arrows which is from the father node to the extened node
def draw_arrow(point,color='Grey',fill='black'):
    #judge the orientation
    row_dis=point.father_node.row-point.row
    col_dis=point.father_node.col-point.col

    #the center coordinate of father node
    row_fat= np.int((rs[point.father_node.row]+rs[point.father_node.row+1])*0.5)
    col_fat= np.int((rs[point.father_node.col]+rs[point.father_node.col+1])*0.5)

    #the center coordinate of barth node, is also the beginning of the pole of arrow
    row_bir=np.int((rs[point.row]+rs[point.row+1])*0.5)
    col_bir=np.int((cs[point.col]+cs[point.col+1])*0.5)

    #the end of arrow
    row_end=np.int(0.8*row_bir+0.2*row_fat)
    col_end=np.int(0.8*col_bir+0.2*col_fat)

    # #the wing of arrow
    # row_wing=np.int(0.6*row_end+0.4*row_bir)
    # col_wing=np.int(0.6*col_end+0.4*col_bir)
    #
    #clear the area to remove the former arrow
    axis=rs[point.row+1]-rs[point.row]
    canvas.create_rectangle(col_bir-np.ceil(0.2*axis),row_bir-np.ceil(0.2*axis),col_bir+np.ceil(0.2*axis),row_bir+np.ceil(0.2*axis),fill='black')

    #draw arrow
    canvas.create_line(col_bir,row_bir,col_end,row_end,width='2',fill=color)
    canvas.create_oval(int(col_bir-axis/15), int(row_bir-axis/15),int(col_bir+axis/15),int(row_bir+axis/15),outline=color,fill=fill)
    # if np.abs(row_dis) + np.abs(col_dis) ==2:
    #     canvas.create_line(col_end,row_end,col_end,row_wing,width='1',fill='Grey')
    #     canvas.create_line(col_end,row_end,col_wing,row_end,width='1',fill='Grey')
    # elif row_dis == 1 or row_dis == -1:
    #     canvas.create_line(col_end,row_end,col_wing+row_end-row_wing,row_wing,width='1',fill='Grey')
    #     canvas.create_line(col_end,row_end,col_wing-row_end+row_wing,row_wing,width='1',fill='Grey')
    # else:
    #     canvas.create_line(col_end,row_end,col_wing,row_wing+col_end-col_wing,width='1',fill='Grey')
    #     canvas.create_line(col_end,row_end,col_wing,row_wing-col_end+col_wing,width='1',fill='Grey')



#draw the info and rectangle of new node
def draw_unit(point,color,flag=0):
    #use flag to make sure draw all the results
    row=point.row
    col=point.col
    #draw rectangle
    #check the red line, regard point as centre
    flag_l=0
    flag_r=0
    flag_u=0
    flag_d=0
    for i in searchlist:
        if flag == 1:
            break
        if i.row-point.row == 1   and i.col-point.col == 0:
            flag_d=1
        if i.row - point.row == -1 and i.col - point.col == 0:
            flag_u=1
        if i.row - point.row == 0 and i.col - point.col == 1:
            flag_r=1
        if i.row - point.row == 0 and i.col - point.col == -1:
            flag_l=1

    size=1

    if flag_l == 0 :
        canvas.create_line(cs[col],rs[row],cs[col],rs[row+1],fill=color,width=size)
    if flag_u == 0 :
        canvas.create_line(cs[col], rs[row], cs[col + 1], rs[row], fill=color,width=size)
    if flag_r == 0 :
        canvas.create_line(cs[col+1], rs[row], cs[col + 1], rs[row + 1], fill=color,width=size)
    if flag_d == 0 :
        canvas.create_line(cs[col], rs[row+1], cs[col + 1], rs[row + 1], fill=color,width=size)

    #show info
    point.f_set()
    t_f = tk.Label(window, text='f=%d' %point.f, bg='black', font=('Arial', np.max([1,np.int(np.floor(100/n))])), foreground='green', width=3, height=1 )
    t_g = tk.Label(window, text='g=%d' %point.g, bg='black', font=('Arial', np.max([1,np.int(np.floor(100/n))])), foreground='green', width=3, height=1 )
    t_h = tk.Label(window, text='h=%d' %point.h, bg='black', font=('Arial', np.max([1,np.int(np.floor(100/n))])), foreground='green', width=3, height=1 )

    t_f.place(x=cs[col]+1,y=rs[row]+1,anchor='nw')
    t_g.place(x=cs[col]+1,y=rs[row+1]-1,anchor='sw')
    t_h.place(x=cs[col+1]-1,y=rs[row+1]-1,anchor='se')

    #draw arrow
    if flag == 1:
        draw_arrow(point,color='red',fill='red')
    else:
        draw_arrow(point)

#based on the father node, extend the new node and draw it at the picture
def extend(father):
    for i in range(father.row - 1, father.row + 2):
        for j in range(father.col - 1, father.col + 2):
            #not create now node
            if i==father.row and j==father.col:
                continue
            if i<0 or j<0 or i>=n or j>=n:
                continue
            #create new node
            new_node = node(father,i,j)
            flag1=0
            flag2=0
            flag3=0
            flag4=0
            flag5=0
            for temp in openlist:
                #update the old node
                if temp.row == new_node.row and temp.col==new_node.col:
                    temp.update(new_node)
                    #深蓝色扩展节点
                    draw_unit(temp,'#0000FF')
                    flag1=1
                    break

            for temp in closelist:
                #check out whether new_node has been in closelist
                if temp.row == new_node.row and temp.col==new_node.col:
                    flag2=1
                    break

            for temp in obstruct:
                #check out whether there is a obstruct directly aroungd the new_node
                if temp.row == father.row and np.abs(temp.col-father.col)==1:
                    if temp.col == new_node.col and np.abs(temp.row - new_node.row) == 1:
                        flag3 += 1
                if temp.col == father.col and np.abs(temp.row-father.row)==1 :
                    if temp.row == new_node.row and np.abs(temp.col - new_node.col) == 1:
                        flag3 += 1

            if np.abs(father.col-new_node.col)+ np.abs(father.row-new_node.row) == 2:
                flag4=1

            #use flag3-5 to be sure agent won't go through two diagonal obstruction
            if flag3==2 and flag4==1:
                flag5=1


            if flag1==0 and flag2==0 and flag5==0:
                #be sure new_node is not in closelist, add the new one
                openlist.append(new_node)
                if i!=end[0] and j!=end[1]:
                    draw_unit(new_node,'blue')
    openlist.remove(father)
    closelist.append(father)

#initial the map
def map_init():
    global map
    global openlist,closelist,obstruct
    global searchlist
    map=np.zeros(n)
    openlist=[]
    closelist=[]
    #a list to save obstructions
    obstruct=[]
    searchlist=[]

#by looping the extend function, figure out the best path
def figure():
    global is_find
    global handle_node

    #whether find the result
    is_find=False
    handle_node=start_node
    openlist.append(handle_node)
    #iterate to extend nodes
    while True:
        if handle_node.row==end[0] and handle_node.col==end[1]:
            is_find = True
            break
        if len(openlist)==0:
            is_find = False
            break

        extend(handle_node)

        if handle_node!=start_node:
            draw_unit(handle_node,'yellow')
            search=handle_node
            searchlist.append(search)

        #sleep a while and then draw the now node and the extended node
        time.sleep(0.1)
        canvas.update()

        #find the least f node, take it as handle_node
        handle_node.f=10000
        for temp in openlist:
            if temp.f <= handle_node.f:
                handle_node=temp

#by getting back from the end node, find the best path
def find_res():
    if is_find == True:
        results_rev=[]
        temp=handle_node
        #go back
        while temp != start_node:
            results_rev.append(temp)
            temp=temp.father_node

        #reverse the results_rev
        results=[]
        for i in range(len(results_rev)):
            results.append(results_rev[len(results_rev)-1-i])

        for i in range(len(results)-1):
            #print('row:',results[i].row,' col:',results[i].col)
            draw_unit(results[i],'red',1)
        tk.messagebox.showinfo(title='tips', message='Find the path!')
        #print(results)
    else:
        #when go through all the possible points, agent still can't find a path
        tk.messagebox.showinfo(title='tips', message='no answer！')

#left mouse reaction, select the start node
def l_callback(event):
    #left mouse click, set the start and draw it as green
    global start
    r = np.int(np.floor(event.y * len(map) / height))
    c = np.int(np.floor(event.x * len(map)/ width))
    #remove the former start on screen
    if start != None:
        canvas.create_rectangle(cs[start[1]]+1, rs[start[0]]+1, cs[start[1] + 1]-1, rs[start[0] + 1]-1, fill='black')

    start = (r,c)
    canvas.create_rectangle(cs[c]+1,rs[r]+1,cs[c+1]-1,rs[r+1]-1,fill='green')
    #print("当前位置：",event.x,event.y)
    #print(r,c)

#right mouse reaction, select the end node
def r_callback(event):
    # right mouse click, set the end and draw it as red
    global end
    r = np.int(np.floor(event.y * len(map)/height))
    c = np.int(np.floor(event.x * len(map)/width))
    if end != None:
        canvas.create_rectangle(cs[end[1]]+1, rs[end[0]]+1, cs[end[1] + 1]-1, rs[end[0] + 1]-1, fill='black')

    end=(r,c)
    canvas.create_rectangle(cs[c]+1,rs[r]+1,cs[c+1]-1,rs[r+1]-1,fill='red')
    #print("当前位置：",event.x,event.y)
    #print(r,c)

#middle mouse reaction, select the obstruction node
def m_callback(event):
    r = np.int(np.floor(event.y * len(map)/height))
    c = np.int(np.floor(event.x * len(map)/width))
    temp=node(None,r,c)
    obstruct.append(temp)
    closelist.append(temp)
    canvas.create_rectangle(cs[c]+1,rs[r]+1,cs[c+1]-1,rs[r+1]-1,fill='blue')

#reaction for the button"draw"
def hit1():
    global n,done
    #use check_n to be sure map size has been set
    do = check_n()
    if do == 1:
        done=1
        n=int(text.get())
        tk.messagebox.showinfo(title='tips', message='Use left mouse button to select start node;'+'\n'+'Use middle mouse button to select obstructions;'
                               +'\n' +'Use right mouse button to select end node. ')
        map_init()
        draw_init()

#reaction for the button"run"
def hit2():
    global start_node,end_node
    end_node = node(None, end[0], end[1])
    start_node = node(None, start[0], start[1])
    #use check_n to be sure map size has been set
    do = check_n()
    if do == 1:
        #use done to be sure map has been drawn before running
        if done == 0:
            tk.messagebox.showinfo(title='tips', message='Please press "draw" first!')
        else:
            figure()
            find_res()


#initial the window, such as size, text, button and so on
def window_init():

    global height,width
    global window
    global text

    #be sure press "run" after pressing "draw"
    global done
    done =0

    #set height & width
    height = 1000
    width = 1000
    #init window
    window = tk.Tk()
    window.title('A_star')
    window.geometry('%dx%d' % (width+100,height))

    #point out the agent to input n
    label = tk.Label(window, text='input map size：', font=('Arial', 8), width=15, height=1)
    label.place(x=width+10,y=20,anchor='nw')

    #the text to input n
    text= tk.Entry(window, show=None, width=4)
    text.place(x=width+20,y=40,anchor='nw')

    #draw button
    b1=tk.Button(window,text='draw',width=4,height=2,bg='white', font=('Arial', 12), command=hit1)
    b1.place(x=width+20,y=100,anchor='nw')

    #run button
    b2=tk.Button(window,text='run',width=4,height=2,bg='white', font=('Arial', 12), command=hit2)
    b2.place(x=width+20,y=200,anchor='nw')

    window.mainloop()

#when press the button"绘图", draw the map
def draw_init():
    global canvas
    global rs,cs
    global height,width

    global start,end
    start=None
    end=None

    h_temp=n*int(np.floor(height / n))
    w_temp=n*int(np.floor(width / n))
    height=h_temp
    width=w_temp

    canvas = tk.Canvas(window,bg='black',height=height,width=width)
    canvas.place(x=0,y=0,anchor='nw')

    #capture the matrix
    rs=[]
    cs=[]

    #浅蓝色划线
    for i in range(0, height, int(np.floor(height / n))):
        canvas.create_line(0, i , width , i ,fill='green')
        rs.append(i)
    if len(rs) <= n:
        canvas.create_line(0, height, width , height,fill='green')
        rs.append(height)
    # y
    for i in range(0, width, int(np.floor(width / n))):
        canvas.create_line(i, 0, i , height ,fill='green')
        cs.append(i )
    if len(cs) <= n:
        canvas.create_line(width, 0, width, height ,fill='green')
        cs.append(width)

    #click mouse
    canvas.bind("<Button-1>", l_callback)
    canvas.bind('<Button-2>', m_callback)
    canvas.bind("<Button-3>", r_callback)




if __name__ == '__main__':
    window_init()
