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