

user_roles_data = [
  # {'role_name': 'superuser'},
  {'role_name': 'client'},
  {'role_name': 'manager'},
  {'role_name': 'redactor'},
]

# {
#   "name": "string",
#   "login": "string",
#   "email": "user@example.com",
#   "password": "string",
#   "comment": "string",
#   "role_id": 0
# }

users_data = [
  {"name": "rus", "login": "rus", "email": "rus@gmail.com", "password": "12345"},
  {"name": "ven", "login": "ven", "email": "ven@example.com", "password": "12345", "comment": "ven", "role_id": 2},
  {"name": "rad", "login": "rad", "email": "rad@example.com", "password": "12345", "comment": "rad", "role_id": 3},
  {"name": "kar", "login": "kar", "email": "kar@example.com", "password": "12345", "comment": "kar", "role_id": 2},
  {"name": "als", "login": "als", "email": "als@example.com", "password": "12345", "comment": "string", "role_id": 3},
  {"name": "leila", "login": "leila", "email": "leila@example.com", "password": "12345", "comment": "string", "role_id": 2},
  {"name": "mama", "login": "mama", "email": "mama@example.com", "password": "12345", "comment": "string", "role_id": 3},
  {"name": "papa", "login": "papa", "email": "papa@example.com", "password": "12345", "comment": "string", "role_id": 2},
  {"name": "bor", "login": "bor", "email": "bor@example.com", "password": "12345", "comment": "string", "role_id": 2},
  {"name": "ant", "login": "ant", "email": "ant@example.com", "password": "12345", "comment": "string", "role_id": 3},
  {"name": "and", "login": "and", "email": "and@example.com", "password": "12345", "role_id": 3},
  {"name": "kost", "login": "kost", "email": "kost@example.com", "password": "12345", "role_id": 2},
]

currency_data = [
  {'currency_name': 'RUB'},
  {'currency_name': 'USD'}
]

client_clusters_data = [
  {'name': 'Вкусная история'},
  {'name': 'Пир горой'},
  {'name': 'Сытый кот'},
  {'name': 'Домашний уют'},
  {'name': 'С пылу с жару'},
]



client_groups_data = [
  {'name': 'Пир на весь мир', 'comment': 'комментарий', 'client_cluster_id': 1},
  {'name': 'Вкусная планета', 'comment': '', 'client_cluster_id': 2},
  {'name': 'Еда в радость', 'comment': '', 'client_cluster_id': 3},
  {'name': 'Гастрономические путешествия', 'comment': 'комментарий', 'client_cluster_id': 4},
  {'name': 'Сытый гость', 'comment': '', 'client_cluster_id': 5},
  {'name': 'Кулинарный рай', 'comment': '', 'client_cluster_id': 1},
  {'name': 'Традиции вкуса', 'comment': '', 'client_cluster_id': 1},
  {'name': 'Домашний очаг', 'comment': 'комментарий', 'client_cluster_id': 2},
  {'name': 'С пылу с жару', 'comment': '', 'client_cluster_id': 2},
  {'name': 'Мир вкусов', 'comment': '', 'client_cluster_id': 3},
  {'name': 'Ресторанный дом', 'comment': 'комментарий', 'client_cluster_id': 3},
  {'name': 'Столичный вкус', 'comment': 'комментарий', 'client_cluster_id': 4},
  {'name': 'Вкусный выбор', 'comment': '', 'client_cluster_id': 1},
  {'name': 'Аппетит', 'comment': '', 'client_cluster_id': 2},
  {'name': 'В кругу друзей', 'comment': 'комментарий', 'client_cluster_id': 3},
  {'name': 'Ели Сумели', 'comment': '', 'client_cluster_id': 4},
  {'name': 'Доби Хуеби', 'comment': 'комментарий', 'client_cluster_id': 4},
]


