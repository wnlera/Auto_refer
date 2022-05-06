from flask import Flask, url_for, render_template
from urllib.parse import unquote
import client_elastic
import json
import os
import re

app = Flask(__name__, static_folder="static", static_url_path="")


search_stats = {"key": [], "found_sentences": []}
n = 0

@app.route("/", methods=["GET"])
def main_page():
    print("!")
    return render_template("main_page.html")

@app.route('/search/<request_str>', methods=["GET"])
def get_review(request_str):
    print(request_str)
    request_str = unquote(request_str)
    print(request_str)
    search_result = client_elastic.search_elastic(request_str)
    review = client_elastic.create_review(search_result)
    print(review)
    return review



# TODO Не все ссылки распознаются правильно
# TODO Убирать предложения не начинающиеся с заглавной буквы и оканчивающиейся на точку

