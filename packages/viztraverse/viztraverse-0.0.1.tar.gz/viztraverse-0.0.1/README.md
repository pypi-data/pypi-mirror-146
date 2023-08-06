### VizTreeTraversal 

## [LeetCode Describes Deserialize & Draw here ](https://support.leetcode.com/hc/en-us/articles/360011883654-What-does-1-null-2-3-mean-in-binary-tree-representation) 
Often, LeetCode problems require a slight learning curve to feel comfortable using their TreeNode data structure. One helpful portion of the LeetCode website
describes a detailed example. Have a look at the linked content [here](https://support.leetcode.com/hc/en-us/articles/360011883654-What-does-1-null-2-3-mean-in-binary-tree-representation)

## Using the product 

To install, use pip3 and the command land as follows: 

```bash
pip3 install viztraverse
```

Once installed you can import the library as follows:
```bash
import viztraverse from viztraverse
```

Then to use the seriealize library:
```bash
viztraverse.deserialize([1,1,null,1]); 
```

And, finally to draw: 
```bash
viztraverse.draw(viztraverse.deserialize([1,1,null,1]); 
```


## Troubleshooting

This library requires the correct or proper version for the tkanner library. The problem is specific to MacOS from what the resources say [here]('https://www.google.com')
Nonetheless, if you must face the problem due to failures, here is a common solution:

```bash
pip3 install tk
```









