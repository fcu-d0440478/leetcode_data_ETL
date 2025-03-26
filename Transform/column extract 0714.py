import json
import pickle
import html2text
import re
import pandas as pd

# 檔案路徑
source_file = "20210712"
output_file = f"{source_file}/{source_file} Leetcode.xlsx"

# 讀取題目基準List
with open(f"./{source_file}/problemset_lst.pickle", "rb") as f:
    problem_sets = pickle.load(f)

# 每一題(ROW)的資料Append進這個DataFrame
excel_output = pd.DataFrame()

# HTML to Text Parser
parser = html2text.HTML2Text()
parser.ignore_links = True

# 每一題的FOR迴圈
for question in problem_sets:
    """ ❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄ 基本資料獲得，供後續讀檔依據 ❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄ """
    # QuestionId
    question_id = question["questionId"]
    # QuestionFrontendId
    frontend_question_id = question["frontendQuestionId"]
    # Title
    question__title = question["title"]
    # titleSlug
    titleSlug = question["titleSlug"]
    # frequency
    frequency = question["freqBar"]
    # difficulty
    difficulty = question["difficulty"]
    # hasSolution
    has_solution = question["hasSolution"]
    # hasVideoSolution
    has_video_solution = question["hasVideoSolution"]
    """ ❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄ 基本資料獲得，供後續讀檔依據 ❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄❄ """



    """ ✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩ 其他JSON檔案讀取 ✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩ """
    # 檔案名稱，EX:1 two-sum
    filename = f"{question_id} {titleSlug}"

    questionData = json.load(
        open((f"{source_file}/{filename}/questionData.json"), "r", encoding="utf-8")
    )
    questionTags = json.load(
        open((f"{source_file}/{filename}/questionTags.json"), "r", encoding="utf-8")
    )
    questionTopicCount = json.load(
        open((f"{source_file}/{filename}/questionTopicCount.json"), "r", encoding="utf-8")
    )
    discussQuestionTopicTags = json.load(
        open((f"{source_file}/{filename}/discussQuestionTopicTags.json"), "r", encoding="utf-8")
    )

    # 有提供解答的題目才會有這些JSON
    if (has_solution):
        QuestionNote = json.load(
        open((f"{source_file}/{filename}/QuestionNote.json"), "r", encoding="utf-8")
        )
        DiscussTopic = json.load(
            open((f"{source_file}/{filename}/DiscussTopic.json"), "r", encoding="utf-8")
        )
    """ ✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩ 其他JSON檔案讀取 ✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩✩ """



    """ ✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯ 從JSON檔案提取欄位資訊 ✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯ """
    # IsPaidOnly
    isPaidOnly = questionData["data"]["question"]["isPaidOnly"]
    # status裡面包含 solution、accept、submission
    status_json = json.loads(questionData["data"]["question"]["stats"])
    # Acceptance rate 提交率
    acRate = status_json["acRate"]
    acRate = "{:.1f}".format(float(acRate.strip('%')))
    # totalAcceptedRaw
    total_accepted_raw = status_json["totalAcceptedRaw"]
    # totalSubmissionRaw
    total_submission_raw = status_json["totalSubmissionRaw"]    
    # likes
    likes = questionData["data"]["question"]["likes"]
    # dislikes
    dislikes = questionData["data"]["question"]["dislikes"]
    # likes_ratio
    likes_ratio = 0
    if (likes==0 and dislikes ==0):
        likes_ratio = None
    else:
        likes_ratio = likes/(likes+dislikes)
    # Number of Discuusion
    discuss_num = questionTopicCount["data"]["questionTopicsList"]["totalNum"]
    # 有提供解法的情況下
    if has_solution:
        # SolutionCount
        regex = re.compile(r'#### Approach [0-9]:')
        match = regex.findall(QuestionNote["data"]["question"]["solution"]["content"])
        SolutionCount = len(match)
        # SolutionTopicId
        regex = re.compile(r'"topicId": (\d+)')
        match = regex.search(QuestionNote["data"]["question"]["article"])
        solutionTopicId = match.group(1)
        # IsSolutionPaid
        IsSolutionPaid = QuestionNote["data"]["question"]["solution"]["paidOnly"]
        # Average Rating for solution
        rating_average = QuestionNote["data"]["question"]["solution"]["rating"][
            "average"
        ]
        # Rating votes for solution
        rating_count = QuestionNote["data"]["question"]["solution"]["rating"][
            "count"
        ]
        # SolutionViewCount
        SolutionViewCount = DiscussTopic["data"]["topic"]["viewCount"]
        # Comments below solution
        CommentsBelowSolution = DiscussTopic["data"]["topic"]["topLevelCommentCount"]
    else:
        SolutionCount = 0
        solutionTopicId = 0
        IsSolutionPaid = None
        rating_average = None
        rating_count = None
        SolutionViewCount = None
        CommentsBelowSolution = None
    # SimilarQuestions
    regex = re.compile(r'"title": ("[\w| |-]*")')
    match = regex.findall(questionData["data"]["question"]["similarQuestions"])
    SimilarQuestions = f"[{', '.join(match)}]"
    # TopicTags
    tag_json = questionData["data"]["question"]["topicTags"]
    tag_list = []
    for i in tag_json:
        tag_list.append(i["name"])
    TopicTags = str(tag_list)
    # DiscussTopicTags
    discuss_topic_tag_json = discussQuestionTopicTags["data"]["discussQuestionTopicTags"]
    discuss_topic_tag_list = []
    for i in discuss_topic_tag_json:
        discuss_topic_tag_list.append([i["name"], i["numTopics"]])
    DiscussTopicTags = str(discuss_topic_tag_list)

    # Hints提示的部分
    hints = questionData["data"]["question"]["hints"] #RAW
    hints_length = len(hints)
    hints_text = [] #text only
    for hint in hints:
        hints_text.append(parser.handle(hint))

    # content
    content = questionData["data"]["question"]["content"] #RAW
    content_text = parser.handle(content)
    

    """ ✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯ 從JSON檔案提取欄位資訊 ✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯✯ """



    """ ************************************************ ONE ROW ************************************************ """

    one_row = {
        "QuestionId": question_id,
        "QuestionFrontendId": frontend_question_id,
        "Title": question__title,
        "TitleSlug": titleSlug,
        "IsPaidOnly": isPaidOnly,
        "Acceptance Rate": acRate,
        "Difficulty": difficulty,
        "Frenquency": frequency,
        "Likes": likes,
        "Dislikes": dislikes,
        "Likes_ratio": likes_ratio,
        "Accepted": total_accepted_raw,
        "Submission": total_submission_raw,
        "Number of Discussion": discuss_num,
        "Number of Hints": hints_length,
        "HasSolution": has_solution,
        "HasVideoSolution": has_video_solution,
        "SolutionCount": SolutionCount,
        "SolutionTopicId": solutionTopicId,
        "IsSolutionPaid": IsSolutionPaid,
        "Rating_average": rating_average,
        "Rating_count": rating_count,
        "SolutionViewCount": SolutionViewCount,
        "Comments below solution": CommentsBelowSolution,
        "SimilarQuestions": SimilarQuestions,
        "TopicTags": TopicTags,
        "DiscussTopicTag": DiscussTopicTags,
        "Content": content_text,
        "Hints_text": hints_text,
    }
    excel_output = excel_output.append(one_row, ignore_index=True)

    """ ************************************************ ONE ROW ************************************************ """
excel_output['IsPaidOnly'] = excel_output['IsPaidOnly'].astype('bool')
excel_output['HasSolution'] = excel_output['HasSolution'].astype('bool')
excel_output['HasVideoSolution'] = excel_output['HasVideoSolution'].astype('bool')
excel_output['IsSolutionPaid'] = excel_output['IsSolutionPaid'].astype('bool')

excel_output['Acceptance Rate'] = excel_output['Acceptance Rate'].astype('float')

excel_output['QuestionId'] = excel_output['QuestionId'].astype('int')
excel_output['QuestionFrontendId'] = excel_output['QuestionFrontendId'].astype('int')
excel_output['SolutionTopicId'] = excel_output['SolutionTopicId'].astype('int')

excel_output['Difficulty'] = excel_output['Difficulty'].astype('category')

excel_output.to_excel(output_file, sheet_name='leetcode data')