client_data = [
  {"name": "Вкусная история", "city": "Москва", "email": "vkusnayaistoriya@mail.ru", "phone": "+7 (916) 123-45-67", "price": 999, 'currency_id': 1, 'client_group_id': 1},
  {"name": "Сытый кот", "city": "Санкт-Петербург", "email": "sytiykot@gmail.com", "phone": "+7 (812) 987-65-43", "price": 1980, 'currency_id': 1, 'client_group_id': 2},
  {"name": "Домашний уют", "city": "Екатеринбург", "email": "domashniyuyut@yandex.ru", "phone": "+7 (343) 567-89-10", "price": 5349, 'currency_id': 1, 'client_group_id': 3},
  {"name": "The Gourmet Spot", "city": "New York", "email": "contact@gourmetspot.com", "phone": "+1-555-0101", "price": 435, 'currency_id': 1, 'client_group_id': 4},
  {"name": "Savory Bites", "city": "Los Angeles", "email": "info@savorybites.com", "phone": "+1-555-0102", "price":5345, 'currency_id': 1, 'client_group_id': 5},
  {"name": "Epicurean Delights", "city": "Chicago", "email": "reservations@epicureandelights.com", "phone": "+1-555-0103", "price": 5345, 'currency_id': 1, 'client_group_id': 6},
  {"name": "Fusion Feast", "city": "Houston", "email": "contact@fusionfeast.com", "phone": "+1-555-0104", "price":5345, 'currency_id': 1, 'client_group_id': 7},
  {"name": "Culinary Haven", "city": "Phoenix", "email": "info@culinaryhaven.com", "phone": "+1-555-0105", "price": 5345, 'currency_id': 1, 'client_group_id': 8},
  {"name": "Flavor Town", "city": "Philadelphia", "email": "contact@flavortown.com", "phone": "+1-555-0106", "price":5345, 'currency_id': 1, 'client_group_id': 9},
  {"name": "Gastronomy Bliss", "city": "San Antonio", "email": "info@gastronomybliss.com", "phone": "+1-555-0107", "price": 2344, 'currency_id': 1, 'client_group_id': 10},
  {"name": "Delectable Dishes", "city": "San Diego", "email": "reservations@delectabledishes.com", "phone": "+1-555-0108", "price":2344, 'currency_id': 1, 'client_group_id': 11},
  {"name": "Taste Temptations", "city": "Dallas", "email": "info@tastetemptations.com", "phone": "+1-555-0109", "price": 2344, 'currency_id': 1, 'client_group_id': 12},
  {"name": "Palate Pleasers", "city": "San Jose", "email": "contact@palatepleasers.com", "phone": "+1-555-0110", "price": 234, 'currency_id': 1, 'client_group_id': 13},
  {"name": "Epic Eats", "city": "Austin", "email": "info@epiceats.com", "phone": "+1-555-0111", "price": 342, 'currency_id': 1, 'client_group_id': 14},
  {"name": "Tasty Treats", "city": "Jacksonville", "email": "contact@tastytreats.com", "phone": "+1-555-0112", "price": 23, 'currency_id': 1, 'client_group_id': 15},
  {"name": "Gourmet Garden", "city": "Jacksonville", "email": "info@gourmetgarden.com", "phone": "+1-555-0113", "price": 31, 'currency_id': 1, 'client_group_id': 16},
  {"name": "Savor Sensations", "city": "Columbus", "email": "contact@savorsensations.com", "phone": "+1-555-0114", "price": 234, 'currency_id': 1, 'client_group_id': 9},
  {"name": "Delightful Dining", "city": "Fort Worth", "email": "info@delightfuldining.com", "phone": "+1-555-0115", "price": 123, 'currency_id': 1, 'client_group_id': 1},
  {"name": "Gastronomic Wonders", "city": "Indianapolis", "email": "contact@gastronomicwonders.com", "phone": "+1-555-0116", "price": 11, 'currency_id': 1, 'client_group_id': 2},
  {"name": "Savory Selections", "city": "Charlotte", "email": "info@savoryselections.com", "phone": "+1-555-0117", "price": 11, 'currency_id': 2, 'client_group_id': 3},
  {"name": "Culinary Creations", "city": "Seattle", "email": "contact@culinarycreations.com", "phone": "+1-555-0118", "price": 31, 'currency_id': 2, 'client_group_id': 4},
  {"name": "Tasteful Temptations", "city": "Denver", "email": "info@tastefultemptations.com", "phone": "+1-555-0119", "price": 13, 'currency_id': 2, 'client_group_id': 5},
  {"name": "Epicurean Experience", "city": "Washington", "email": "contact@epicureanexperience.com", "phone": "+1-555-0120", "price": 23, 'currency_id': 2, 'client_group_id': 6},
  {"name": "Delicious Delights", "city": "Boston", "email": "info@deliciousdelights.com", "phone": "+1-555-0121", "price": 21, 'currency_id': 2, 'client_group_id': 7},
  {"name": "Gourmet Grandeur", "city": "El Paso", "email": "contact@gourmetgrandeur.com", "phone": "+1-555-0122", "price": 33, 'currency_id': 2, 'client_group_id': 8},
  {"name": "Savory Spots", "city": "Nashville", "email": "info@savoryspots.com", "phone": "+1-555-0123", "price": 22, 'currency_id': 2, 'client_group_id': 1},
  {"name": "Culinary Canvas", "city": "Detroit", "email": "contact@culinarycanvas.com", "phone": "+1-555-0124", "price": 11, 'currency_id': 2, 'client_group_id': 2},
  {"name": "Tasteful Tides", "city": "Memphis", "email": "info@tastefultides.com", "phone": "+1-555-0125", "price": 666, 'currency_id': 2, 'client_group_id': 3},
  {"name": "Epicurean Euphoria", "city": "Portland", "email": "contact@epicureaneuphoria.com", "phone": "+1-555-0126", "price": 555, 'currency_id': 2, 'client_group_id': 4},
  {"name": "Gastronomy Galore", "city": "Oklahoma City", "email": "info@gastronomygalore.com", "phone": "+1-555-0127", "price": 444, 'currency_id': 2, 'client_group_id': 5},
  {"name": "Savory Symphony", "city": "Las Vegas", "email": "contact@savorysymphony.com", "phone": "+1-555-0128", "price": 333, 'currency_id': 2, 'client_group_id': 6},
  {"name": "Culinary Capers", "city": "Louisville", "email": "info@culinarycapers.com", "phone": "+1-555-0129", "price": 222, 'currency_id': 2, 'client_group_id': 7},
  {"name": "Taste Sensations", "city": "Baltimore", "email": "contact@tastesensations.com", "phone": "+1-555-0130", "price": 111, 'currency_id': 2, 'client_group_id': 8},
  {"name": "Gourmet Glee", "city": "Milwaukee", "email": "info@gourmetglee.com", "phone": "+1-555-0131", "price": 888, 'currency_id': 2, 'client_group_id': 1},
  {"name": "Savory Scenes", "city": "Albuquerque", "email": "contact@savoryscenes.com", "phone": "+1-555-0132", "price": 777, 'currency_id': 2, 'client_group_id': 2},
  {"name": "Culinary Concepts", "city": "Tucson", "email": "info@culinaryconcepts.com", "phone": "+1-555-0133", "price": 666, 'currency_id': 2, 'client_group_id': 3},
  {"name": "Taste Trends", "city": "Fresno", "email": "contact@tastetrends.com", "phone": "+1-555-0134", "price": 3213, 'currency_id': 2, 'client_group_id': 4},
  {"name": "Epicurean Escapade", "city": "Sacramento", "email": "info@epicureanescapade.com", "phone": "+1-555-0135", "price": 9999, 'currency_id': 2, 'client_group_id': 5},
  {"name": "Gastronomy Gems", "city": "Kansas City", "email": "contact@gastronomygems.com", "phone": "+1-555-0136", "price": 6454, 'currency_id': 2, 'client_group_id': 6},
  {"name": "Savory Stories", "city": "Mesa", "email": "info@savorystories.com", "phone": "+1-555-0137", "price": 123, 'currency_id': 2, 'client_group_id': 7},
]



