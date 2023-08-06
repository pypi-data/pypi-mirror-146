from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from string import punctuation
from ingestor.common.constants import TITLE, SYNOPSIS, COMBINED_FEATURES, CONTENT_ID, LABEL, CONTENT_CORE_ID, \
    CONTENT_CORE, \
    PROPERTIES, CONTENT_CORE_SYNOPSIS,TAGS, TAGS_ID, TAGS_DESCRIPTION, DEFAULT_TAGS_DESCRIPTION, ADDITIONAL_STOPWORDS,\
    CONTENT_TAGS_DESCRIPTION_CSV, CONTENT_CC_SYNOPSIS_CSV
from ingestor.content_profile.config import HAS_TAG
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from collections import OrderedDict
import pandas as pd
from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
import pickle

nltk.download('stopwords')

from graphdb.schema import Node


def cluster_data_to_df(cluster_list):
    pd.set_option("display.max_columns", None)

    df_list = []
    for index, clusters in enumerate(cluster_list):
        dataframe_cluster = []
        for data in clusters:
            df_cluster = DataFrame.from_dict(data)
            dataframe_cluster.append(df_cluster)
        dataframe_cluster = pd.concat(dataframe_cluster)
        dataframe_cluster = dataframe_cluster.reset_index(drop=True)
        df_list.append(dataframe_cluster)
    return df_list


def cluster_data_to_single_df(clusters):
    pd.set_option("display.max_columns", None)

    dataframe_cluster = []
    for data in clusters:
        df_cluster = DataFrame.from_dict(data)
        dataframe_cluster.append(df_cluster)
    dataframe_cluster = pd.concat(dataframe_cluster)
    dataframe_cluster = dataframe_cluster.reset_index(drop=True)

    return dataframe_cluster


def get_content_core_synopsis_df(graph, content_core_content_df, id_content):
    if id_content > 2 :
        content_core_synopsis_df = pd.read_csv(CONTENT_CC_SYNOPSIS_CSV)

        content_core_id_list = content_core_content_df[CONTENT_ID].drop_duplicates().tolist()
        content_id_list = content_core_content_df[CONTENT_ID].drop_duplicates().tolist()
        content_core_synopsis_list = []

        for id_cc in content_core_id_list:
            static_node_cc_synopsis = Node(**{LABEL: CONTENT_CORE_SYNOPSIS, PROPERTIES: {CONTENT_CORE_ID: id_cc}})
            content_core_synopsis = graph.find_node(static_node_cc_synopsis)
            if len(content_core_synopsis) == 0:
                synopsis_cc = ''
                content_core_synopsis_list.append(synopsis_cc)
            elif len(content_core_synopsis) > 0:
                content_core_synopsis = content_core_synopsis[0]
                synopsis_cc = content_core_synopsis.properties[CONTENT_CORE_SYNOPSIS]
                content_core_synopsis_list.append(synopsis_cc)

        temp_content_core_synopsis_df = pd.DataFrame(list(zip(content_id_list, content_core_synopsis_list)),
                                                     columns=[CONTENT_ID, CONTENT_CORE_SYNOPSIS])
        content_core_synopsis_df = pd.concat([content_core_synopsis_df,temp_content_core_synopsis_df],axis=0)
        content_core_synopsis_df = content_core_synopsis_df.drop_duplicates(subset=[CONTENT_ID])
        content_core_synopsis_df = content_core_synopsis_df.reset_index(drop=True)
        content_core_synopsis_df.to_csv(CONTENT_CC_SYNOPSIS_CSV, index=False)
    else :
        content_core_id_list = content_core_content_df[CONTENT_ID].drop_duplicates().tolist()
        content_id_list = content_core_content_df[CONTENT_ID].drop_duplicates().tolist()
        content_core_synopsis_list = []

        for id_cc in content_core_id_list:
            static_node_cc_synopsis = Node(**{LABEL: CONTENT_CORE_SYNOPSIS, PROPERTIES: {CONTENT_CORE_ID: id_cc}})
            content_core_synopsis = graph.find_node(static_node_cc_synopsis)
            if len(content_core_synopsis) == 0:
                synopsis_cc = ''
                content_core_synopsis_list.append(synopsis_cc)

        content_core_synopsis_df = pd.DataFrame(list(zip(content_id_list, content_core_synopsis_list)),
                                                columns=[CONTENT_ID, CONTENT_CORE_SYNOPSIS])
        content_core_synopsis_df.to_csv(CONTENT_CC_SYNOPSIS_CSV,index=False)

    return content_core_synopsis_df


