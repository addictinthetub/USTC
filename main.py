import PySimpleGUI as sg

from collections import Counter
import re

from collections import defaultdict
import re

#----------------------------------    前戏    ------------------------------------------

letterA = sg.Input(s=15)
letterB = sg.Input(s=15)
letterC = sg.Input(s=15)
letterD = sg.Input(s=15)
letterE = sg.Input(s=15)
letterF = sg.Input(s=15)
letterG = sg.Input(s=15)
letterH = sg.Input(s=15)
letterI = sg.Input(s=15)
letterJ = sg.Input(s=15)
letterK = sg.Input(s=15)
letterL = sg.Input(s=15)
letterM = sg.Input(s=15)
letterN = sg.Input(s=15)
letterO = sg.Input(s=15)
letterP = sg.Input(s=15)
letterQ = sg.Input(s=15)
letterR = sg.Input(s=15)
letterS = sg.Input(s=15)
letterT = sg.Input(s=15)
letterU = sg.Input(s=15)
letterV = sg.Input(s=15)
letterW = sg.Input(s=15)
letterX = sg.Input(s=15)
letterY = sg.Input(s=15)
letterZ = sg.Input(s=15)

result = sg.Output(s=(60,30),key='-OUTPUT1-')

hints = sg.Output(s=(60,12),key='-OUTPUT2-')

NAME_SIZE=23

#----------------------------------    变量    ------------------------------------------

def name(name):
        dots = NAME_SIZE-len(name)-2
        return sg.Text(name + ' ' + '•'*dots, size=(NAME_SIZE,1), justification='r',pad=(0,0), font='Courier 10')

layout_l = [
                [sg.Text('字母的置换情况')],
                [name('A'), letterA],
                [name('B'), letterB],
                [name('C'), letterC],
                [name('D'), letterD],
                [name('E'), letterE],
                [name('F'), letterF],
                [name('G'), letterG],
                [name('H'), letterH],
                [name('I'), letterI],
                [name('J'), letterJ],
                [name('K'), letterK],
                [name('L'), letterL],
                [name('M'), letterM],
                [name('N'), letterN],
                [name('O'), letterO],
                [name('P'), letterP],
                [name('Q'), letterQ],
                [name('R'), letterR],
                [name('S'), letterS],
                [name('T'), letterT],
                [name('U'), letterU],
                [name('V'), letterV],
                [name('W'), letterW],
                [name('X'), letterX],
                [name('Y'), letterY],
                [name('Z'), letterZ],
                [name('确认'), sg.Button('OK')],
                ]

layout_r  = [
            [sg.Text('置换后文本')],
            [result],
            [sg.Text('置换建议')],
            [hints], 
            ]


layout = [[sg.T('置换置乱密码辅助破译器', font='_ 14', justification='c', expand_x=True)],
          [sg.Text('输入密码文件绝对路径'),sg.Input(s=40),sg.Button('upload')],
          [sg.Col(layout_l, p=0), sg.Col(layout_r, p=0)]]

window = sg.Window('Live Text Update', layout)

#----------------------------------    布局    ------------------------------------------

def count_letters(file_path):
    letter_count = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip().lower()
            for char in line:
                if char.isalpha():
                    letter_count[char] = letter_count.get(char, 0) + 1
    return letter_count

def count_bigrams(text):
    text = re.sub(r'[^a-zA-Z]', '', text).lower()
    bigrams = [text[i:i+2] for i in range(len(text)-1)]
    bigram_counts = Counter(bigrams)
    
    return bigram_counts

def letter_substitution(input_str, substitution_array):
    substitution_dict = {chr(97+i): chr(97+substitution_array[i]-1) for i in range(26)}  

    output_str = ""
    for char in input_str:
        if char.isalpha():
            if char.lower() in substitution_dict:
                if char.islower():  # 处理小写字母
                    output_str += substitution_dict[char.lower()]
                else:  # 处理大写字母
                    output_str += substitution_dict[char.lower()].upper()
            else:
                output_str += char
        else:
            output_str += char

    return output_str

def count_and_sort_letters(s):
    # 计算每个字母的频率，不区分大小写
    letter_count = {}
    for char in s:
        if char.isalpha():  # 只考虑字母
            char = char.lower()  # 将字母转换为小写
            if char in letter_count:
                letter_count[char] += 1
            else:
                letter_count[char] = 1
    
    # 按字母顺序排序
    sorted_letters = sorted(letter_count.items(), key=lambda x: x[1])
    
    # 输出每行一个字母的排序结果，形式为"a:12"
    for letter, count in sorted_letters:
        print(f"{letter}:{count}")
    
    # 将最多的11个字母存入数组
    top_11_letters = sorted(sorted_letters, key=lambda x: x[1], reverse=True)[:11]
    
    return sorted_letters, top_11_letters

def find_and_count_combinationsthe(input_str, char_t, char_e):
    pattern = re.compile(f"{re.escape(char_t)}[a-z]{re.escape(char_e)}")
    combinations = re.findall(pattern, input_str)
    
    # 使用 Counter 来统计每个组合的出现次数
    combination_counts = Counter(combinations)
    
    # 选取出现次数最多的三个组合
    top_3_combinations = combination_counts.most_common(3)
    
    return top_3_combinations