client_profile = [
    {"address": "123 Main St, New York, NY", "full_name": "John Doe", "certificate": "Certified Professional", "contract_number": "CN-001", "contract_date": "2024-07-13"},
    {"address": "456 Elm St, Los Angeles, CA", "full_name": "Jane Smith", "certificate": "Expert Technician", "contract_number": "CN-002", "contract_date": "2024-07-13"},
    {"address": "789 Oak St, Chicago, IL", "full_name": "Robert Johnson", "certificate": "Senior Engineer", "contract_number": "CN-003", "contract_date": "2024-07-13"},
    {"address": "321 Pine St, Houston, TX", "full_name": "Michael Brown", "certificate": "Certified Specialist", "contract_number": "CN-004", "contract_date": "2024-07-13"},
    {"address": "654 Cedar St, Phoenix, AZ", "full_name": "Emily Davis", "certificate": "Technical Consultant", "contract_number": "CN-005", "contract_date": "2024-07-13"},
    {"address": "987 Maple St, Philadelphia, PA", "full_name": "William Miller", "certificate": "Lead Developer", "contract_number": "CN-006", "contract_date": "2024-07-13"},
    {"address": "111 Birch St, San Antonio, TX", "full_name": "Sarah Wilson", "certificate": "Software Engineer", "contract_number": "CN-007", "contract_date": "2024-07-13"},
    {"address": "222 Spruce St, San Diego, CA", "full_name": "James Martinez", "certificate": "System Architect", "contract_number": "CN-008", "contract_date": "2024-07-13"},
    {"address": "333 Palm St, Dallas, TX", "full_name": "Patricia Anderson", "certificate": "Network Specialist", "contract_number": "CN-009", "contract_date": "2024-07-13"},
    {"address": "444 Willow St, San Jose, CA", "full_name": "David Thomas", "certificate": "IT Manager", "contract_number": "CN-010", "contract_date": "2024-07-13"},
    {"address": "555 Cypress St, Austin, TX", "full_name": "Linda Taylor", "certificate": "Project Manager", "contract_number": "CN-011", "contract_date": "2024-07-13"},
    {"address": "666 Chestnut St, Jacksonville, FL", "full_name": "Christopher Jackson", "certificate": "Data Analyst", "contract_number": "CN-012", "contract_date": "2024-07-13"},
    {"address": "777 Fir St, San Francisco, CA", "full_name": "Barbara Lee", "certificate": "Database Administrator", "contract_number": "CN-013", "contract_date": "2024-07-13"},
    {"address": "888 Poplar St, Columbus, OH", "full_name": "Daniel Harris", "certificate": "Security Specialist", "contract_number": "CN-014", "contract_date": "2024-07-13"},
    {"address": "999 Redwood St, Fort Worth, TX", "full_name": "Elizabeth Clark", "certificate": "Cloud Engineer", "contract_number": "CN-015", "contract_date": "2024-07-13"},
    {"address": "101 Pinecone St, Indianapolis, IN", "full_name": "Joseph Lewis", "certificate": "DevOps Engineer", "contract_number": "CN-016", "contract_date": "2024-07-13"},
    {"address": "202 Acorn St, Charlotte, NC", "full_name": "Susan Walker", "certificate": "Frontend Developer", "contract_number": "CN-017", "contract_date": "2024-07-13"},
    {"address": "303 Mapleleaf St, Seattle, WA", "full_name": "Paul Hall", "certificate": "Backend Developer", "contract_number": "CN-018", "contract_date": "2024-07-13"},
    {"address": "404 Oakleaf St, Denver, CO", "full_name": "Jessica Young", "certificate": "Full Stack Developer", "contract_number": "CN-019", "contract_date": "2024-07-13"},
    {"address": "505 Pineapple St, Washington, DC", "full_name": "Steven King", "certificate": "Mobile Developer", "contract_number": "CN-020", "contract_date": "2024-07-13"},
    {"address": "606 Elmleaf St, Boston, MA", "full_name": "Karen Wright", "certificate": "UX/UI Designer", "contract_number": "CN-021", "contract_date": "2024-07-13"},
    {"address": "707 Cedarbough St, El Paso, TX", "full_name": "Mark Lopez", "certificate": "QA Engineer", "contract_number": "CN-022", "contract_date": "2024-07-13"},
    {"address": "808 Redwoodbark St, Nashville, TN", "full_name": "Nancy Hill", "certificate": "Product Manager", "contract_number": "CN-023", "contract_date": "2024-07-13"},
    {"address": "909 Oakwood St, Detroit, MI", "full_name": "Joshua Scott", "certificate": "Business Analyst", "contract_number": "CN-024", "contract_date": "2024-07-13"},
    {"address": "101 Cedarwood St, Memphis, TN", "full_name": "Betty Green", "certificate": "Data Scientist", "contract_number": "CN-025", "contract_date": "2024-07-13"},
    {"address": "202 Elmwood St, Portland, OR", "full_name": "Gregory Adams", "certificate": "Machine Learning Engineer", "contract_number": "CN-026", "contract_date": "2024-07-13"},
    {"address": "303 Pineforest St, Oklahoma City, OK", "full_name": "Donna Baker", "certificate": "AI Specialist", "contract_number": "CN-027", "contract_date": "2024-07-13"},
    {"address": "404 Cedarforest St, Las Vegas, NV", "full_name": "Matthew Rodriguez", "certificate": "Blockchain Developer", "contract_number": "CN-028", "contract_date": "2024-07-13"},
    {"address": "505 Elmforest St, Louisville, KY", "full_name": "Sandra Martinez", "certificate": "Game Developer", "contract_number": "CN-029", "contract_date": "2024-07-13"},
    {"address": "606 Pinehill St, Baltimore, MD", "full_name": "Donald Hernandez", "certificate": "Embedded Systems Engineer", "contract_number": "CN-030", "contract_date": "2024-07-13"},
    {"address": "707 Cedarhill St, Milwaukee, WI", "full_name": "Lisa Moore", "certificate": "Robotics Engineer", "contract_number": "CN-031", "contract_date": "2024-07-13"},
    {"address": "123 Main St, New York, NY", "full_name": "John Doe", "certificate": "Certified Professional", "contract_number": "CN-001", "contract_date": "2024-07-13"},
    {"address": "456 Elm St, Los Angeles, CA", "full_name": "Jane Smith", "certificate": "Expert Technician", "contract_number": "CN-002", "contract_date": "2024-07-13"},
    {"address": "789 Oak St, Chicago, IL", "full_name": "Robert Johnson", "certificate": "Senior Engineer", "contract_number": "CN-003", "contract_date": "2024-07-13"},
    {"address": "321 Pine St, Houston, TX", "full_name": "Michael Brown", "certificate": "Certified Specialist", "contract_number": "CN-004", "contract_date": "2024-07-13"},
    {"address": "654 Cedar St, Phoenix, AZ", "full_name": "Emily Davis", "certificate": "Technical Consultant", "contract_number": "CN-005", "contract_date": "2024-07-13"},
    {"address": "987 Maple St, Philadelphia, PA", "full_name": "William Miller", "certificate": "Lead Developer", "contract_number": "CN-006", "contract_date": "2024-07-13"},
    {"address": "111 Birch St, San Antonio, TX", "full_name": "Sarah Wilson", "certificate": "Software Engineer", "contract_number": "CN-007", "contract_date": "2024-07-13"},
    {"address": "222 Spruce St, San Diego, CA", "full_name": "James Martinez", "certificate": "System Architect", "contract_number": "CN-008", "contract_date": "2024-07-13"},
    {"address": "333 Palm St, Dallas, TX", "full_name": "Patricia Anderson", "certificate": "Network Specialist", "contract_number": "CN-009", "contract_date": "2024-07-13"},
]


