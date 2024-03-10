# MiniMax & AlphaBeta

## 传送门

[一图流解释 Alpha-Beta 剪枝](https://www.7forz.com/3211/)

[alpha-beta剪枝算法及实践](https://blog.csdn.net/qq_31615919/article/details/79681063)

[Alpha-Beta剪枝](https://blog.csdn.net/tangchenyi/article/details/22925957)

## MiniMax Algorithm

```cpp
//node记录当前player，depth记录搜索深度
function minimax(node, depth) 
   // 如果能得到确定的结果或者深度为零，使用评估函数返回局面得分
   if node is a terminal node or depth = 0
       return the heuristic value of node
   // 如果轮到对手走棋，是极小节点，选择一个得分最小的走法
   if the adversary is to play at node
       let α := +∞
       for each child of node
           α := min(α, minimax(child, depth-1))
   // 如果轮到我们走棋，是极大节点，选择一个得分最大的走法
   else {we are to play at node}
       let α := -∞
       foreach child of node
           α := max(α, minimax(child, depth-1))
   return α;
```

## Alpha-Beta Pruning

事实上，MIN、MAX不断的倒推过程中是存在着联系的，当它们满足某种关系时后续的搜索是多余的！alpha-beta剪枝算法把生成后继和倒推值估计结合起来，及时减掉一些无用分支，以此来提高算法的效率。

定义极大层的下界为alpha，极小层的上界为beta，alpha-beta剪枝规则描述如下：
（1）alpha剪枝。若任一极小值层结点的beta值不大于它任一前驱极大值层结点的alpha值，即alpha(前驱层) >= beta(后继层)，则可终止该极小值层中这个MIN结点以下的搜索过程。这个MIN结点最终的倒推值就确定为这个beta值。
（2）beta剪枝。若任一极大值层结点的alpha值不小于它任一前驱极小值层结点的beta值，即alpha(后继层) >= beta(前驱层)，则可以终止该极大值层中这个MAX结点以下的搜索过程，这个MAX结点最终倒推值就确定为这个alpha值。

```cpp
function alphabeta(node, depth, α, β, Player)
    //达到最深搜索深度或胜负已分         
    if  depth = 0 or node is a terminal node
        return the heuristic value of node//heuristic：启发式的
    if  Player = MaxPlayer // 极大节点
        for each child of node // 子节点是极小节点
            α := max(α, alphabeta(child, depth-1, α, β, not(Player) ))   
            if β ≤ α 
            // 该极大节点的值>=α>=β，该极大节点后面的搜索到的值肯定会大于β，因此不会被其上层的极小节点所选用了。对于根节点，β为正无穷
                 break //beta剪枝                        
        return α
    else // 极小节点
        for each child of node //子节点是极大节点
            β := min(β, alphabeta(child, depth-1, α, β, not(Player) )) // 极小节点
            if β ≤ α // 该极大节点的值<=β<=α，该极小节点后面的搜索到的值肯定会小于α，因此不会被其上层的极大节点所选用了。对于根节点，α为负无穷
                break //alpha剪枝
        return β 
```

可以看到alpha-beta剪枝每次跟踪两个变量alpha和beta，对于MAX方，beta是父节点MIN的一个上界，当前搜索到alpha父节点的上界时，没有必要继续搜索了，因为已经达到了父节点的上界；对于MIN方，alpha是父节点MAX的一个下界，当前搜索到alpha父节点的下界时，没有必要继续搜索了，因为已经达到了父节点的下界，最搜索下去只是徒劳。

