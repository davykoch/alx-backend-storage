#!/usr/bin/env python3
"""Module that returns top students by average score"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
    mongo_collection: A pymongo collection object

    Returns:
    A list of students sorted by average score in descending order
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {"$sort": {"averageScore": -1}}
    ]

    return list(mongo_collection.aggregate(pipeline))
