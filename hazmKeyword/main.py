# ruff: noqa

import warnings

import nltk
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from hazm import SentEmbedding
from hazm import POSTagger
from hazm.corpus_readers import PersicaReader
from hazm import Normalizer
from hazm import word_tokenize
from hazm import sent_tokenize


grammers = [
    """
NP:
        {<NOUN,EZ>?<NOUN.*>}    # Noun(s) + Noun(optional)

""",
    """
NP:
        {<NOUN.*><ADJ.*>?}    # Noun(s) + Adjective(optional)

""",
]
normalizer = Normalizer()


def tokenize(text):
    normalizer = Normalizer()
    return [
        word_tokenize(sent)
        for sent in sent_tokenize(normalizer.normalize(text))
    ]


def posTagger(text, pos_model_path="../hazmKeyword/pos_tagger.model", posTaggerModel=None):
    tokens = tokenize(text)
    tagger = POSTagger(pos_model_path) if posTaggerModel is None else posTaggerModel
    return tagger.tag_sents(tokens)


def extractGrammer(tagged_text, grammer):
    keyphrase_candidate = set()
    np_parser = nltk.RegexpParser(grammer)
    trees = np_parser.parse_sents(tagged_text)
    for tree in trees:
        for subtree in tree.subtrees(
            filter=lambda t: t.label() == "NP",
        ):  # For each nounphrase
            keyphrase_candidate.add(" ".join(word for word, tag in subtree.leaves()))
    keyphrase_candidate = {kp for kp in keyphrase_candidate if len(kp.split()) <= 5}
    keyphrase_candidate = list(keyphrase_candidate)
    return keyphrase_candidate


def extractCandidates(tagged_text, grammers=grammers):
    all_candidates = set()
    for grammer in grammers:
        all_candidates.update(extractGrammer(tagged_text, grammer))
    return np.array(list(all_candidates))


def text2vec(candidates, sent2vec_model_path="../hazmKeyword/sent2vec-naab.model", sent2vecModel=None):
    sent2vec_model = (
        SentEmbedding(sent2vec_model_path) if sent2vecModel is None else sent2vecModel
    )
    candidate_vector = [[sent2vec_model[candidate] for candidate in candidates]]
    text_vector = sent2vec_model[" ".join(candidates)]
    return candidate_vector, text_vector


def vectorSimilarity(candidates_vector, text_vector, norm=True):
    candidate_sim_text = cosine_similarity(
        candidates_vector[0],
        text_vector.reshape(1, -1),
    )
    candidate_sim_candidate = cosine_similarity(candidates_vector[0])
    if norm:
        candidates_sim_text_norm = candidate_sim_text / np.max(candidate_sim_text)
        candidates_sim_text_norm = 0.5 + (
            candidates_sim_text_norm - np.average(candidates_sim_text_norm)
        ) / np.std(candidates_sim_text_norm)
        np.fill_diagonal(candidate_sim_candidate, np.NaN)
        candidate_sim_candidate_norm = candidate_sim_candidate / np.nanmax(
            candidate_sim_candidate,
            axis=0,
        )
        candidate_sim_candidate_norm = 0.5 + (
            candidate_sim_candidate_norm
            - np.nanmean(candidate_sim_candidate_norm, axis=0)
        ) / np.nanstd(candidate_sim_candidate_norm, axis=0)
        return candidates_sim_text_norm, candidate_sim_candidate_norm
    return candidate_sim_text, candidate_sim_candidate


