import logging
import os
import shutil
import uuid
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import UploadFile, File, Form

from rest_api.config import DB_HOST, DB_PORT, DB_USER, DB_PW, DB_INDEX, ES_CONN_SCHEME, TEXT_FIELD_NAME, \
    SEARCH_FIELD_NAME, FILE_UPLOAD_PATH, EMBEDDING_DIM, EMBEDDING_FIELD_NAME, EXCLUDE_META_DATA_FIELDS, VALID_LANGUAGES, \
    FAQ_QUESTION_FIELD_NAME, REMOVE_NUMERIC_TABLES, REMOVE_WHITESPACE, REMOVE_EMPTY_LINES, REMOVE_HEADER_FOOTER, EMBEDDING_MODEL_PATH, EMBEDDING_MODEL_FORMAT, USE_GPU, RETRIEVER_TYPE
from haystack.database.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.dense import DensePassageRetriever


logger = logging.getLogger(__name__)
router = APIRouter()


document_store = ElasticsearchDocumentStore(
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USER,
    password=DB_PW,
    index=DB_INDEX,
    scheme=ES_CONN_SCHEME,
    ca_certs=False,
    verify_certs=False,
    text_field=TEXT_FIELD_NAME,
    search_fields=SEARCH_FIELD_NAME,
    embedding_dim=EMBEDDING_DIM,
    embedding_field=EMBEDDING_FIELD_NAME,
    excluded_meta_data=EXCLUDE_META_DATA_FIELDS,  # type: ignore
    faq_question_field=FAQ_QUESTION_FIELD_NAME,
)

retriever = DensePassageRetriever(
    document_store=document_store,
    embedding_model=EMBEDDING_MODEL_PATH,
    do_lower_case=True,
    use_gpu=USE_GPU
)

@router.post("/update-embeddings")
def upload_file_to_document_store():
    document_store.update_embeddings(retriever)
    return "Successfully updated embeddings."
