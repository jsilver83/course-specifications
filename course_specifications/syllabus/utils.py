import copy

from course_specifications.utils import get_textbooks_by_system_id


def get_weekly_topics_list(total_contact_hours, w_num, topics):
    """"
    :param total_contact_hours: the total number of contact hours
    :param w_num: the number of weeks
    :param topics:the list of topics
    :return: A list that contains lists. Each list contains topics for a week
    """
    w_hours = total_contact_hours / w_num
    topics_list = []
    if (topics):
        for i in range(0, w_num):
            week_list = []
            temp = w_hours
            temp_list = []
            for topic in topics:
                if temp >= topic.contact_hours:
                    temp_list.append(topic)
                    week_list.append(topic)
                    if (temp == topic.contact_hours):
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


def get_textbooks_list(book_system_ids):
    cleaned_book_system_ids = clean_book_ids(book_system_ids)
    text_book_list = []
    response = get_textbooks_by_system_id(cleaned_book_system_ids)
    if response and response != 'ERROR':
        text_book_list = [textbook for textbook in response]
    return text_book_list


def clean_book_ids(book_system_ids):
    book_system_ids = book_system_ids.replace("'", '')
    book_system_ids = book_system_ids.replace('"', '')
    book_system_ids = book_system_ids.replace('[', '')
    book_system_ids = book_system_ids.replace(']', '')
    book_system_ids = book_system_ids.replace(' ', '')
    return book_system_ids