def find_and_count_combinationsthat(input_str, char_t, char_h):
    pattern = re.compile(f"{re.escape(char_t)}{re.escape(char_h)}[a-z]{re.escape(char_t)}")
    combinations = re.findall(pattern, input_str)
    
    # 使用 Counter 来统计每个组合的出现次数
    combination_counts = Counter(combinations)
    
    # 选取出现次数最多的三个组合
    top_3_combinations = combination_counts.most_common(3)
    
    return top_3_combinations

def find_and_count_combinationsand(input_str, char_a, char_dl):
    pattern = re.compile(f"{re.escape(char_a)}[a-z]{re.escape(char_dl)}")
    combinations = re.findall(pattern, input_str)
    
    # 使用 Counter 来统计每个组合的出现次数
    combination_counts = Counter(combinations)
    
    # 选取出现次数最多的三个组合
    top_3_combinations = combination_counts.most_common(3)
    
    return top_3_combinations

#----------------------------------    函数    ------------------------------------------

while True:
    event, value = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    elif event == 'OK':

        with open(value[0], 'r', encoding='utf-8') as file:
            text = file.read()

        substitution_array = [0]*26

        for i in range(26):
            if value[i+1] != "":
                substitution_array[i] = ord(value[i+1].lower()) - ord('a')+1
            else:
                substitution_array[i] = i+1

        input_str = text
        
        output_str = letter_substitution(input_str, substitution_array)

        window['-OUTPUT1-'].print(output_str)

        window['-OUTPUT1-'].update(output_str)

    elif event == 'upload':

        with open(value[0],'r', encoding='utf-8') as f:
            window['-OUTPUT1-'].print(f.read())
        
        with open(value[0], 'r', encoding='utf-8') as file:
            text = file.read()

        input_string = text
        
        sorted_letters, top_11_letters = count_and_sort_letters(input_string)

        #keys_list = list(sorted_letters.keys())

        char_e = top_11_letters[0][0]

        char_t = top_11_letters[1][0]

        char_dl1 = top_11_letters[9][0]

        char_dl2 = top_11_letters[10][0]
        
        window['-OUTPUT2-'].print('单个字母个数统计-------------------------------------------------------------')

        bigram_counts = count_bigrams(text) #两字母组合计数

        window['-OUTPUT2-'].print('两个字母组合个数统计---------------------------------------------------------')

        sorted_bigrams = sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True)[:100] #统计前几个最多的字母组合

        for bigram, count in sorted_bigrams:
            window['-OUTPUT2-'].print(f"{bigram}: {count}") #字母组合统计结果的输出


        window['-OUTPUT2-'].print('置换破译建议----------------------------------------------------------------')
        window['-OUTPUT2-'].print(char_e+'字母最多，建议置换为e')
        window['-OUTPUT2-'].print(char_t+'字母第二多，建议置换为t')

         #统计特定四个字母的组合出现次数

        window['-OUTPUT2-'].print('字母组合the个数统计---------------------------------------------------------')

        top_combinations = find_and_count_combinationsthe(input_string,char_t,char_e)

        window['-OUTPUT2-'].print('出现次数最多的三个组合是：',top_combinations)

        window['-OUTPUT2-'].print('通过the的查找确认h')
        
        #combinations_dict = find_combinationsthe(text,char_e,char_t)

        #print_top_5_combinations(combinations_dict)

        char_h = top_combinations[0][0][1]

        window['-OUTPUT2-'].print('字母组合that个数统计---------------------------------------------------------')

        top_combinations = find_and_count_combinationsthat(input_string,char_t,char_h)

        window['-OUTPUT2-'].print('出现次数最多的三个组合是：',top_combinations)

        window['-OUTPUT2-'].print('通过that查找确认a')

        char_a = top_combinations[0][0][2]
        
         # 统计特定三个字母组合出现次数

        window['-OUTPUT2-'].print('字母组合and个数统计----------------------------------------------------------')

        top_combinations = find_and_count_combinationsand(input_string,char_a,char_dl1)

        window['-OUTPUT2-'].print('出现次数最多的三个组合是：',top_combinations)

        top_combinations = find_and_count_combinationsand(input_string,char_a,char_dl2)

        window['-OUTPUT2-'].print('出现次数最多的三个组合是：',top_combinations)

        window['-OUTPUT2-'].print('由于d和l的个数相近且与其他字母相差都很大，可以通过上述and的查找确认d，l和n')

        window['-OUTPUT2-'].print('11个常见字母除了上面确定的还有r,i,s,o，将这些确认之后就可以有很大概率能寻找到一些认识的单词了')

        window['-OUTPUT2-'].print('最后附上常见双字母组合和常见连写字母组合供参考：TH HE AN RE ER IN ON AT ND ST ES EN OF TE ED OR TI HI AS TO, LL EE SS OO TT FF RR NN PP CC')
        
#----------------------------------    结束    ------------------------------------------

# 测试用文件地址        D:\projects\py projects\tongjiyangben.txt     D:\projects\py projects\codegatsby.txt

# 示例用法