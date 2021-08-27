def validAttribute(type, attribute):
	if type == "book":
		return attribute in ["book_url","title","book_id","ISBN",\
		"author_url","author","rating","rating_count","review_count",\
		"image_url","similar_books"]
	elif type == "author":
		return attribute in ["name", "author_url","author_id","rating",\
		"rating_count","review_count","image_url","related_authors","author_books"]
	return False
def validType(type):
  	return type == "book" or type == "author"
def validValue(value):
	if len(value) == 0:
		return False
	if "\"" in value:
		if value.count("\"") %2 != 0:
			return False
	if "NOT" in value:
		if len(value.strip()) - 3 <= 0:
			return False
	if ">" in value:
		if len(value.split(">")) != 2:
			return False
	if "<" in value:
		if len(value.split("<")) != 2:
			return False
	return True
def validCondition(condition):
	if not validType(condition[0][0]):
		return False
	if not validAttribute(condition[0][0], condition[0][1]):
		return False
	if not validValue(condition[1]):
		return False
	return True
def splitCondition(condition):
	condition = condition.split(":")
	condition[0] = condition[0].split(".")
	condition[0][0] = condition[0][0].strip()
	condition[0][1] = condition[0][1].strip()
	condition[1] = condition[1].strip()
	return condition
def parser(query):
	select_query = {}
	conditions = []
	if "AND" in query:
		conditions = query.split("AND")
		if len(conditions[0]) == 0 or len(conditions[1]) == 0:
			return None
		conditions[0] = splitCondition(conditions[0])
		conditions[1] = splitCondition(conditions[1])
	elif "OR" in query:
		conditions = query.split("OR")
		if len(conditions[0]) == 0 or len(conditions[1]) == 0:
			return None
		conditions[0] = splitCondition(conditions[0])
		conditions[1] = splitCondition(conditions[1])
	else:
		conditions.append(splitCondition(query))
	print(conditions)
	if len(conditions) == 1:
		if not validCondition(conditions[0]):
			return None
		values = conditions[0][1]
		attribute = conditions[0][0][1]
		if "NOT" in values:
			values = valuex.split("NOT")[1].strip()
		elif ">" in values:
			value_gt = float(values.split(">")[1])
			if "\"" in values:
				return None
			select_query[attribute] = {"$gt" : value_gt}
		elif "<" in values:
			value_gt = float(values.split("<")[1])
			if "\"" in values:
				return None
			select_query[attribute] = {"$lt" : value_gt}
		else:
			if values.isdigit():
				values = int(values)
			elif values.replace('.','',1).isdigit():
				values = float(values)
			select_query[attribute] = values 
	else:
		if conditions[0][1].isdigit():
			conditions[0][1] = int(conditions[0][1])
		elif conditions[0][1].replace('.','',1).isdigit():
			conditions[0][1] = float(conditions[0][1])
		if conditions[1][1].isdigit():
			conditions[1][1] = int(conditions[1][1])
		elif conditions[1][1].replace('.','',1).isdigit():
			conditions[1][1] = float(conditions[1][1])
		if "AND" in query:
			select_query["$and"] = [
				{conditions[0][0][1] : conditions[0][1]},\
				{conditions[1][0][1] : conditions[1][1]},\
			]
		elif "OR" in query:
			select_query["$or"] = [
				{conditions[0][0][1] : conditions[0][1]},\
				{conditions[1][0][1] : conditions[1][1]},\
			]
		else:
			return None
	print(select_query)
	return conditions[0][0][0], select_query
