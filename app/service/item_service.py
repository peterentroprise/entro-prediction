from models.item_model import Item

import logging

import pandas as pd
from simpletransformers.question_answering import QuestionAnsweringModel, QuestionAnsweringArgs

def answer_question(item: Item):
    print(item)

    train_data = [
        {
            "context": "Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24–10 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levis Stadium in the San Francisco Bay Area at Santa Clara, California. As this was the 50th Super Bowl, the league emphasized the golden anniversary with various gold-themed initiatives, as well as temporarily suspending the tradition of naming each Super Bowl game with Roman numerals (under which the game would have been known as Super Bowl L), so that the logo could prominently feature the Arabic numerals 50.",
            "qas": [
                {
                    "id": "00001",
                    "is_impossible": False,
                    "question": "Who is the new champion?",
                    "answers": [  {
                            "text": "Denver Broncos",
                            "answer_start": 178,
                        }],
                },
                {
                    "id": "00002",
                    "is_impossible": False,
                    "question": "What year was Super Bowl 50?",
                    "answers": [  {
                            "text": "2016",
                            "answer_start": 347,
                        }],
                },
            ],
        },
    ]

    eval_data = [
        {
            "context": "Super Bowl 50 was an American football game to determine the champion of the National Football League (NFL) for the 2015 season. The American Football Conference (AFC) champion Denver Broncos defeated the National Football Conference (NFC) champion Carolina Panthers 24–10 to earn their third Super Bowl title. The game was played on February 7, 2016, at Levis Stadium in the San Francisco Bay Area at Santa Clara, California. As this was the 50th Super Bowl, the league emphasized the golden anniversary with various gold-themed initiatives, as well as temporarily suspending the tradition of naming each Super Bowl game with Roman numerals (under which the game would have been known as Super Bowl L), so that the logo could prominently feature the Arabic numerals 50.",
            "qas": [
                {
                    "id": "00001",
                    "is_impossible": False,
                    "question": "Who is the new champion?",
                    "answers": [  {
                            "text": "Denver Broncos",
                            "answer_start": 178,
                        }],
                },
                {
                    "id": "00002",
                    "is_impossible": False,
                    "question": "What year was Super Bowl 50?",
                    "answers": [  {
                            "text": "2016",
                            "answer_start": 347,
                        }],
                },
            ],
        },
    ]

    # define model args
    model_args = QuestionAnsweringArgs()
    model_args.num_train_epochs = 5
    model_args.reprocess_input_data = True
    model_args.overwrite_output_dir = True
    # model_args.use_early_stopping = True
    # model_args.early_stopping_delta = 0.01
    # model_args.early_stopping_metric = "mcc"
    # model_args.early_stopping_metric_minimize = False
    # model_args.early_stopping_patience = 5
    # model_args.evaluate_during_training_steps = 1000

    # Create the QuestionAnsweringModel
    model = QuestionAnsweringModel('distilbert', 'distilbert-base-uncased-distilled-squad', args=model_args, use_cuda=False)

    # model.train_model(train_data, eval_data=eval_data)

    # Making predictions using the model.
    to_predict = [{'context': item.context, 'qas': [{'question': item.question, 'id': '0'}]}]

    results = model.predict(to_predict)
    
    return results