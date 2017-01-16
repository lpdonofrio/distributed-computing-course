#Prompt: detect when two accounts actually belong to the same person

#This code is modified from code originally written by Jim Blomo and Derek Kuo


from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from mrjob.step import MRStep


class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def mapper1_extract_user_business(self,_,record):
        """Taken a record, yield <user_id, business_id>"""
        yield [record['user_id'], record['business_id']]

    def reducer1_compile_businesses_under_user(self,user_id,business_ids):
        business_ids = list(set(business_ids))
        yield [user_id, business_ids]

    def mapper2_collect_businesses_under_user(self, user_id, business_ids):
        yield ['LIST', [user_id, business_ids]]

    def reducer2_calculate_similarity(self,stat,user_business_ids):
        def Jaccard_similarity(business_list1, business_list2):
            jaccard = len((set(business_list1) & set(business_list2))) / len((set(business_list1) | set(business_list2)))
            return jaccard

        user_business_ids = list(user_business_ids)
        for item1 in range(0, len(user_business_ids)-1):
            for item2 in range(item1+1, len(user_business_ids)):
                similarity = Jaccard_similarity(user_business_ids[item1][1], user_business_ids[item2][1])
                if similarity >= 0.5:
                    yield [[user_business_ids[item1][0],user_business_ids[item2][0]], similarity]


    def steps(self):
        return [
            MRStep(mapper=self.mapper1_extract_user_business, reducer=self.reducer1_compile_businesses_under_user),
            MRStep(mapper=self.mapper2_collect_businesses_under_user, reducer= self.reducer2_calculate_similarity)
        ]


if __name__ == '__main__':
    UserSimilarity.run()
