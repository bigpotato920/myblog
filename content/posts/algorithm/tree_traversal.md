Title: 二叉树的遍历问题总结
Date: 2014-2-20
Modified: 2014-2-20
Category: algorithm
Tags: leetcode, algorithm, tree, java
Slug: tree_traversal
Summary: 对二叉树深度优先和广度优先遍历问题的总结
Author: bigpotato

##二叉树的遍历问题总结
二叉树的遍历主要有：

+ 深度优先遍历
+ 广度优先遍历

其中深度优先遍历又包括：

+ 前序遍历
+ 中序遍历
+ 后序遍历

深度优先遍历分为递归和非递归的实现方式，广度优先遍历就是层次遍历，根据二叉树的遍历方式的组合可以重二叉树，下面对这些问题进行一个总结。
###前序遍历
>Given a binary tree, return the preorder traversal of its nodes' values.
>For example:
>Given binary tree `{1,#,2,3}`,
>
>```
>  1
>   \
>    2
>   /
>  3
>```

>return `[1,2,3]`.


>**Note:** Recursive solution is trivial, could you do it iteratively?

[**Leetcode 前序遍历题目地址**](https://oj.leetcode.com/problems/binary-tree-preorder-traversal/)


前序遍历非递归可以用一个栈来实现，由于遍历过程中要先访问树的左子树，而后右子树，所以实现的时候先把根节点的右孩子入栈，而后是左孩子。
```java
    public List<Integer> preorderTraversal(TreeNode root) {
        Stack<TreeNode> stack = new Stack<TreeNode>();
        private List<Integer> result = new ArrayList<Integer>();
        if (root == null)
            return result;
        stack.push(root);
        while (!stack.empty()) {
            TreeNode node = stack.pop();
            result.add(node.val);
            if (node.right != null)
                stack.push(node.right);
            if (node.left != null)
                stack.push(node.left);
        }
        return result;
    }
```
###中序遍历
>Given a binary tree, return the inorder traversal of its nodes' values.
>For example:
>Given binary tree `{1,#,2,3}`,

>```
>  1
>   \
>    2
>   /
>  3 
>```

>return `[1,3,2]`.


>**Note:** Recursive solution is trivial, could you do it iteratively?


[**Leetcode 中序遍历题目地址**](https://oj.leetcode.com/problems/binary-tree-inorder-traversal/)


二叉树中序遍历非递归也是利用栈来完成，由于二叉树中序遍历要先遍历左孩子而后根节点，最后是右孩子。所以算法先找到根节点的最左孩子，把一路下来的左孩子依次入栈，访问最左孩子，而后是访问根节点，然后把根节点右孩子当做当前节点重复上述过程直到节点都访问完。代码如下：
```java
    public List<Integer> inorderTraversal(TreeNode root) {
        Stack<TreeNode> stack = new Stack<TreeNode>();
        List<Integer> result = new ArrayList<Integer>();
        TreeNode cur_node = root;
        if (root == null)
            return result;

        while (cur_node != null || !stack.empty()) {

            while (cur_node != null) {
                stack.push(cur_node);
                cur_node = cur_node.left;
            }

            cur_node = stack.pop();
            result.add(cur_node.val);
            cur_node = cur_node.right;
        }
        
        return result;
    }
```

###后序遍历
>Given a binary tree, return the postorder traversal of its nodes' values.
For example:
Given binary tree `{1,#,2,3}`,

>```
>  1
>   \
>    2
>   /
>  3 
>```

>return `[3,2,1]`.


>**Note:** Recursive solution is trivial, could you do it iteratively?


[**Leetcode 后序遍历题目地址**](https://oj.leetcode.com/problems/binary-tree-postorder-traversal/)


二叉树后序遍历非递归可以通过两个栈来实现，具体代码如下：
```java
    public List<Integer> postorderTraversal(TreeNode root) {
        Stack<TreeNode> s1 = new Stack<TreeNode>();
        Stack<TreeNode> s2 = new Stack<TreeNode>();
        List<Integer> result = new ArrayList<Integer>();
        if (root == null)
            return result;

        s1.push(root);

        while (!s1.empty()) {
            TreeNode cur_node = s1.pop();
            if (cur_node.left != null)
                s1.push(cur_node.left);
            if (cur_node.right != null)
                s1.push(cur_node.right);

            s2.push(cur_node);
        }

        while (!s2.empty()) {
            result.add(s2.pop().val);
        }
        
        return result;
    }
```
二叉树后序遍历非递归还可以通过一个栈来和一个访问前驱标志来实现，通过这个标志为来判断根节点的右子树是否访问完，如果访问完则访问根节点，否则继续遍历右子树，代码如下：
```java
    public List<Integer> postorderTraversal(TreeNode root) {
        Stack<TreeNode> s = new Stack<TreeNode>();
        List<Integer> result = new ArrayList<Integer>();
        TreeNode pre = null;
        while (root != null || !s.empty()) {
            //找到最左孩子
            if (root != null) {
                s.push(root);
                root = root.left;
            //如果右子树没有被访问，访问右子树
            } else if (s.peek().right != pre) {
                root = s.peek().right;
                pre = null;
            //访问根节点
            } else {
                pre = s.peek();
                result.add(s.pop().val);
            }
        }
        
        return result;
    }
```
二叉树后序遍历非递归还可以只通过一个栈来实现，代码如下：
```java
    public List<Integer> postorderTraversal(TreeNode root) {
        Stack<TreeNode> s = new Stack<TreeNode>();
        List<Integer> result = new ArrayList<Integer>();
        if (root == null)
            return result;
        do {
            while (root != null) {
                if (root.right != null)
                    s.push(root.right);
                s.push(root);
                root = root.left;
            }

            root = s.pop();
            if (root.right != null && root.right == s.peek()) {
                s.pop();
                s.push(root);
                root = root.right;
            } else {
                result.add(root.val);
                root = null;
            }

        } while (!s.empty());

        return result;
    }
```

###通过二叉树中序和后序遍历构建二叉树
>Given inorder and postorder traversal of a tree, construct the binary tree.


>**Note:**


>You may assume that duplicates do not exist in the tree.


[**Leetcode题目地址**](https://oj.leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)


对与如下的二叉树,其中序遍历序列和后序遍历序列分别为：
```
        1
       / \
      2   3
     / \ / \
    4  5 6  7
```
**中序遍历:**4 2 5 `1` 6 3 7


**后序遍历:**4 5 2 6 7 3 `1`


在后序遍历序列中最后一个元素即为二叉树根节点，在中序遍历序列中二叉树根节点把二叉树分成左右子树，左子树的根节点为根节点1的左孩子，右子树的根节点为根节点1的右孩子，这个过程具有良好的递归性。算法实现的代码如下：
```java
    public TreeNode buildTree(int[] inorder, int[] postorder) {
       return buildTreeHelper(inorder, 0, inorder.length - 1,
               postorder, 0, postorder.length - 1);
    }

    private TreeNode buildTreeHelper(int[] inorder, int in_begin, int in_end,
                                     int[] postorder, int post_begin, int post_end) {
        if (in_begin > in_end)
            return null;
        TreeNode root = new TreeNode(postorder[post_end]);
        int in_index = in_begin;
        for (int i = in_begin; i <= in_end; i++) {
            if (inorder[i] == root.val) {
                in_index = i;
                break;
            }
        }
        root.left = buildTreeHelper(inorder, in_begin, in_index - 1,
                postorder, post_begin, post_begin + in_index - in_begin - 1);

        root.right = buildTreeHelper(inorder, in_index + 1, in_end,
                postorder, post_begin + in_index - in_begin, post_end - 1);

        return root;
    }
```

###通过二叉树前序遍历和中序遍历序列构建二叉树
>Given preorder and inorder traversal of a tree, construct the binary tree.


>**Note:**


>You may assume that duplicates do not exist in the tree.


[**Leetcode 题目地址**](https://oj.leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)


对与如下的二叉树,其前序遍历序列和中序遍历序列分别为：
```
        1
       / \
      2   3
     / \ / \
    4  5 6  7
```
**前序遍历:**`1` 2 4 5 3 6 7


**中序遍历:**4 2 5 `1` 6 3 7


这道题的思路和上一个题目类似，前序遍历序列第一个元素是整个二叉树的根节点元素，根据根节点元素可以把中序遍历序列分成两部分，分别用来构造二叉树的左右子树。具体代码如下：
```java
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        return buildTreeHelper(preorder, 0, preorder.length - 1,
                inorder, 0, inorder.length - 1);
    }

    private TreeNode buildTreeHelper(
        int[] preorder, int pre_begin, int pre_end,
        int[] inorder, int in_begin, int in_end) {

        if (pre_begin > pre_end)
            return null;
        TreeNode root = new TreeNode(preorder[pre_begin]);
        int in_index = in_begin;
        for (int i = in_begin; i <= in_end; i++) {
            if (inorder[i] == root.val) {
                in_index = i;
                break;
            }
        }

        root.left = buildTreeHelper(
                preorder, pre_begin + 1, pre_begin + in_index - in_begin,
                inorder, in_begin, in_index - 1);
        root.right = buildTreeHelper(
                preorder, pre_begin + in_index - in_begin + 1, pre_end,
                inorder, in_index + 1, in_end);

        return root;
    }
```

###二叉树层次遍历
>Given a binary tree, return the level order traversal of its nodes' values. (ie, from left to right, level by level).

>For example:


>Given binary tree `{3,9,20,#,#,15,7}`,


>```
>   3
>  / \ 
> 9  20
>    /\
>   15 7
>```

>return its level order traversal as:


>```
>[
>   [3],
>   [9, 20],
>   [15, 7]
>]
>```


[**Leetocode 二叉树层序遍历题目地址**](https://oj.leetcode.com/problems/binary-tree-level-order-traversal/)


二叉树层序遍历可以采用队列来实现，但这道题要求求出每一层的序列，这里采用的方法是利用两个变量分别记录当前层的元素数目和下一层的元素数目。代码如下：
```java
public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<List<Integer>>();
        Queue<TreeNode> queue = new LinkedList<TreeNode>();

        if (root == null)
            return result;

        queue.add(root);
        int cur_level_count = 1;
        int next_level_count = 0;
        List<Integer> tmp_level = new ArrayList<Integer>();

        while (!queue.isEmpty()) {
            TreeNode node = queue.remove();
            if (node != null) {
                tmp_level.add(node.val);
                queue.add(node.left);
                queue.add(node.right);
               
                next_level_count += 2; 
            }
            cur_level_count--;

            if (cur_level_count == 0) {
                if (!tmp_level.isEmpty()) {
                    result.add(new ArrayList<Integer>(tmp_level));
                    tmp_level.clear();
                    cur_level_count = next_level_count;
                    next_level_count = 0;
                }
        
            }
        }

        return result;
    }
```


>Given a binary tree, return the bottom-up level order traversal of its nodes' values. (ie, from left to right, level by level from leaf to root).

>For example:


>Given binary tree `{3,9,20,#,#,15,7}`,


>```
>   3
>  / \ 
> 9  20
>    /\
>   15 7
>```

>return its level order traversal as:


>```
>[
>   [15, 7]
>   [9, 20],
>   [3]
>]
>```


[**Leetocode 二叉树层序遍历题目地址**](https://oj.leetcode.com/problems/binary-tree-level-order-traversal-ii/)


这道题目和上一题的思路类似，只是在把每一层的遍历结果插入result时采用头插法，就能得到逆序的层次遍历结果。