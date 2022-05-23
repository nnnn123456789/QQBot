import random

current_question = None
question_pool = []


class question:
    def __init__(self, prompt, ans):
        self.prompt = prompt
        self.ans = ans
    

    def verify(self, solution):
        return (solution.strip() == self.ans)

def quiz_initial():
    global question_pool
    #autoans_pool = []
    f = open("quiz.txt","r", encoding='utf8')
    lines = f.readlines()
    #print(lines)
    f.close()
    for line in lines:
        l = line[:-1].split('\t')
        if not len(l) == 2:
            continue
        question_pool.append(question(l[0], l[1]))
    #print(question_pool)



def get_random_question():
    global question_pool
    n = len(question_pool)
    if n == 0:
        quiz_initial()
        n = len(question_pool)
    random.seed()
    s = random.randrange(0,n)
    q = question_pool[s]
    print(q.prompt)
    return q



def set_current_question(ques = None):
    if ques == None:
        ques = get_random_question()
    #print(ques)
    global current_question
    current_question = ques


def get_current_solution():
    if current_question == None:
        set_current_question()
    return current_question.ans


def get_current_prompt():
    if current_question == None:
        set_current_question()
    return current_question.prompt


def try_a_solution(solution):
    ans = get_current_solution()
    if solution.strip() == ans :
        set_current_question()
        return True
    else:
        return False





#the following codes run on qqbot

def quiz(args, groupid, qqid):

    if(not len(args) == 2):
        return "[CQ:at,qq=%d]参数错误, 请重试" %(qqid)
    
    this_ans = str(args[1])

    ans_ret = try_a_solution(this_ans)

    prompt = get_current_prompt()

    leading = ""

    if ans_ret :
        leading = ("恭喜[CQ:at,qq=%d]回答正确!下一道题:\n" % qqid)
    else:
        leading = ("[CQ:at,qq=%d]答的不对!当前问题是\n" % qqid)
    
    return "%s%s" % (leading, prompt)
    


