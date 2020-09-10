import pytest

# flake8: noqa
@pytest.fixture(scope="module")
def global_data():
    return {
        'header_rows': (
            ''' CSS   490  SPECIAL TOPICS ''',
            ''' CSS   301  TECHNICAL WRITINGPrerequisites ''',
            ''' CSS   385  INTRO TO GAME DEV(VLPA/NW)Prerequisites (cancellation in effect) ''',
        ),
        'main_rows': (
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
Restr  13190 D  5       MW     845-1045   UW1  060      Kool,Nancy L.              Open     21/  30           $10  W     
                        IN-CLASS ASSIGNMENTS DUE ON                                                                                                                         
                        FIRST DAY OF QUARTER.                                                                                                                               
                        UNREGISTERED STUDENTS                                                                                                                               
                        PLANNING TO REGISTER SHOULD                                                                                                                         
                        ATTEND CLASS ON THE FIRST DAY                                                                                                                       
                        AND EMAIL CSSADV@UW.EDU.                                                                                                                            
 '''
            ''' 
Restr  12928 A  5       TTh    330-530    DISC 061      Pisan,Yusuf                Closed   46/  45           $23        
 '''
        )
    }
