from models.item_model import Item

import torch
import logging
import pandas as pd

from simpletransformers.question_answering import QuestionAnsweringModel, QuestionAnsweringArgs

# from haystack import Finder
# from haystack.indexing.cleaning import clean_wiki_text
# from haystack.indexing.utils import convert_files_to_dicts, fetch_archive_from_http
# from haystack.reader.farm import FARMReader
# from haystack.reader.transformers import TransformersReader
# from haystack.utils import print_answers
# from haystack.retriever.sparse import ElasticsearchRetriever
# from haystack.database.elasticsearch import ElasticsearchDocumentStore



# def populate_haystack(item: Item):
#     print(item)

#     document_store = ElasticsearchDocumentStore(host="35.202.130.14", username="", password="", index="document")

#     doc_dir = "data/article_txt_got"
#     s3_url = "https://s3.eu-central-1.amazonaws.com/deepset.ai-farm-qa/datasets/documents/wiki_gameofthrones_txt.zip"
#     fetch_archive_from_http(url=s3_url, output_dir=doc_dir)

#     dicts = convert_files_to_dicts(dir_path=doc_dir, clean_func=clean_wiki_text, split_paragraphs=True)
#     dicts_with_uuid = [dict(item, _id=str(uuid.uuid4())) for item in dicts]
#     dicts_with_uuid_and_type = [dict(item, _type="item") for item in dicts_with_uuid]
#     document_store.write_documents(dicts_with_uuid_and_type)
    
#     return item

# def ask_haystack(item: Item):
#     print(item)

#     retriever = ElasticsearchRetriever(document_store=document_store)

#     reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

#     finder = Finder(reader, retriever)

#     prediction = finder.get_answers(question=item.question, top_k_retriever=10, top_k_reader=5)
    
#     return prediction

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
    model_args.no_cache = True
    model_args.overwrite_output_dir = True
    # model_args.use_early_stopping = True
    # model_args.early_stopping_delta = 0.01
    # model_args.early_stopping_metric = "mcc"
    # model_args.early_stopping_metric_minimize = False
    # model_args.early_stopping_patience = 5
    # model_args.evaluate_during_training_steps = 1000

    kwargs ={"reprocess_input_data": False,
             "fp16":False,
             "num_train_epochs": 1,
             "save_steps": 100_000,
             "logging_steps": 100}

    cuda_available = torch.cuda.is_available()

    # Create the QuestionAnsweringModel
    model = QuestionAnsweringModel('longformer', 'outputs/longformer-large-4096-finetuned-triviaqa/', args=model_args, use_cuda=cuda_available)

    # model.train_model(train_data, eval_data=eval_data)

    # Making predictions using the model.
    to_predict = [{'context': item.context, 'qas': [{'question': item.question, 'id': '0'}]}]

    results = model.predict(to_predict)
    
    return results