# for ind, item in enumerate(client_data):
#     params = {"name": item['name'], "city": item['city'], "email": item['email'], "phone": item['phone'], "price": item['price'], "client_group_id": item['client_group_id'], "currency_id": item['currency_id'],
#               'profile': client_profile[ind]}
#     print(params)




main_group_data = [
  {'group_name': 'first group'},
  {'group_name': 'second group'},
  {'group_name': 'therd group'},
  {'group_name': 'fourth group'},
  {'group_name': 'fith group'},
  {'group_name': ''}
]

track_group_data = [
  {'track_collection_name': 'first', 'player_option': True, 'group_coollection_id': 1},
  {'track_collection_name': 'second', 'player_option': False, 'group_coollection_id': 1},
  {'track_collection_name': 'therd', 'player_option': True, 'group_coollection_id': 2},
  {'track_collection_name': 'fourth', 'player_option': False, 'group_coollection_id': 2},
  {'track_collection_name': 'sixten', 'group_coollection_id': 3},
  {'track_collection_name': 'fifth', 'player_option': False, 'group_coollection_id': 23},
  {'player_option': True, 'group_coollection_id': 1},
]

from collections import Counter

append_user_to_client_group_list = [
  {'client_group_id': 1, 'user_id': 2},
  {'client_group_id': 2, 'user_id': 3},
  {'client_group_id': 3, 'user_id': 4},
  {'client_group_id': 4, 'user_id': 5},
  {'client_group_id': 5, 'user_id': 6},
  {'client_group_id': 6, 'user_id': 7},
  {'client_group_id': 7, 'user_id': 8},
  {'client_group_id': 8, 'user_id': 9},
  {'client_group_id': 1, 'user_id': 10},
  {'client_group_id': 2, 'user_id': 2},
  {'client_group_id': 3, 'user_id': 3},
  {'client_group_id': 4, 'user_id': 4},
  {'client_group_id': 5, 'user_id': 5},
  {'client_group_id': 6, 'user_id': 6},
  {'client_group_id': 7, 'user_id': 7},
  {'client_group_id': 8, 'user_id': 8},
  {'client_group_id': 9, 'user_id': 9},
  {'client_group_id': 10, 'user_id': 6},
  {'client_group_id': 1, 'user_id': 7},
  {'client_group_id': 2, 'user_id': 12},
  {'client_group_id': 4, 'user_id': 2},
  {'client_group_id': 5, 'user_id': 3},
  {'client_group_id': 6, 'user_id': 4},
  {'client_group_id': 7, 'user_id': 5},
]

# unqiue_items = [tuple(item.items()) for item in append_user_to_client_group_list]
# print(unqiue_items is append_user_to_client_group_list)
# counter = Counter(unqiue_items)
# if all(count == 1 for count in counter.values()):
#   print('uniqu')
# else:
#   print('not uniqu')

filterd_clients = [entry['client_group_id'] for entry in append_user_to_client_group_list if entry['user_id'] == 2]
counter = Counter(filterd_clients)
count_len = len(counter)
# print(count_len)


# user_id = 12
# count = 0
# for item in append_user_to_client_group_list:
#   if item['user_id'] == user_id:
#     count += 1
# print(count)