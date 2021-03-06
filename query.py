import json

def valid_course_not_in_fav(sub, num, email):
    return """
        SELECT True 
        FROM course
        WHERE Subject='{}' AND Number='{}' 
        AND NOT EXISTS 
        (SELECT True FROM favorite WHERE COURSE_SUB='{}' AND COURSE_NUM='{}' AND EMAIL='{}')
    """.format(sub, num, sub, num, email)

def get_subject(subject): # Group By
    return """  
        SELECT DISTINCT subject, number, MIN(title), ROUND(AVG(overall_gpa), 2) FROM course \
        WHERE subject='{subject}' \
        GROUP BY subject, number
        ;
    """.format(subject = subject)


def get_favorite(email): # join 
    return """
        SELECT favorite.course_sub, favorite.course_num, course.title, course.overall_gpa
        FROM favorite INNER JOIN course ON 
        favorite.COURSE_SUB = course.Subject AND favorite.COURSE_NUM = course.NUMBER
        where favorite.EMAIL = '{email}' 
        ;
    """.format(email = email)

def insert_favorite(email, course_sub, course_num):
    return """
        INSERT INTO favorite (EMAIL, COURSE_SUB, COURSE_NUM)
        SELECT * FROM (SELECT '{email}', '{course_sub}', '{course_num}') AS TMP
        WHERE NOT EXISTS (
	    SELECT * FROM favorite WHERE EMAIL = '{email}' \
                AND COURSE_SUB = '{course_sub}' AND COURSE_NUM = '{course_num}'
        ) LIMIT 1""".format(email=email, course_num = course_num, course_sub=course_sub)

def update_favorite(email, old_course_sub, old_course_num, new_course_sub, new_course_num):
    return """
        UPDATE favorite
        SET COURSE_SUB = '{new_course_sub}', COURSE_NUM = '{new_course_num}'
        WHERE EMAIL = '{email}' AND COURSE_SUB = '{old_course_sub}' AND COURSE_NUM = '{old_course_num}'
    """.format(email=email, old_course_sub=old_course_sub, old_course_num=old_course_num, new_course_sub=new_course_sub, new_course_num=new_course_num)

def remove_favorite(email, course_sub, course_num):
    return """
        DELETE FROM favorite
        WHERE EMAIL = '{email}' AND COURSE_SUB = '{course_sub}' AND COURSE_NUM = '{course_num}'
    """.format(email=email, course_sub=course_sub, course_num=course_num)

# def aggregate_sections_grade(subject_name, subject_number): # Group By
#     return """
#         SELECT SUM(ap) as ap, SUM(a) as a, SUM(am) as am, SUM(bp) as bp, SUM(b) as b, \
#                SUM(bm) as bm, SUM(cp) as cp, SUM(c) as c, SUM(cm) as cm, SUM(dp) as dp, \
#                SUM(d) as d, SUM(dm) as dm, SUM(f) as f, SUM(w) as w, instructor, semester\
#         FROM raw
#         WHERE `subject`='{subject_name}' AND number='{subject_number}'
#         GROUP BY instructor, semester, `subject`, number
#     """.format(subject_name = subject_name, subject_number = subject_number)

def find_course_instructor(subject_name, subject_number):
    return """
        SELECT MIN(title) # A simplification
        FROM raw
        WHERE `subject`='{subject_name}' AND number='{subject_number}'
        GROUP BY `subject`, `number`
    """.format(subject_name = subject_name, subject_number = subject_number)

def advance_fun2(data):
    data = [(i[0], "{}{}".format(*i[1:])) for i in data]
    i2c, c2i = {}, {}
    for i, c in data:
        i2c[i] = i2c.get(i, []) + [c]
        c2i[c] = c2i.get(c, []) + [i]
    return i2c, c2i