def get_tags_df(graph, tags_content_df):
    id_content = tags_content_df[CONTENT_ID][0]
    if id_content > 2:
        tag_df = pd.read_csv(CONTENT_TAGS_DESCRIPTION_CSV)
        content_id_list = tags_content_df[CONTENT_ID].tolist()
        tags_id_list = tags_content_df[TAGS_ID].tolist()
        tags_description_list = []
        for id_tag in tags_id_list:
            static_node_tag = Node(**{LABEL: TAGS, PROPERTIES: {TAGS_ID: id_tag}})
            tag_node = graph.find_node(static_node_tag)[0]
            tags_description = tag_node.properties[TAGS_DESCRIPTION]
            tags_description_list.append(tags_description)
        temp_tag_df = pd.DataFrame(list(zip(content_id_list, tags_description_list)), columns=[CONTENT_ID, TAGS_DESCRIPTION])
        temp_tag_df = temp_tag_df.fillna(DEFAULT_TAGS_DESCRIPTION)
        temp_tag_df = temp_tag_df.groupby([CONTENT_ID])[TAGS_DESCRIPTION].apply(','.join).reset_index()
        tag_df = pd.concat([tag_df,temp_tag_df],axis=0)
        tag_df = tag_df.drop_duplicates(subset=[CONTENT_ID])
        tag_df = tag_df.reset_index(drop=True)
        tag_df.to_csv(CONTENT_TAGS_DESCRIPTION_CSV,index=False)
    else:
        content_id_list = tags_content_df[CONTENT_ID].tolist()
        tags_id_list = tags_content_df[TAGS_ID].tolist()
        tags_description_list = []
        for id_tag in tags_id_list:
            static_node_tag = Node(**{LABEL: TAGS, PROPERTIES: {TAGS_ID: id_tag}})
            tag_node = graph.find_node(static_node_tag)[0]
            tags_description = tag_node.properties[TAGS_DESCRIPTION]
            tags_description_list.append(tags_description)
        tag_df = pd.DataFrame(list(zip(content_id_list, tags_description_list)), columns=[CONTENT_ID, TAGS_DESCRIPTION])
        tag_df = tag_df.groupby([CONTENT_ID])[TAGS_DESCRIPTION].apply(','.join).reset_index()
        tag_df.to_csv(CONTENT_TAGS_DESCRIPTION_CSV,index=False)

    return tag_df, id_content


def combine_features(df, graph, tags_content_df, content_core_content_df):

    final_df = df
    tag_df, id_content = get_tags_df(graph, tags_content_df)
    content_core_synopsis_df= get_content_core_synopsis_df(graph, content_core_content_df, id_content)
    final_df = pd.merge(final_df, content_core_synopsis_df, on=CONTENT_ID)
    final_df = pd.merge(final_df, tag_df, on=CONTENT_ID, how='left')
    final_df = final_df.fillna('')
    final_df[SYNOPSIS] = final_df[SYNOPSIS].replace(['0'], '')
    final_df[COMBINED_FEATURES] = final_df[TITLE] + "," + final_df[SYNOPSIS] + "," + final_df[CONTENT_CORE_SYNOPSIS] + \
                                  "," + final_df[TAGS_DESCRIPTION]

    return final_df

