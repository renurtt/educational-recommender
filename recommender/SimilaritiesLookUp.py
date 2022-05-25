from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

from recommender.models import User, LearningMaterial

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pymorphy2


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
    def get_similarities_in_skill_set(target_user_sill_set, other_users, threshold):
        # new_desc = pd.Series('c#_proficient java_low')
        # data = pd.DataFrame.from_dict(
        #     {
        #         'col_2': ['c#_medium', 'c#_proficient', 'java_medium c#_proficient']})
        # descriptions = data['col_2']
        # print('Skill set similar to: ', new_desc)
        # print(SimilaritiesLookUp.get_recommendations(new_desc, descriptions))

        # new_desc = pd.Series('java dev')
        # data = pd.DataFrame.from_dict(
        #     {'col_2': ['junior python dev', 'junior js dev', 'senior java dev', 'senior dafs dev', 'kfsld ewe dev',
        #                'fasf fsda dev']})
        # descriptions = data['col_2']

        new_desc = pd.Series(target_user_sill_set)
        data = pd.DataFrame.from_records(other_users)
        # print(data)
        descriptions = data['skill_set']

        recommended_users = SimilaritiesLookUp.get_recommendations(data, new_desc, descriptions)
        recommended_users = recommended_users[recommended_users['score'] >= threshold]

        recommended_users_list = [User(row['username'], row['external_id'], row['score']) for index, row in
                                  recommended_users.iterrows()]

        return recommended_users_list

    @staticmethod
    def get_similarities_in_desired_position(target_user_desired_position, other_users, threshold):
        new_desc = pd.Series(target_user_desired_position)
        data = pd.DataFrame.from_records(other_users)
        # print(data)
        descriptions = data['desired_position']

        recommended_users = SimilaritiesLookUp.get_recommendations(data, new_desc, descriptions)
        recommended_users = recommended_users[recommended_users['score'] >= threshold]

        recommended_users_list = [User(row['username'], row['external_id'], row['score']) for index, row in
                                  recommended_users.iterrows()]

        return recommended_users_list

    @staticmethod
    def normalize_words_in_string(morph, string):
        x = [morph.parse(word)[0].normal_form for word in string.split(' ')]
        normalized = ' '.join(x)
        return normalized

    @staticmethod
    def get_similar_materials(user_description, materials):
        pd.options.mode.chained_assignment = None
        morph = pymorphy2.MorphAnalyzer()

        user_description = SimilaritiesLookUp.normalize_words_in_string(morph, user_description)

        user_description = pd.Series(user_description)
        materials = pd.DataFrame.from_records(materials)

        for i in range(len(materials['overview'])):
            materials['overview'][i] = SimilaritiesLookUp.normalize_words_in_string(morph, materials['overview'][i])

        materials_desc = materials['overview']


        overall_descriptions = pd.concat([materials_desc, user_description])

        cv = CountVectorizer()
        count_matrix = cv.fit_transform(overall_descriptions)
        cosine_sim = cosine_similarity(count_matrix)

        # print(cosine_sim)
        sim_scores = list(enumerate(cosine_sim[-1][:-1]))
        # print('sim_scores', sim_scores)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        indices = [i[0] for i in sim_scores]

        recommendations = pd.concat([materials.iloc[indices],
                                     pd.Series([i[1] for i in sim_scores], name='score',
                                               index=[i[0] for i in sim_scores])],
                                    axis=1, ignore_index=False)

        # print('rec', recommendations)

        recommendations = recommendations[recommendations['score'] >= 0.1]

        recommendations = [LearningMaterial(row['id'], row['score']) for index, row in
                           recommendations.iterrows()]
        return recommendations
