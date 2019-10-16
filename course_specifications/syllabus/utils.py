import copy

def get_topics_list(w_hours,w_num,topics):
    topics_list = []
    if(topics):
        for i in range(0,w_num):
            week_list= []
            temp = w_hours
            temp_list = []
            # print(topics)
            for topic in topics:
                if temp >= topic.contact_hours:
                    temp_list.append(topic)
                    week_list.append(topic)
                    if(temp == topic.contact_hours):
                        break
                    else:
                        temp -= topic.contact_hours
                else:
                    topic.contact_hours -= temp
                    if '(Continue)' not in topic.topic:
                        deep_topic_copy = copy.deepcopy(topic)
                        week_list.append(deep_topic_copy)
                        topic.topic += ' (Continue)'
                    else:
                        week_list.append(topic)
                    break
            topics_list.append(week_list)
            for item in temp_list:
                topics.remove(item)
    return topics_list