def create_tfidf_df(df):
    # PREPROCESS THE COMBINED FEATURES
    nonstop_words = []
    non_punctuation_stc = []
    factory = StopWordRemoverFactory()
    stop_words = stopwords.words('indonesian')
    stopword_sastrawi = factory.get_stop_words()
    stop_words = stop_words + stopword_sastrawi + ADDITIONAL_STOPWORDS

    df[COMBINED_FEATURES] = [x.lower() for x in df[COMBINED_FEATURES]]
    df[COMBINED_FEATURES] = [x.strip() for x in df[COMBINED_FEATURES]]
    df[COMBINED_FEATURES] = [x.replace(',', ' ') for x in df[COMBINED_FEATURES]]
    df[COMBINED_FEATURES] = (df[COMBINED_FEATURES].str.split()
                             .apply(lambda x: OrderedDict.fromkeys(x).keys()).str.join(' '))
    df[COMBINED_FEATURES] = [x.split() for x in df[COMBINED_FEATURES]]
    remove_table = str.maketrans("", "", punctuation)

    for stc in df[COMBINED_FEATURES]:
        words = [x.translate(remove_table) for x in stc]
        words2 = []
        for w in words:
            w = [x for x in w if x.isalnum()]
            w = "".join(w)
            words2.append(w)

        non_punctuation_stc.append(words2)

    df[COMBINED_FEATURES] = non_punctuation_stc

    for stc in df[COMBINED_FEATURES]:
        words = [x for x in stc if x not in stop_words]

        nonstop_words.append(words)

    df[COMBINED_FEATURES] = nonstop_words
    df[COMBINED_FEATURES] = [" ".join(x) for x in df[COMBINED_FEATURES]]

    # BUILD TFIDF MATRIX
    text_content = df[COMBINED_FEATURES]
    vector = TfidfVectorizer(lowercase=True, use_idf=True, norm=u'l2', smooth_idf=True)
    tfidf_matrix = vector.fit_transform(text_content)

    # Transform to TFIDF Dataframe
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vector.get_feature_names_out())

    tfidf_df.index = df[CONTENT_ID]
    return tfidf_df


def calculate_cosine_similarity(list_tfidf_df):
    list_dict_similarity = []
    for tfidf_df in list_tfidf_df:
        cs_matrix = cosine_similarity(tfidf_df)
        cs_df = pd.DataFrame(cs_matrix, index=tfidf_df.index, columns=tfidf_df.index)
        content_id_list = list(cs_df.index)
        list_of_similarity = []
        for content_id in content_id_list:
            cosine_similarity_series = cs_df.loc[content_id]
            if isinstance(cosine_similarity_series, pd.DataFrame):
                cosine_similarity_series = cosine_similarity_series.head(1)
                cosine_similarity_series = cosine_similarity_series.iloc[0, :]
                cosine_similarity_series = cosine_similarity_series.sort_values(ascending=False)
                cosine_similarity_series = cosine_similarity_series.drop(labels=content_id)
                cosine_similarity_dict = cosine_similarity_series.to_dict()
                list_of_similarity.append(cosine_similarity_dict)
            else:
                cosine_similarity_series = cosine_similarity_series.sort_values(ascending=False)
                cosine_similarity_series = cosine_similarity_series[1:]
                cosine_similarity_dict = cosine_similarity_series.to_dict()
                list_of_similarity.append(cosine_similarity_dict)
        dict_similarity = dict(zip(content_id_list, list_of_similarity))
        list_dict_similarity.append(dict_similarity)
    return list_dict_similarity


def generate_new_features(df_list, graph, tags_content_df, content_core_content_df):
    list_new_df_result = []
    for df in df_list:
        df = combine_features(df, graph, tags_content_df, content_core_content_df)
        list_new_df_result.append(df)

    return list_new_df_result


def generate_tfidf_matrix(df_new_list):
    list_tfidf_matrix = []
    for df in df_new_list:
        tfidf_matrix = create_tfidf_df(df)
        list_tfidf_matrix.append(tfidf_matrix)

    return list_tfidf_matrix


def calculate_single_cosine_similarity(all_content_tfidf_df):
    cs_matrix = cosine_similarity(all_content_tfidf_df)
    cs_df = pd.DataFrame(cs_matrix, index=all_content_tfidf_df.index, columns=all_content_tfidf_df.index)
    content_id_list = list(cs_df.index)
    list_of_similarity = []
    for content_id in content_id_list:
        cosine_similarity_series = cs_df.loc[content_id]
        cosine_similarity_series = cosine_similarity_series.sort_values(ascending=False)
        cosine_similarity_series = cosine_similarity_series[1:]
        cosine_similarity_dict = cosine_similarity_series.to_dict()
        list_of_similarity.append(cosine_similarity_dict)
    dict_similarity = dict(zip(content_id_list, list_of_similarity))
    return dict_similarity

