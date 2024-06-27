#!/usr/bin/env python3
"""Module that inserts a new document in a collection"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a MongoDB collection based on kwargs.

    Args:
    mongo_collection: A pymongo collection object
    **kwargs: Arbitrary keyword arguments representing the document fields

    Returns:
    The _id of the newly inserted document
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
