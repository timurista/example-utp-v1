# the tutor will do the following
# interact with db to store and retrieve user questions
# also progress

import dataclasses
import json
import os
from dataclasses import dataclass
from uuid import uuid4

import fireworks.client
from dotenv import load_dotenv

# Use a pipeline as a high-level helper

load_dotenv()

MODEL="accounts/fireworks/models/mixtral-8x7b-instruct"
# MODEL="accounts/fireworks/models/llama-v2-7b-chat"
STATIC_QUESTION_GENERATOR_PROMPT_TEMPLATE = """
Generate a multiple choice question with 5 possible answers, and 1 correct answer. The choices should be in the form a,b,c,d,e.
The question should probe the questions understanding of the topic in machine learning {topic}.
Here's an example of the EXACT output I want you to give me. Just give me the JSON string only.
"{
    "question": "What is the difference between supervised and unsupervised learning?",
    "choices": [
        "Supervised learning is when the model is trained on labeled data, while unsupervised learning is when the model is trained on unlabeled data.",
        "Supervised learning is when the model is trained on unlabeled data, while unsupervised learning is when the model is trained on labeled data.",
        "Supervised learning is when the model is trained on labeled data, while unsupervised learning is when the model is trained on labeled data.",
        "Supervised learning is when the model is trained on unlabeled data, while unsupervised learning is when the model is trained on unlabeled data.",
        "Supervised learning is when the model is trained on labeled data, while unsupervised learning is when the model is trained on unlabeled data."
    ],
    "correct": "Supervised learning is when the model is trained on labeled data, while unsupervised learning is when the model is trained on unlabeled data."
}"
"""

@dataclass
class Question:
    question: str
    choices: list
    correct: str

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def get_client():
    fireworks.client.api_key = os.environ.get("FIREWORKS_API_KEY")
    return fireworks.client

class Session():
    def __init__(self):
        # generate session id
        self.session_id = uuid4()
        self.progress = 0
        self.current_question = None
        self.current_answer = None
        self.questions = self.load_questions()
        self.topics = [
            "Linear Regression in Supervised Learning",
            "Logistic Regression in Supervised Learning",
            "Decision Trees in Supervised Learning",
            "Dimensionality Reduction in Unsupervised Learning",
            "Clustering in Unsupervised Learning",
            "Neural Network Architectures in Deep Learning",
            "Convolutional Neural Networks in Deep Learning",
            "Backpropagation in Deep Learning",
            "Markov Decision Processes in Reinforcement Learning",
            "Q-Learning in Reinforcement Learning",
            "Policy Gradients in Reinforcement Learning",
        ]
        self.api = get_client()

    def generate_question(self, topic):
        # Implementation of generate question
        # fix key error
        prompt = STATIC_QUESTION_GENERATOR_PROMPT_TEMPLATE.replace("{topic}", topic)
        # print("prompt", prompt)
        try:
            response_generator = self.api.ChatCompletion.create(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                model=MODEL,
                stream=True
            )
            question = ""

            for chunk in response_generator:
                if chunk.choices[0].delta.content is not None:
                    question += chunk.choices[0].delta.content

            print("generated question", question)
            # make sure it ends with "}] if not there
            if question[-2:] != '"}]':
                question += '"}]'
            if question[:2] != '[{"':
                question = '[{"' + question[2:]

            json_question = json.loads(question)
            print("json_question", json_question)
            return Question(**json_question)
        except Exception as e:
            print("error", e)
            return None



    def load_questions(self):
        try:
            os.mkdir('.db')
            # create questions db if it doesn't exist
            if not os.path.exists('.db/questions.json'):
                with open('.db/questions.json', 'w') as f:
                    json.dump([], f)
        except FileExistsError:
            pass
        # load questions from db
        with open('.db/questions.json') as f:
            questions = json.load(f)
            # convert to Question objects
            questions = [Question(**q) for q in questions if q is not None and q != ""]
        return questions

    def has_questions(self):
        return len(self.questions) > 0

class PersonalTutor():
    def __init__(self):
        self.session = Session()
        self.api = get_client()

    def start_session(self):
        print("Starting Learning Session...")
        if not self.session.has_questions():
            print("No questions to review. lets make some...")
            # generate 5 questions to probe understanding
            for i in range(1):
                q = self.session.generate_question(self.session.topics[i])
                print("generated question", q)
                self.session.questions.append(q)

            # add questions to db
            with open('.db/questions.json', 'w') as f:
                # copy any existing questions
                db_questions = self.session.load_questions()
                # add the new questions to top
                self.session.questions.extend(db_questions)
                json.dump(self.session.questions, f, cls=EnhancedJSONEncoder)
        # get first question
        if not self.session.current_question:
            self.session.current_question = self.session.questions.pop(0)


    def review_progress(self):
        # Implementation of progress review
        pass

    def main_menu(self):
        # Implementation of main menu
        pass

    def get_current_question(self):
        # Implementation of get question
        return self.session.current_question