def embedRankExtraction(
    all_candidates,
    candidate_sim_text,
    candidate_sim_candidate,
    keyword_num=10,
    beta=0.8,
):
    if len(all_candidates) < keyword_num:
        warnings.warn(
            (
                f"total number of keyword candidates is {len(all_candidates)}, which is"
                " lower than your request keyword_num"
            ),
        )

    N = int(min(len(all_candidates), keyword_num))

    selected_candidates = []
    unselected_candidates = list(range(len(all_candidates)))
    best_candidate = np.argmax(candidate_sim_text)
    selected_candidates.append(best_candidate)
    unselected_candidates.remove(best_candidate)

    for _i in range(N - 1):
        selected_vec = np.array(selected_candidates)
        unselected_vec = np.array(unselected_candidates)

        unselected_candidate_sim_text = candidate_sim_text[unselected_vec, :]

        dist_between = candidate_sim_candidate[unselected_vec][:, selected_vec]

        if dist_between.ndim == 1:
            dist_between = dist_between[:, np.newaxis]

        best_candidate = np.argmax(
            beta * unselected_candidate_sim_text
            - (1 - beta) * np.max(dist_between, axis=1).reshape(-1, 1),
        )
        best_index = unselected_candidates[best_candidate]
        selected_candidates.append(best_index)
        unselected_candidates.remove(best_index)
    return all_candidates[selected_candidates].tolist()


def extractKeyword(candidates, keyword_num=5, sent2vecModel=None):
    candidates_vector, text_vector = text2vec(candidates, sent2vecModel=sent2vecModel)
    candidate_sim_text_norm, candidate_sim_candidate_norm = vectorSimilarity(
        candidates_vector,
        text_vector,
    )
    return embedRankExtraction(
        candidates,
        candidate_sim_text_norm,
        candidate_sim_candidate_norm,
        keyword_num,
    )


def embedRank(text, keyword_num, sent2vecModel=None, posTaggerModel=None):
    token_tag = posTagger(text, posTaggerModel=posTaggerModel)
    candidates = extractCandidates(token_tag)
    return extractKeyword(candidates, keyword_num, sent2vecModel=sent2vecModel)


# if __name__ == "__main__":
#     persikaReader = PersicaReader("persica.csv")
#     text = next(persikaReader.texts())
#     keyword_num = 10
#     keywords = embedRank(text, keyword_num)

# keyword_num = 3
# keywords = embedRank("اخراج کارمندان معترض به همکاری با رژیم صهیونیستی توسط گوگلگوگل اعلام کرد: ۲۸ کارمندش را پس از شرکت در اعتراضات علیه قرارداد ابر رایانشی شرکت با رژیم صهیونیستی اخراج کرد.به گزارش خبرگزاری تسنیم، به نقل از رویترز، گوگل در بیانیه‌ای اعلام کرد تعدادی از کارمندان معترض وارد برخی دفاتر این شرکت شدند و کار را مختل کردند. در متن بیانیه آمده است: این افراد به طور فیزیکی فعالیت کارمندان دیگر را مختل کردند و اجازه ندادند آنها به واحدهای ما دسترسی یابند. این امر نقض واضح سیاست‌های ما و رفتاری کاملاً غیرقابل قبول است.این شرکت آمریکایی در آخر اشاره کرده بود تحقیقات جداگانه به اخراج 28 کارمند منجر شد. گوگل اعلام کرد همچنان به تحقیق ادامه می‌دهد و اقدامات مورد نیاز را انجام خواهد داد.کارمندان گوگل که عضو کمپین «نه به فناوری برای آپارتاید» هستند، در بیانیه‌ای که در پلتفرم مدیوم منتشر شده، اعلام کردند چنین اقدامی انتقام جویانه است و برخی کارمندان که به طور مستقیم در اعتراضات روز سه شنبه در دفاتر گوگل شرکت نکرده بودند، جزو کارمندان اخراجی هستند. در بخشی از بیانیه آنها آمده است: کارمندان گوگل حق اعتراض مسالمت آمیز درباره شرایط و وضعیت کار را دارند.معترضان اعلام کرده‌اند پروژه Nimbus از توسعه ابزارهای نظامی توسط رژیم صهیونیستی پشتیبانی می‌کند.طبق این قرارداد 1.2 میلیارد دلاری که در 2021 میلادی بسته شده، گوگل و آمازون سرویس‌های ابر رایانشی را برای رژیم صهیونیستی فراهم می‌کنند.اعتراضات کارمندان گوگل پدیده‌ای جدید نیست. در سال 2018 میلادی کارمندان این شرکت موفق شدند گوگل را وادار کنند قراردادی با ارتش آمریکا به نام پروژه میون لغو کند.", keyword_num)

# print(keywords)

