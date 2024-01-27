
# Prompt Engineering

[toc]

# 吴恩达 x Open AI ChatGPT 提示工程教程

![](Pics/prompt000.png)

[吴恩达 x Open AI ChatGPT 提示工程教程](https://www.bilibili.com/video/BV1s24y1F7eq/)

[ChatGPT|万字长文总结吴恩达prompt-engineering课 --- 知乎](https://zhuanlan.zhihu.com/p/628394563)

## 01 Introduction

种类
1. base LLM --- 基于训练文本数据预测下一个词
2. instruction tuned LLM --- 遵从指令 & 针对指令微调 --- 在基础LLM上使用输入输出进行微调

RLHF --- Reinforcement Learning with Human Feedback

Helpful,Honest,Harmless

## 02 Guidelines for Prompting

principle
1. write clear and specific instructions (不在于长短，在于说清楚) clear ≠ short
2. give the model time to think

### Tactic 1: Use delimiters to clearly indicate distinct parts of the input

delimiter 定界符 可以是任何清晰的标点符号来分割文本

使用定界符可用于避免 prompt injection

![](Pics/prompt002.png)


```python
# Use delimiters to clearly indicate distinct parts of the input¶
# Delimiters can be anything like: ```, """, ---, < >, <tag> </tag>, :
prompt = f"""
Summarize the text delimited by triple backticks 
into a single sentence. ```{text}```
"""
```

![](Pics/prompt001.png)


### Tactic 2: Ask for a structured output

JSON

HTML

```python

# Ask for a structured output
prompt = f"""
Generate a list of three made-up book titles along \ 
with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.
"""
```

### Tactic 3: Ask the model to check whether conditions are satisfied

```python
text_2 = f"""
The sun is shining brightly today, and the birds are singing. It's a beautiful day to go for a walk in the park. The flowers are blooming, and the trees are swaying gently in the breeze. People are out and about, enjoying the lovely weather. Some are having picnics, while others are playing games or simply relaxing on the grass. It's a perfect day to spend time outdoors and appreciate the beauty of nature.
"""
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_2}\"\"\"
"""

# Result
# No steps provided.
```

```python
text_1 = f"""
Making a cup of tea is easy! First, you need to get some water boiling. While that's happening, grab a cup and put a tea bag in it. Once the water is hot enough, just pour it over the tea bag. Let it sit for a bit so the tea can steep. After a few minutes, take out the tea bag. If you like, you can add some sugar or milk to taste. And that's it! You've got yourself a delicious cup of tea to enjoy.
"""

prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""

# Result
# Step 1 - Get some water boiling.
# Step 2 - Grab a cup and put a tea bag in it.
# Step 3 - Once the water is hot enough, pour it over the tea bag.
# Step 4 - Let it sit for a bit so the tea can steep.
# Step 5 - After a few minutes, take out the tea bag.
# Step 6 - If you like, add some sugar or milk to taste.
# Step 7 - Enjoy your delicious cup of tea.
```

### Tactic 4: "Few-shot" prompting

Few-shot 少样本

```python
prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
```

### Tactic 5: Specify the steps required to complete a task

```python
text = f"""
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
"""
# example 1
prompt_1 = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following \
keys: french_summary, num_names.

Separate your answers with line breaks.

Text:
 ```{text}```
"""

# 1 - Jack and Jill, siblings, go on a quest to fetch water from a hilltop well, but encounter misfortune when Jack trips on a stone and tumbles down the hill, with Jill following suit, yet they return home and remain undeterred in their adventurous spirits.

# 2 - Jack et Jill, frère et sœur, partent en quête d'eau d'un puits au sommet d'une colline, mais rencontrent un malheur lorsque Jack trébuche sur une pierre et dévale la colline, suivi par Jill, pourtant ils rentrent chez eux et restent déterminés dans leur esprit d'aventure.

# 3 - Jack, Jill

# 4 - {
#   "french_summary": "Jack et Jill, frère et sœur, partent en quête d'eau d'un puits au sommet d'une colline, mais rencontrent un malheur lorsque Jack trébuche sur une pierre et dévale la colline, suivi par Jill, pourtant ils rentrent chez eux et restent déterminés dans leur esprit d'aventure.",
#   "num_names": 2
# }




# Ask for output in a specified format




prompt_2 = f"""
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
"""

# Summary: Jack and Jill, siblings, go on a quest to fetch water from a hilltop well but encounter misfortune along the way.

# Translation: Jack et Jill, frère et sœur, partent en quête d'eau d'un puits au sommet d'une colline mais rencontrent des malheurs en chemin.

# Names: Jack, Jill

# Output JSON: {"french_summary": "Jack et Jill, frère et sœur, partent en quête d'eau d'un puits au sommet d'une colline mais rencontrent des malheurs en chemin.", "num_names": 2}
```

### Tactic 6: Instruct the model to work out its own solution before rushing to a conclusion

错误使用

```python
prompt = f"""
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost me a flat $100k per year, and an additional $10 / square foot
What is the total cost for the first year of operations as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
"""
```



```python
prompt = f"""
Your task is to determine if the student's solution is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution and evaluate if the student's solution is correct or not. Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
 ```question here```
Student's solution:
 ```student's solution here```
Actual solution:
 ```steps to work out the solution and your solution here```
Is the student's solution the same as actual solution just calculated:
 ```yes or no```
Student grade:
 ```correct or incorrect```

Question:
 ```I'm building a solar power installation and I need help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost me a flat $100k per year, and an additional $10 / square foot
What is the total cost for the first year of operations as a function of the number of square feet.``` 
Student's solution:
 ```Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000```

Actual solution:
"""

# To calculate the total cost for the first year of operations, we need to add up the costs of land, solar panels, and maintenance.

# Let x be the size of the installation in square feet.

# Costs:
# 1. Land cost: $100 * x
# 2. Solar panel cost: $250 * x
# 3. Maintenance cost: $100,000 + $10 * x

# Total cost: $100 * x + $250 * x + $100,000 + $10 * x = $360 * x + $100,000

# Is the student's solution the same as the actual solution just calculated:
# No

# Student grade:
# Incorrect
```

### Model Limitations

#### hallucination 幻觉，幻视，幻听

doesn't know the boundary of its knowledge very well

it might try to answer questions about obscure topics and can make things up that sound plausible but are not actually true

![](Pics/prompt003.png)

## 03 Iterative Prompt Development

iteratively analyze and refine your prompts to generate marketing copy from a product fact sheet

![](Pics/prompt004.png)






## 04 Summarizing


## 05 Inferring


## 06 Transforming


## 07 Expanding


## 08 Chatbot


## 09 Conclusion

