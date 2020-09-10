from scraper.course import Course

test_header_rows = (
    ''' CSS   490  SPECIAL TOPICS ''',
    ''' CSS   301  TECHNICAL WRITINGPrerequisites '''
    ''' CSS   385  INTRO TO GAME DEV(VLPA/NW)Prerequisites (cancellation in effect) ''',
)

test_sections = (
    ''' 
Restr  11050 B  5       MTWTh  900-1130   UW2  031      Si,Dong                    Open     12/  45           $23        
                        A-term                                                                                                                                              
                        TOPIC: MACHINE INTELLIGENCE                                                                                                                         
                        IN THIS CLASS, STUDENTS WILL LEARN                                                                                                                  
                        ABOUT THEORETICAL FOUNDATIONS OF                                                                                                                    
                        MACHINE LEARNING AND HOW TO USE IT                                                                                                                  
                        TO SOLVE REAL-WORLD PROBLEMS.                                                                                                                       
                        MACHINE LEARNING IS AN EXCITING                                                                                                                     
                        AND FAST-MOVING FIELD WITH MANY                                                                                                                     
                        SUCCESSFUL CONSUMER APPLICATIONS,                                                                                                                   
                        E.G., GOOGLE TRANSLATE/ALPHAGO,                                                                                                                     
                        APPLE SIRI, MICROSOFT KINECT, FACE                                                                                                                  
                        DETECTION IN DIGITAL CAMERAS,                                                                                                                       
                        AMAZON/NETFLIX RECOMMENDATIONS,                                                                                                                     
                        AND MORE.                                                                                                                                           
                        PREREQS: CSS 343, ST MATH 308,                                                                                                                      
                        STATISTICS                                                                                                                                          
 ''',
    ''' 
Restr  12928 A  5       TTh    330-530    DISC 061      Pisan,Yusuf                Closed   46/  45           $23        
 '''
)

test_outputs = (
    '''{"name": "SPECIAL TOPICS", "code": "CSS", "number": "490", "quarter": "SUMMER", "year": "2019", 
    "gen_ed_marker": "", "description": "A-term TOPIC: MACHINE INTELLIGENCE IN THIS CLASS, STUDENTS WILL LEARN ABOUT 
    THEORETICAL FOUNDATIONS OF MACHINE LEARNING AND HOW TO USE IT TO SOLVE REAL-WORLD PROBLEMS. MACHINE LEARNING IS 
    AN EXCITING AND FAST-MOVING FIELD WITH MANY SUCCESSFUL CONSUMER APPLICATIONS, E.G., GOOGLE TRANSLATE/ALPHAGO, 
    APPLE SIRI, MICROSOFT KINECT, FACE DETECTION IN DIGITAL CAMERAS, AMAZON/NETFLIX RECOMMENDATIONS, 
    AND MORE. PREREQS: CSS 343, ST MATH 308, STATISTICS", "is_restricted": "Restr", "sln": "11050", "section_id": 
    "B", "credits": "5", "meeting_days": ["M", "T", "W", "Th"], "meeting_time_start": "9:00", "meeting_time_end": 
    "11:30", "room": "UW2  031", "instructor": "Si,Dong", "status": "Open", "currently_enrolled": 12, 
    "enrollment_limit": 45, "is_crnc": "", "course_fee": "$23", "special_type": ""} '''
)

def test_course_name():
    course = Course(test_header_rows[0], "", "", "")
    assert course.name == 'GAME ENGINE DEV'


def test_course_code():
    pass


def test_course_number():
    pass


def test_course_quarter():
    pass


def test_course_year():
    pass


def test_course_gen_end_marker():
    pass


def test_course_description():
    pass


def test_course_is_restricted():
    pass


def test_course_sln():
    pass


def test_course_section_id():
    pass


def test_course_credits():
    pass


def test_course_meeting_time_start():
    pass


def test_course_meeting_time_end():
    pass


def test_course_room():
    pass


def test_course_instructor():
    pass


def test_course_section():
    pass


def test_course_currently_enrolled():
    pass


def test_course_enrollment_limit():
    pass


def test_course_is_crnc():
    pass


def test_course_fee():
    pass
