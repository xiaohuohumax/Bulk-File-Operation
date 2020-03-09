<!--
 * @Author:xiaohuohu
 * @Date: 2020-03-09 11:23:53
 * @LastEditTime: 2020-03-09 12:04:51
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \CodeAll\code_Python\批量操作\批量操作6.0\renameRule.md
 -->
# `-o`改名规则

1. `<old:?:?:?>` 原名字切片操作
   **三个参数均可缺省 (-,+)**
   `<old:初始:结束:步进>`
2. `<oldr:?:?:...>` 原名字正则操作
   **前两个参数均可缺省 [0,+) 第三个参数 不能包含:`< >`**
   `<old:选中第几位:选中的子项位数:正则表达式>`
   例如: 
   原: `xiao123huohu567hu`
   操作: `<oldr:0:1:(\d(\d{2}))>` `<oldr:1:1:(\d(\d{2}))>`
   结果: `23` `67`
3. `<new:...>` 添加新名字
   **`...`不能包含`空格 < >`**
   例如:
   操作: `<new:xiaohuohu>`
   结果: `xiaohuohu`
4. `<time:...>` 添加时间
   **`...`可以填写时间表达式:`%Y %m %d %H %M %S`只能包含:`% 字母 数字 _`**
   例如:
   操作: `<time:%Y_%m_%d_%H_%M_%S>`
   结果: `2020_03_04_12_34_12`
5. `<add:?:?>` 自增 防止重名
   **连个参数均可缺省[0,+) (0,+)**
   默认没写时自动末尾添加 `<add:1:1>` 也可以添加 `-a` 去除自动添加
   例如: 
   原: `xyz.png` `xxx.png`
   操作: `<add:1:3>`
   结果: `1.png` `4.png`
6. 上述命令可随意组合
   例如:
   操作: `<old:1:7:1><new:sdas><time:%Y><add:1:4><old:::><new:xiaohuohu>`