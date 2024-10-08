from pymongo import MongoClient

# Exercice 1 :

def prizes_per_category_basic(client: MongoClient) -> list[dict]:
    pipeline = [
        {"$group": {
            "_id": "$category",
            "prizes": {"$sum": 1}
        }},
        {"$project": {
            "_id": 1,
            "prizes": 1
        }}
    ]
    results = client["nobel"]["prizes"].aggregate(pipeline)
    return list(results)

# Exercice 2 :

def prizes_per_category_sorted(client: MongoClient) -> list[dict]:
    pipeline = [
        {"$group": {
            "_id": "$category",
            "prizes": {"$sum": 1}
        }},
        {"$sort": {
            "prizes": -1,
            "_id": 1 
        }}
    ]
    results = client["nobel"]["prizes"].aggregate(pipeline)
    return list(results)

# Exercice 3 :

def prizes_per_category_filtered(client: MongoClient, nb_laureates: int) -> list[dict]:
    pipeline = [
        {"$match": {
            "laureates": {"$size": nb_laureates}
        }},
        {"$group": {
            "_id": "$category",
            "prizes": {"$sum": 1}
        }}
    ]
    results = client["nobel"]["prizes"].aggregate(pipeline)
    return list(results)

# Exercice 4 :

def prizes_per_category(client: MongoClient, nb_laureates: int) -> list[dict]:
    pipeline = [
        {"$match": {
            "laureates": {"$size": nb_laureates}
        }},
        {"$group": {
            "_id": "$category",
            "prizes": {"$sum": 1}
        }},
        {"$sort": {
            "prizes": -1,
            "_id": 1
        }}
    ]
    results = client["nobel"]["prizes"].aggregate(pipeline)
    return list(results)


# Exercice 5 :  

def laureates_per_birth_country_complex(client: MongoClient) -> list[dict]:
    pipeline = [
        {
            "$match": {
                "$or": [
                    {
                        "$and": [
                            {"died": {"$ne": "0000-00-00"}},
                            {"$expr": {"$eq": ["$diedCountry", "$bornCountry"]}}
                        ]
                    },
                    {"died": "0000-00-00"}
                ]
            }
        },
        {
            "$group": {
                "_id": "$bornCountry",
                "laureates": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 1,
                "laureates": 1
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        }
    ]
    results = client["nobel"]["laureates"].aggregate(pipeline)
    return list(results)