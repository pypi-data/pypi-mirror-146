from my_verilog import *
    
    
    
clk = port('CLK','in',1)               #输入端口clk
D = port('D', 'in', 1)                 #输入端口D
set_ = port('set', 'in', 1)            #输入端口set，用于置1
reset = port('rst', 'in', 1)           #输入端口rst，用于置0
 
Q = port('Q', 'out', 1)                #输出端口Q

reg_Q = reg('Q', 1)                    #Q设置为寄存器类变量

always_item = IF('rst', [block_assign(Q,0)],[IF('set', [block_assign(Q,1)], [block_assign(Q,~D)])])

always_1 = always(clk)                    
always_1.append(always_item)

items = items_set(reg_Q, always_1) 
           
top = module('test', None, items, D, Q, clk)   #module类，参数分别为，模块名，模块参数，模块行为，端口
code = top.visit()                             #visit方法，翻译成verilogHDL
print(code)







    