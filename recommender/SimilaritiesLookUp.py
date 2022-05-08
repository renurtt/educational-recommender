from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

from recommender.models import User


class SimilaritiesLookUp:

    @staticmethod
    def create_similarity_matrix(new_description, overall_descriptions):
        # Append the new description to the overall set.
        # overall_descriptions.append(new_description)
        overall_descriptions = pd.concat([overall_descriptions, new_description], ignore_index=True)
        # print(overall_descriptions)
        # Define a tfidf vectorizer and remove all stopwords.
        tfidf = TfidfVectorizer(stop_words="english")
        # Convert tfidf matrix by fitting and transforming the data.
        tfidf_matrix = tfidf.fit_transform(overall_descriptions)
        # calculating the cosine similarity matrix.
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        # print('cosine_sim = ', cosine_sim)
        return cosine_sim

    @staticmethod
    def get_recommendations(data, new_description, overall_descriptions):
        # create the similarity matrix
        cosine_sim = SimilaritiesLookUp.create_similarity_matrix(new_description, overall_descriptions)
        # Get pairwise similarity scores of all the students with new student.
        sim_scores = list(enumerate(cosine_sim[-1][:-1]))
        # Sort the descriptions based on similarity score.
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # print(sim_scores)
        # Get the scores of top 10 descriptions.
        sim_scores = sim_scores
        # Get the student indices.
        indices = [i[0] for i in sim_scores]
        return pd.concat(
            [data.iloc[indices], pd.Series([i[1] for i in sim_scores], name='score', index=[i[0] for i in sim_scores])],
            axis=1, ignore_index=False)

    @staticmethod
    def get_similarities(target_user_sill_set, other_users, threshold):
        # new_desc = pd.Series('c#_proficient java_low')
        # data = pd.DataFrame.from_dict(
        #     {
        #         'col_2': ['c#_medium', 'c#_proficient', 'java_medium c#_proficient']})
        # descriptions = data['col_2']
        # print('Skill set similar to: ', new_desc)
        # print(SimilaritiesLookUp.get_recommendations(new_desc, descriptions))

        new_desc = pd.Series('java dev')
        data = pd.DataFrame.from_dict(
            {'col_2': ['junior python dev', 'junior js dev', 'senior java dev', 'senior dafs dev', 'kfsld ewe dev',
                       'fasf fsda dev']})
        descriptions = data['col_2']

        new_desc = pd.Series(target_user_sill_set)
        data = pd.DataFrame.from_records(other_users)
        # print(data)
        descriptions = data['skill_set']

        recommended_users = SimilaritiesLookUp.get_recommendations(data, new_desc, descriptions)
        recommended_users = recommended_users[recommended_users['score'] >= threshold]

        recommended_users_list = [User(row['username'], row['external_id'], row['score']) for index, row in recommended_users.iterrows()]

        return recommended_users_list
