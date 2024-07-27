# Pipelines for Database Query

def get_course_pipeline(course_id):
    return [
        {
            '$match': {
                'course_id': course_id
            }
        },
        {
            '$lookup': {
                'from': "course_material",
                'let': { 'course_id': "$course_id" },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': { '$eq': ["$course_id", "$$course_id"] }
                        }
                    },
                    {
                        '$sort': { 'week': 1 }
                    }
                ],
                'as': "materials"
            }
        },
        {
            '$lookup': {
                'from': "assignment",
                'let': { 'course_id': "$course_id" },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': { '$eq': ["$course_id", "$$course_id"] }
                        }
                    },
                    {
                        '$sort': { 'week': 1 }
                    }
                ],
                'as': "assignments"
            }
        },
        {
            '$lookup': {
                'from': "coding_assignment",
                'let': { 'course_id': "$course_id" },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': { '$eq': ["$course_id", "$$course_id"] }
                        }
                    },
                    {
                        '$sort': { 'week': 1 }
                    }
                ],
                'as': "coding_assignments"
            }
        },
        {
            '$project': {
                '_id': 1,
                'course_id': 1,
                'course_name': 1,
                'materials': {
                    '$map': {
                        'input': "$materials",
                        'as': "material",
                        'in': {
                            'material_id': "$$material._id",
                            'course_id': "$$material.course_id",
                            'material_type': "$$material.material_type",
                            'url': "$$material.url",
                            'content': "$$material.content",
                            'week': "$$material.week"
                        }
                    }
                },
                'assignments': {
                    '$map': {
                        'input': "$assignments",
                        'as': "assignment",
                        'in': {
                            'assgn_id': "$$assignment._id",
                            'question': "$$assignment.question",
                            'q_type': "$$assignment.q_type",
                            'options': "$$assignment.options",
                            'answers': "$$assignment.answers",
                            'assgn_type': "$$assignment.assgn_type",
                            'course_id': "$$assignment.course_id",
                            'week': "$$assignment.week",
                            'deadline': "$$assignment.deadline"
                        }
                    }
                },
                'coding_assignments': {
                    '$map': {
                        'input': "$coding_assignments",
                        'as': "coding_assignment",
                        'in': {
                            'assgn_id': "$$coding_assignment._id",
                            'question': "$$coding_assignment.question",
                            'language': "$$coding_assignment.language",
                            'public_testcase': "$$coding_assignment.public_testcase",
                            'private_testcase': "$$coding_assignment.private_testcase",
                            'assgn_type': "$$coding_assignment.assgn_type",
                            'course_id': "$$coding_assignment.course_id",
                            'week': "$$coding_assignment.week",
                            'deadline': "$$coding_assignment.deadline"
                        }
                    }
                }
            }
        }
    ]


def get_course_pipeline_week(course_id, week):
    return [
        {
            '$match': {
                'course_id': course_id
            }
        },
        {
            '$lookup': {
                'from': "course_material",
                'let': { 'course_id': "$course_id" },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': { 
                                '$and': [
                                    { '$eq': ["$course_id", "$$course_id"] },
                                    { '$eq': ["$week", week] }
                                ]
                            }
                        }
                    },
                    {
                        '$sort': { 'week': 1 }
                    }
                ],
                'as': "materials"
            }
        },
        {
            '$lookup': {
                'from': "assignment",
                'let': { 'course_id': "$course_id" },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': { 
                                '$and': [
                                    { '$eq': ["$course_id", "$$course_id"] },
                                    { '$eq': ["$week", week] }
                                ]
                            }
                        }
                    },
                    {
                        '$sort': { 'week': 1 }
                    }
                ],
                'as': "assignments"
            }
        },
        {
            '$lookup': {
                'from': "coding_assignment",
                'let': { 'course_id': "$course_id" },
                'pipeline': [
                    {
                        '$match': {
                            '$expr': { 
                                '$and': [
                                    { '$eq': ["$course_id", "$$course_id"] },
                                    { '$eq': ["$week", week] }
                                ]
                            }
                        }
                    },
                    {
                        '$sort': { 'week': 1 }
                    }
                ],
                'as': "coding_assignments"
            }
        },
        {
            '$project': {
                '_id': 0,
                'course_id': 1,
                'course_name': 1,
                'materials': {
                    '$map': {
                        'input': "$materials",
                        'as': "material",
                        'in': {
                            'material_id': "$$material._id",
                            'course_id': "$$material.course_id",
                            'material_type': "$$material.material_type",
                            'url': "$$material.url",
                            'content': "$$material.content",
                            'week': "$$material.week"
                        }
                    }
                },
                'assignments': {
                    '$map': {
                        'input': "$assignments",
                        'as': "assignment",
                        'in': {
                            'assgn_id': "$$assignment._id",
                            'question': "$$assignment.question",
                            'q_type': "$$assignment.q_type",
                            'options': "$$assignment.options",
                            'answers': "$$assignment.answers",
                            'assgn_type': "$$assignment.assgn_type",
                            'course_id': "$$assignment.course_id",
                            'week': "$$assignment.week",
                            'deadline': "$$assignment.deadline"
                        }
                    }
                },
                'coding_assignments': {
                    '$map': {
                        'input': "$coding_assignments",
                        'as': "coding_assignment",
                        'in': {
                            'assgn_id': "$$coding_assignment._id",
                            'question': "$$coding_assignment.question",
                            'language': "$$coding_assignment.language",
                            'public_testcase': "$$coding_assignment.public_testcase",
                            'private_testcase': "$$coding_assignment.private_testcase",
                            'assgn_type': "$$coding_assignment.assgn_type",
                            'course_id': "$$coding_assignment.course_id",
                            'week': "$$coding_assignment.week",
                            'deadline': "$$coding_assignment.deadline"
                        }
                    }
                }
            }
        }
    ]
