# the tutor will do the following
# interact with db to store and retrieve user questions
# also progress

import json
import os
from dataclasses import dataclass
from uuid import uuid4

import fireworks.client
from dotenv import load_dotenv

# Use a pipeline as a high-level helper

load_dotenv()

MODEL="accounts/fireworks/models/mixtral-8x7b-instruct"
STATIC_QUESTION_GENERATOR_PROMPT_TEMPLATE = """
Generate a multiple choice question with 5 possible answers, and 1 correct answer. The choices should be in the form a,b,c,d,e.g.
The question should probe the questions understanding of the topic in machine learning {topic}.
Here's an example and the output should be in a json:
{
    "question": "What is the difference between supervised and unsupervised learning?",
    "choices": [
        "Supervised learning is when the model is trained on labeled data, while unsupervised learning is when the model is trained on unlabeled data.",
        "Supervised learning is when the model is trained on unlabeled data, while unsupervised learning is when the model is trained on labeled data.",
        "Supervised learning is when the model is trained on labeled data, while unsupervised learning is when the model is trained on labeled data.",
        "Supervised learning is when the model is trained on unlabeled data, while unsupervised learning is when the model is trained on unlabeled data.",
        "Supervised learning is when the model is trained on labeled data, while unsupervised learning is when the model is trained on unlabeled data."
    ],
    "correct_answer": "Supervised learning is when the model is trained on labeled data, while unsupervised learning is when the model is trained on unlabeled data."
}
"""

@dataclass
class Question:
    question: str
    choices: list
    correct_answer: str

def get_client():
    fireworks.client.api_key = os.environ.get("FIREWORKS_API_KEY")
    mixtral_client = fireworks.client
    return mixtral_client

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
        response = self.api.Completion.create(
            prompt=prompt,
            model=MODEL,
            tokens=5000,
        )
        print("response", response)
        question = response.choices[0].text
        print("generated question", question)
        json_question = json.loads(question)
        return Question(**json_question)


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
            for i in range(5):
                q = self.session.generate_question(self.session.topics[i])
                self.session.questions.append(q)


    def review_progress(self):
        # Implementation of progress review
        pass

    def main_menu(self):
        # Implementation of main menu
        pass

    def get_current_question(self):
        # Implementation of get question
        pass
