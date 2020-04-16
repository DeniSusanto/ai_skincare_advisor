import config
import pandas as pd
import numpy as np
import nltk
nltk.download('punkt')
nltk.download("stopwords")
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

RECOMMENDATION_THRESHOLD = config.RECOMMENDATION_THRESHOLD
FACIAL_ISSUES_KEYS = config.FACIAL_ISSUES_KEYS
AVAILABLE_CONCERNS = config.AVAILABLE_CONCERNS
ALL_ISSUES_AND_CONCERNS = FACIAL_ISSUES_KEYS + AVAILABLE_CONCERNS

RECOMMENDATION_PRODUCT_MAPPING = config.RECOMMENDATION_PRODUCT_MAPPING

RS_PRICE_WEIGHT = config.RS_PRICE_WEIGHT
RS_RATINGS_WEIGHT = config.RS_RATINGS_WEIGHT
RS_LIKES_WEIGHT = config.RS_LIKES_WEIGHT
RS_PREFERENCES_WEIGHT = config.RS_PREFERENCES_WEIGHT

class ProductRecommendation():
#     main input is a dict data structure. It consists data from questionnaire and facial features detection.
#     keys include:
#         acne float
#         wrinkles float
#         crows_feet float
#         dark_eye float
#         sallowness float
#         skin_type stirng
#         allergies [string]
#         price float
#         concerns [string]
#         preferences [string]
# 
#     example of input
# 
#     main_input = {
#     'acne': 3,
#     'wrinkles': 2,
#     'crows_feet': 2,
#     'dark_eye': 2,
#     'sallowness': 1.4,
#     'skin_type': "oily",
#     'allergies': ["glycerin","camellia"],
#     'price': 50,
#     'concerns': ["pores", "redness", "acne"],
#     'preferences': ["lightweight", 'eye cream']
# }
        
    def __init__(self, catalogue_df, main_input):
        self.input = main_input
        if self.input['price']:
            self.input['price'] = float(self.input['price'])
        else:
            self.input['price'] = float("inf")
        self.product_catalogue_df = catalogue_df
        self.concerns = []
        self.issues = []
        for k,v in main_input.items():
            if k in RECOMMENDATION_THRESHOLD:
                if v >= RECOMMENDATION_THRESHOLD[k]:
                    self.issues.append(k)
        if main_input['concerns']:
            for concern in main_input['concerns']:
                if (concern in FACIAL_ISSUES_KEYS):
                    if (concern not in self.issues):
                        self.issues.append(concern)
                else:
                    self.concerns.append(concern)
                
   
    def _global_filtered_catalogue(self):
        bool_filter = np.ones(self.product_catalogue_df.shape[0], dtype=bool)
        if self.input['skin_type']:
            bool_filter = bool_filter & (self.product_catalogue_df[self.input['skin_type']] == 1)
        if self.input['allergies']:
            bool_filter = bool_filter & (~(self.product_catalogue_df["ingredients"].str.contains('|'.join(self.input['allergies']))))
        return self.product_catalogue_df[bool_filter].reset_index(drop = True).copy()

    def optional_filtered_catalogue(self, catalogue_df, filter_dict):
        bool_filter = np.ones(catalogue_df.shape[0], dtype=bool)
        for (k, v) in filter_dict.items():
            if v != None:
                if k == "price":
                    bool_filter = bool_filter & (catalogue_df["price"] <= v)
                if k == "concern":
                    bool_filter = bool_filter & (catalogue_df[v] == 1)
                if k == "label":
                    bool_filter = bool_filter & (catalogue_df["Label"] == v)
        return catalogue_df[bool_filter].reset_index(drop = True).copy()
    
    def sort_recommended_products(self, catalogue_df):
        values=[]
        ratings = catalogue_df["rating"].tolist()
        prices = catalogue_df["price"].tolist()
        likes = catalogue_df["likes"].tolist()

        max_price = catalogue_df["price"].max()
        max_rating = catalogue_df["rating"].max()
        max_likes = catalogue_df["likes"].max()
        scores=[]
        if self.input['preferences']:
            X=" ".join(self.input['preferences'])
            for i in range(len(catalogue_df)):
                Y=catalogue_df['description'].iloc[i]
                X_list=[]
                Y_list=[]
                X_list = word_tokenize(X)  
                Y_list = word_tokenize(Y)
                sw = stopwords.words('english')  
                l1 =[]
                l2 =[] 

                X_set={}
                Y_set={}
                X_set = {w for w in X_list if not w in sw}  
                Y_set = {w for w in Y_list if not w in sw} 
                rvector=[]
                rvector = X_set.union(Y_set)  

                for w in rvector: 
                    if w in X_set: l1.append(1) # create a vector 
                    else: l1.append(0) 
                    if w in Y_set: l2.append(1) 
                    else: l2.append(0) 
                c = 0
                for i in range(len(rvector)): 
                    c+= l1[i]*l2[i] 
                try:
                    cosine = c / float((sum(l1)*sum(l2))**0.5)
                except:
                    cosine = 0
                values.append(cosine)
            new_filtered = catalogue_df.assign(cosine=values)
            cosines = new_filtered["cosine"].tolist()
            for i in range(len(catalogue_df)):
                score= RS_PRICE_WEIGHT * (max_price-prices[i])/max_price + RS_RATINGS_WEIGHT * ratings[i]/max_rating + \
                RS_LIKES_WEIGHT * likes[i]/max_likes + RS_PREFERENCES_WEIGHT * cosines[i]
                scores.append(score)
        else:
            for i in range(len(catalogue_df)):
                score= RS_PRICE_WEIGHT * (max_price-prices[i])/max_price + RS_RATINGS_WEIGHT * ratings[i]/max_rating + \
                RS_LIKES_WEIGHT * likes[i]/max_likes + RS_PREFERENCES_WEIGHT * 1
                scores.append(score)
            
            

        catalogue_df["scores"]=scores
        sorted_catalogue = catalogue_df.sort_values(by = ["scores"], ascending = False).reset_index(drop = True).copy()
        return sorted_catalogue
    
    #Will mainly call this. Will return a bunch of recommendations based on products
    def get_default_recommendation(self):
        main_filtered = self._global_filtered_catalogue()
        
        recommendation = {}
        for issue in self.issues:
            labels = RECOMMENDATION_PRODUCT_MAPPING[issue]
            products_dir = {}
            for label in labels:
                price = self.input['price']
                filter_dict = {
                    'price' : price,
                    'label' : label
                }
                specific_filtered = self.optional_filtered_catalogue(main_filtered, filter_dict)
                sorted_specific_filtered = self.sort_recommended_products(specific_filtered)
                products_dir[label] = sorted_specific_filtered
            recommendation[issue] = products_dir
            
        for concern in self.concerns:
            price = self.input['price']
            filter_dict = {
                'price' : price,
                'concern' : concern
            }
            specific_filtered = self.optional_filtered_catalogue(main_filtered, filter_dict)
            sorted_specific_filtered = self.sort_recommended_products(specific_filtered)
            recommendation[concern] = sorted_specific_filtered
            
        recommendation["all_products"] = self.sort_recommended_products(self.optional_filtered_catalogue(main_filtered, {
                'price' : self.input['price']}))
        
        return recommendation