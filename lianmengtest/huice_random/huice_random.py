import random

class HuiceRandom:
    def __init__(self):
        self.changjing = {
            '开屏': 1.0,
            '全屏': 1.5,
            '激励': 1.5,
            '信息流': 1.0,
            '插屏': 1.0,
            '全局 + 自选染': 0.5,
            'draw': 0.5,
            'banner + 新插屏': 0.5,
            '版本壳 + 插件': 0.5,
        }
        self.renyuanlist = ['范佳旺', '刘静怡', '葛珺','杨跃娟']
        self.changjinglist = list(self.changjing.keys())
        self.total_sum = sum(self.changjing.values())
        self.value_per_person = self.total_sum / len(self.renyuanlist)
        self.result = {}
        self.result_time={}
        self.pianyiliang=0.5
    def random_changjing(self):
        sum_per_person = 0
        assigned_scenes = []
        for i, person in enumerate(self.renyuanlist):
            if i != len(self.renyuanlist) - 1:
                for scene in self.changjinglist:
                    assigned_scenes.append(scene)
                    sum_per_person=sum_per_person + self.changjing[scene]
                    if  sum_per_person>= self.value_per_person-self.pianyiliang:
                        self.result[person] = assigned_scenes
                        self.result_time[person]=sum_per_person
                        print(f"{person} 分配的场景: {assigned_scenes},预估总时长:{sum_per_person}")
                        break
                sum_per_person = 0
                for scene in assigned_scenes:
                    self.changjinglist.remove(scene)
                assigned_scenes = []
            else:
                for scene in self.changjinglist:
                    assigned_scenes.append(scene)
                    sum_per_person = sum_per_person + self.changjing[scene]
        self.result[self.renyuanlist[len(self.renyuanlist) - 1]] = assigned_scenes
        self.result_time[self.renyuanlist[len(self.renyuanlist) - 1]] = sum_per_person
        print(f"{self.renyuanlist[len(self.renyuanlist) - 1]} 分配的场景: {assigned_scenes},预估总时长:{sum_per_person}")

    def youhua_random_changjing(self):
        for i in range(1000):
            self.changjinglist = list(self.changjing.keys())
            random.shuffle(self.renyuanlist)
            random.shuffle(self.changjinglist)
            self.random_changjing()
            # print(self.result)
            # print(self.result_time)
            youhua_result=True
            for x in range(len(self.renyuanlist)):
                for y in range(x+1,len(self.renyuanlist)):
                    if abs(self.result_time[self.renyuanlist[x]]-self.result_time[self.renyuanlist[y]])>self.pianyiliang:
                        youhua_result=False
                        break
            if youhua_result==True:
                return self.result
            else:
                print(f"第{i+1}次优化后分配结果不符合预期，舍弃")



# 示例用法
huice_random = HuiceRandom()
print(huice_random.value_per_person)
print(huice_random.youhua_random_changjing())
