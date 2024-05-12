
class Chassis_TestStatics():

    def __init__(self):
        '''
        Class of "enums", i.e., static string-value variables used throughout the conway_test module
        as a way to use consistent strings when they reference a named domain structural element.
        '''

    CHASSIS_SCENARIOS_REPO                          = "CHASSIS_SCENARIOS_REPO"  
    '''
    Denotes an environment variable that points to the root folder under which all the test scenarios reside
    for the :class:`conway_test`, i.e., the root folder for the ``conway_scenarios`` repo.

    This is a root directory that then breaks into sub-folders by ``scenario_id``, each of which is a test database for
    the scenario denoted by that ``scenario_id``.
    ''' 

    # When testing the repo administrator, we need to simulate root folders for the local and remote collection
    # of repos
    #
    BUNDLED_REPOS_LOCAL_FOLDER                      = "bundled_repos_local"
    BUNDLED_REPOS_REMOTE_FOLDER                     = "bundled_repos_remote"

    TEST_USER_PROFILE_NAME                          = "TestRobot@CCL"
    '''
    Denotes the name of the user profile that should be used when running tests for conway.ops functionality.
    This name can be used to retrieve a profile object with information such as:

    * The location of local and remote repos
    * The Conway-based projects and repos accessible to the user behind this profile
    * GitHub credentials

    A test-specific variant ensures that the tests have available fixtures (e.g., repos and GitHub users that
    exist for the purposes of the tests only)
    '''


